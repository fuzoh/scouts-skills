"""`site` : site statique du dépôt (GitHub Pages) depuis `site/*.md` et le registre.

  site [--out build/site]

Chaque `site/<nom>.md` (frontmatter `title`, `order`, `menu` facultatif : libellé court
ou `false` pour ne pas figurer au menu) devient `<out>/<nom>.html` dans un gabarit unique :
menu, titre, pied de page (licences, dépôt, version de `pyproject.toml`). Les liens
relatifs `x.md` deviennent `x.html`. `site/sources.md` sert d'en-tête à la page des
sources, complétée par la liste des sources embarquées (`status` indexed ou verified,
`decision` différente de rejected), groupées par émetteur. `site/nouveautes.md` sert
d'en-tête à la page des versions, complétée par `CHANGELOG.md` (tenu par release-please)
sans son titre de premier niveau.

Sortie déterministe (aucune date, tris stables). Code 1 si un lien interne ne pointe
vers aucun fichier généré.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import typer
import yaml
from markdown_it import MarkdownIt

from scripts import registry as reg

app = typer.Typer(add_completion=False, help=__doc__)

SITE_NAME = "Skills scouts"
REPO_URL = "https://github.com/fuzoh/scouts-skills"
EMBEDDED_STATUSES = ("indexed", "verified")
SOURCES_PAGE = "sources"
CHANGELOG_PAGE = "nouveautes"
CHANGELOG_TITLE_RE = re.compile(r"\A\s*# [^\n]*\n")
ISSUER_LABELS = {
    "msds": "Mouvement Scout de Suisse (MSdS)",
    "cofor": "Commission formation du MSdS (cofor)",
    "js": "Jeunesse+Sport (J+S) / OFSPO",
    "cudesch": "cudesch",
}
ISSUER_ORDER = ("msds", "cofor", "js", "cudesch")
OTHERS_LABEL = "Autres émetteurs"
FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.DOTALL)
HREF_RE = re.compile(r'href="([^"]*)"')

CSS = """\
:root {
  color-scheme: light dark;
  --fond: #f4f6f3; --carte: #ffffff; --texte: #1d2521; --doux: #5b675f; --bord: #dde3dc;
  --accent: #1f6b46; --accent-fond: #e5f1ea; --code-fond: #eef2ee; --ombre: 0 1px 3px rgb(0 0 0 / .06), 0 8px 24px rgb(0 0 0 / .05);
}
@media (prefers-color-scheme: dark) {
  :root {
    --fond: #121714; --carte: #1a211d; --texte: #e3e9e4; --doux: #9daaa1; --bord: #2c3630;
    --accent: #6fcf9a; --accent-fond: #1f3127; --code-fond: #232c27; --ombre: none;
  }
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--fond); color: var(--texte); font: 1.0625rem/1.65 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
a { color: var(--accent); text-underline-offset: .2em; text-decoration-thickness: 1px; }
a:hover { text-decoration-thickness: 2px; }
:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; border-radius: 4px; }
.saut { position: absolute; left: -999px; }
.saut:focus { position: static; display: block; padding: .5rem 1rem; background: var(--carte); }
.cadre { max-width: 52rem; margin: 0 auto; padding: 0 1.25rem; }
header { background: var(--carte); border-bottom: 1px solid var(--bord); }
header .cadre { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: .5rem 1.5rem; padding-block: .9rem; }
.marque { margin: 0; font-weight: 700; font-size: 1.1rem; }
.marque a { color: var(--texte); text-decoration: none; }
.marque span { display: block; font-weight: 400; font-size: .85rem; color: var(--doux); }
header nav ul { list-style: none; padding: 0; margin: 0; display: flex; flex-wrap: wrap; gap: .3rem; }
header nav a { display: block; padding: .3rem .75rem; border-radius: 999px; color: var(--texte); text-decoration: none; font-size: .95rem; }
header nav a:hover { background: var(--accent-fond); }
header nav a[aria-current="page"] { background: var(--accent); color: var(--carte); font-weight: 600; }
main { max-width: calc(52rem - 2.5rem); background: var(--carte); margin: 2rem auto; padding: 2rem 2.5rem 2.5rem; border: 1px solid var(--bord); border-radius: 14px; box-shadow: var(--ombre); }
.page-index main > h1 { font-size: 2.4rem; }
.page-index main > h1 + p { font-size: 1.2rem; color: var(--doux); }
h1, h2, h3 { line-height: 1.25; }
h1 { font-size: 2rem; margin: 0 0 1.25rem; letter-spacing: -.01em; }
h2 { font-size: 1.4rem; margin: 2.25rem 0 .75rem; padding-top: 1.25rem; border-top: 1px solid var(--bord); }
h3 { font-size: 1.1rem; margin: 1.75rem 0 .5rem; }
li { margin: .3rem 0; }
li::marker { color: var(--accent); }
strong { font-weight: 650; }
table { border-collapse: separate; border-spacing: 0; display: block; width: fit-content; max-width: 100%; overflow-x: auto; margin: 1.25rem 0; border: 1px solid var(--bord); border-radius: 10px; font-size: .95rem; }
th, td { padding: .55rem .8rem; text-align: left; vertical-align: top; border-bottom: 1px solid var(--bord); }
tr:last-child td { border-bottom: 0; }
th { background: var(--accent-fond); font-weight: 600; }
tbody tr:nth-child(even) td { background: color-mix(in srgb, var(--fond) 50%, transparent); }
code { font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace; font-size: .9em; background: var(--code-fond); padding: .1em .35em; border-radius: 5px; }
pre { overflow-x: auto; padding: 1rem 1.15rem; background: var(--code-fond); border: 1px solid var(--bord); border-radius: 10px; line-height: 1.5; }
pre code { background: none; padding: 0; }
blockquote { margin: 1.25rem 0; padding: .75rem 1.1rem; border-left: 4px solid var(--accent); background: var(--accent-fond); border-radius: 0 10px 10px 0; }
footer { color: var(--doux); font-size: .875rem; padding-bottom: 2.5rem; }
footer p { margin: .4rem 0; }
footer a { color: inherit; }
@media (max-width: 52rem) { main { margin-inline: 1.25rem; } }
@media (max-width: 40rem) {
  main { margin: 0; border-radius: 0; border-inline: 0; padding: 1.5rem 1.25rem 2rem; }
  .page-index main > h1 { font-size: 1.9rem; }
  h1 { font-size: 1.65rem; }
  header nav a { padding: .2rem .6rem; font-size: .9rem; }
}
"""

GABARIT = """\
<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · {site}</title>
<meta name="description" content="{description}">
<style>
{css}</style>
</head>
<body class="page-{name}">
<a class="saut" href="#contenu">Aller au contenu</a>
<header>
<div class="cadre">
<p class="marque"><a href="index.html">{site}</a><span>Assistants du scoutisme suisse</span></p>
<nav aria-label="Menu principal">
<ul>
{menu}
</ul>
</nav>
</div>
</header>
<main id="contenu">
<h1>{title}</h1>
{body}</main>
<footer class="cadre">
<p>Code sous licence MIT. Contenu propre (skills, référentiels, savoirs, site, documentation) sous licence <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.fr">CC BY-SA 4.0</a>. Textes officiels : droits à leurs auteurs, listés dans <a href="sources.html">Sources et auteurs</a>.</p>
<p>Ce site n'est pas une publication officielle du MSdS ni de J+S. Dépôt : <a href="{repo}">{repo_short}</a>. Version {version}.</p>
</footer>
</body>
</html>
"""


class SiteError(Exception):
    pass


@dataclass
class Page:
    name: str          # nom du fichier sans extension
    title: str
    order: int
    menu: str | None   # libellé au menu, None si absent du menu
    description: str
    body_md: str


# --------------------------------------------------------------------------- #
# Markdown
# --------------------------------------------------------------------------- #

def _heading_ids(self, tokens, idx, options, env):
    """`id` stable sur chaque titre, dédoublonné par page."""
    token = tokens[idx]
    inline = tokens[idx + 1] if idx + 1 < len(tokens) else None
    if inline is not None and not token.attrGet("id"):
        base = reg.slugify(inline.content) or "section"
        seen = env.setdefault("ids", {})
        n = seen.get(base, 0) + 1
        seen[base] = n
        token.attrSet("id", base if n == 1 else f"{base}-{n}")
    return self.renderToken(tokens, idx, options, env)


def _md_links(self, tokens, idx, options, env):
    """Lien relatif `page.md[#ancre]` → `page.html[#ancre]`."""
    token = tokens[idx]
    href = str(token.attrGet("href") or "")
    parts = urlsplit(href)
    if not parts.scheme and not parts.netloc and parts.path.endswith(".md"):
        new = parts.path[:-3] + ".html" + (f"#{parts.fragment}" if parts.fragment else "")
        token.attrSet("href", new)
    return self.renderToken(tokens, idx, options, env)


def markdown() -> MarkdownIt:
    md = MarkdownIt("commonmark", {"html": False}).enable("table")
    md.add_render_rule("heading_open", _heading_ids)
    md.add_render_rule("link_open", _md_links)
    return md


# --------------------------------------------------------------------------- #
# Pages
# --------------------------------------------------------------------------- #

def site_dir() -> Path:
    return reg.ROOT / "site"


def load_page(path: Path) -> Page:
    text = path.read_text(encoding="utf-8")
    m = FRONT_RE.match(text)
    if not m:
        raise SiteError(f"{path.name} : frontmatter `---` manquant")
    try:
        front = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as exc:
        raise SiteError(f"{path.name} : frontmatter yaml invalide ({exc})") from exc
    if not front.get("title"):
        raise SiteError(f"{path.name} : `title` manquant")
    if not isinstance(front.get("order"), int):
        raise SiteError(f"{path.name} : `order` entier manquant")
    menu = front.get("menu", front["title"])
    return Page(
        name=path.stem,
        title=str(front["title"]),
        order=front["order"],
        menu=None if menu is False else str(menu),
        description=str(front.get("description") or front["title"]),
        body_md=m.group(2),
    )


def load_pages(folder: Path | None = None) -> list[Page]:
    folder = folder or site_dir()
    paths = sorted(p for p in folder.glob("*.md") if not p.name.startswith("_"))
    if not paths:
        raise SiteError(f"aucune page dans {folder}")
    pages = [load_page(p) for p in paths]
    return sorted(pages, key=lambda p: (p.order, p.name))


def render_menu(pages: list[Page], current: str) -> str:
    items = []
    for p in pages:
        if p.menu is None:
            continue
        cur = ' aria-current="page"' if p.name == current else ""
        items.append(f'<li><a href="{p.name}.html"{cur}>{html.escape(p.menu)}</a></li>')
    return "\n".join(items)


def render_page(page: Page, pages: list[Page], body_html: str, version: str) -> str:
    return GABARIT.format(
        title=html.escape(page.title),
        name=page.name,
        site=SITE_NAME,
        description=html.escape(page.description, quote=True),
        css=CSS,
        menu=render_menu(pages, page.name),
        body=body_html,
        repo=REPO_URL,
        repo_short=REPO_URL.removeprefix("https://github.com/"),
        version=html.escape(version),
    )


# --------------------------------------------------------------------------- #
# Page des sources
# --------------------------------------------------------------------------- #

def embedded_sources(sources: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """Sources embarquées dans `scouts-ressources` (même règle que `build`)."""
    sources = reg.all_sources() if sources is None else sources
    return [s for s in sources
            if s.get("status") in EMBEDDED_STATUSES and s.get("decision") != "rejected"]


def _capitalize(text: str) -> str:
    """Majuscule initiale, sauf pour un nom de domaine (camp-equitable.ch)."""
    if "." in text.split(" ", 1)[0]:
        return text
    return text[:1].upper() + text[1:]


def issuer_label(src: dict[str, Any]) -> str:
    """Libellé de l'émetteur : nom officiel, sinon `issuer_detail`."""
    issuer = str(src.get("issuer") or "")
    if issuer in ISSUER_LABELS:
        return ISSUER_LABELS[issuer]
    return _capitalize(str(src.get("issuer_detail") or "").strip()) or OTHERS_LABEL


def _sort_key(text: str) -> str:
    return reg.slugify(text, max_len=500)


def _sorted_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(items, key=lambda s: (_sort_key(str(s.get("title") or "")), str(s.get("id"))))


def group_sources(sources: list[dict[str, Any]]) -> list[tuple[str, list[tuple[str, list[dict[str, Any]]]]]]:
    """Groupes de premier niveau, chacun en sous-groupes (émetteur, sources).

    Émetteurs officiels dans l'ordre d'ISSUER_ORDER, un sous-groupe chacun (libellé vide) ;
    puis « Autres émetteurs », un sous-groupe par `issuer_detail`, triés par libellé.
    """
    groups: dict[str, list[dict[str, Any]]] = {}
    for s in sources:
        groups.setdefault(issuer_label(s), []).append(s)
    out: list[tuple[str, list[tuple[str, list[dict[str, Any]]]]]] = []
    official = [ISSUER_LABELS[i] for i in ISSUER_ORDER]
    for label in official:
        if label in groups:
            out.append((label, [("", _sorted_items(groups[label]))]))
    others = sorted((k for k in groups if k not in official), key=_sort_key)
    if others:
        out.append((OTHERS_LABEL, [(k, _sorted_items(groups[k])) for k in others]))
    return out


def _date_fr(value: Any) -> str:
    try:
        d = value if isinstance(value, date) else date.fromisoformat(str(value))
    except ValueError:
        return str(value)
    return d.strftime("%d.%m.%Y")


def _edition(src: dict[str, Any]) -> str:
    version = str(src.get("version") or "").strip()
    if version:
        return f"version {version}"
    published = src.get("published")
    if published:
        return f"publié le {_date_fr(published)}"
    return ""


def render_source(src: dict[str, Any]) -> str:
    e = html.escape
    title = e(str(src.get("title") or src.get("id")))
    details = [f"<code>{e(str(src['id']))}</code>"]
    ref = str(src.get("ref") or "").strip()
    if ref:
        details.append(f"réf. {e(ref)}")
    edition = _edition(src)
    if edition:
        details.append(e(edition))
    links = []
    url = str(src.get("url") or "").strip()
    file_url = str(src.get("file_url") or "").strip()
    if url:
        links.append(f'<a href="{e(url, quote=True)}">page d\'origine</a>')
    if file_url and file_url != url:
        links.append(f'<a href="{e(file_url, quote=True)}">fichier</a>')
    parts = [f"<strong>{title}</strong>", ", ".join(details) + "."]
    parts.append(("Lien : " + ", ".join(links) + ".") if links else "Pas de lien public.")
    if src.get("redactions"):
        parts.append("Données personnelles ou d'accès retirées (caviardage).")
    return "<li>" + " ".join(parts) + "</li>"


def render_sources(sources: list[dict[str, Any]], env: dict[str, Any] | None = None) -> str:
    """HTML de la liste ; `env` partagé avec l'en-tête pour des `id` de titres uniques."""
    groups = group_sources(sources)
    issuers = sum(len(sub) for _, sub in groups)
    out = [f"<p>{len(sources)} sources embarquées, {issuers} émetteurs.</p>"]
    md = markdown()
    env = {} if env is None else env
    for label, subgroups in groups:
        out.append(md.render(f"## {label}", env).strip())
        for sublabel, items in subgroups:
            if sublabel:
                out.append(md.render(f"### {sublabel}", env).strip())
            out.append("<ul>")
            out.extend(render_source(s) for s in items)
            out.append("</ul>")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- #
# Page des versions
# --------------------------------------------------------------------------- #

def render_changelog(path: Path, env: dict[str, Any] | None = None) -> str:
    """HTML de `CHANGELOG.md` sans son titre `# …` ; message d'attente s'il n'existe pas."""
    if not path.is_file():
        return "<p>Aucune version publiée pour l'instant.</p>\n"
    text = CHANGELOG_TITLE_RE.sub("", path.read_text(encoding="utf-8"), count=1)
    return markdown().render(text, {} if env is None else env)


# --------------------------------------------------------------------------- #
# Génération et contrôle
# --------------------------------------------------------------------------- #

def build_site(out: Path) -> list[Path]:
    """Écrit le site dans `out` ; retourne les fichiers écrits."""
    pages = load_pages()
    names = {p.name for p in pages}
    for required in ("index", SOURCES_PAGE):
        if required not in names:
            raise SiteError(f"page `site/{required}.md` manquante")
    version = reg.project_version()
    out.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for page in pages:
        env: dict[str, Any] = {}
        body = markdown().render(page.body_md, env)
        if page.name == SOURCES_PAGE:
            body += render_sources(embedded_sources(), env)
        elif page.name == CHANGELOG_PAGE:
            body += render_changelog(reg.ROOT / "CHANGELOG.md", env)
        path = out / f"{page.name}.html"
        path.write_text(render_page(page, pages, body, version), encoding="utf-8")
        written.append(path)
    return written


def check_links(out: Path, files: list[Path] | None = None) -> list[str]:
    """Liens relatifs (et ancres) qui ne pointent vers aucune des pages `files` (défaut : `out/*.html`)."""
    errors: list[str] = []
    ids: dict[str, set[str]] = {}
    files = sorted(files if files is not None else out.glob("*.html"))
    for f in files:
        ids[f.name] = set(re.findall(r'id="([^"]+)"', f.read_text(encoding="utf-8")))
    for f in files:
        for href in HREF_RE.findall(f.read_text(encoding="utf-8")):
            href = html.unescape(href)
            parts = urlsplit(href)
            if parts.scheme or parts.netloc or href.startswith("mailto:"):
                continue
            target = parts.path or f.name
            if target not in ids:
                errors.append(f"{f.name} : lien `{href}` vers un fichier absent")
            elif parts.fragment and parts.fragment not in ids[target]:
                errors.append(f"{f.name} : ancre `{href}` introuvable")
    return errors


@app.command()
def main(out: Path = typer.Option(Path("build/site"), "--out", help="Dossier de sortie.")) -> None:
    """Génère le site statique dans --out."""
    try:
        written = build_site(out)
    except SiteError as exc:
        typer.echo(f"erreur : {exc}", err=True)
        raise typer.Exit(1) from exc
    errors = check_links(out, written)
    for err in errors:
        typer.echo(f"erreur : {err}", err=True)
    if errors:
        raise typer.Exit(1)
    typer.echo(f"✓ {len(written)} page(s) dans {out}")


if __name__ == "__main__":
    app()

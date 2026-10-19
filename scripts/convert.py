"""`convert <id>` : écrit `sources/<id>/raw.md` (ou `raw/<slug>.md` par page web).

- PDF : pymupdf4llm (mode layout désactivé), `<!-- p.N -->` au début de chaque
  page physique.
- pptx : markitdown, `<!-- p.N -->` = diapo. docx : markitdown. xlsx : un `#`
  par feuille.
- web : trafilatura depuis `original/<slug>.html` (ou playwright avec --render),
  frontmatter {url, retrieved, sha256}, ancres `<!-- #ancre -->` avant les titres.
  `--render` laisse `original/` intact (collecte et conversion séparées) : la
  page rendue est gardée dans `build/render/<id>/<slug>.html`, git-ignoré.

`redactions:` du yaml est appliqué au texte écrit (`scripts/redact.py`) ; une règle
sans effet supprime le texte brut écrit et refuse (rien de non caviardé ne reste).

N'écrase que `raw.md` / `raw/` (et `build/render/`). Passe `status` à `converted`.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Any

import typer

from scripts import redact
from scripts import registry as reg

app = typer.Typer(add_completion=False, help=__doc__)

PAGE_MARK = "<!-- p.{n} -->"
PAGE_RE = re.compile(r"^<!-- p\.(\d+) -->$", re.M)


class ConvertError(Exception):
    pass


def _tidy(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


# --------------------------------------------------------------------------- #
# PDF
# --------------------------------------------------------------------------- #

GRAPHICS_LOSS = 0.15       # perte de mots tolérée avant reprise sans graphismes
GRAPHICS_MIN_WORDS = 20    # en dessous, la page est une couverture ou un schéma


def pdf_to_markdown(path: Path) -> str:
    import pymupdf
    import pymupdf4llm

    pymupdf4llm.use_layout(False)  # le mode layout désactive la détection de titres
    parts: list[str] = []
    with pymupdf.open(path) as doc:
        chunks = pymupdf4llm.to_markdown(doc, page_chunks=True, show_progress=False)
        for i, chunk in enumerate(chunks, start=1):
            text = chunk["text"]
            expected = len(doc[i - 1].get_text().split())
            # Les graphismes vectoriels (encadrés Word, fonds colorés) masquent
            # le texte pour pymupdf4llm : si la page perd plus de GRAPHICS_LOSS
            # de ses mots, on la reprend sans graphismes (tableaux non détectés).
            if expected >= GRAPHICS_MIN_WORDS and len(text.split()) < (1 - GRAPHICS_LOSS) * expected:
                retry = pymupdf4llm.to_markdown(
                    doc, pages=[i - 1], show_progress=False,
                    ignore_graphics=True, ignore_images=True,
                )
                if len(retry.split()) > len(text.split()):
                    text = retry
            parts.append(PAGE_MARK.format(n=i) + "\n\n" + _tidy(text))
    return "\n".join(parts)


# --------------------------------------------------------------------------- #
# Office
# --------------------------------------------------------------------------- #

def _markitdown(path: Path) -> str:
    from markitdown import MarkItDown

    return MarkItDown().convert(str(path)).text_content


def pptx_to_markdown(path: Path) -> str:
    text = _markitdown(path)
    text = re.sub(r"<!-- Slide number: (\d+) -->", lambda m: PAGE_MARK.format(n=m.group(1)), text)
    return _tidy(text)


def docx_to_markdown(path: Path) -> str:
    return _tidy(_markitdown(path))


def xlsx_to_markdown(path: Path) -> str:
    text = _markitdown(path)
    text = re.sub(r"^## (.*)$", r"# \1", text, flags=re.M)  # un titre # par feuille
    return _tidy(text)


# --------------------------------------------------------------------------- #
# Web
# --------------------------------------------------------------------------- #

_ANCHOR = "@@ANC:{a}@@ "
_ANCHOR_RE = re.compile(r"^(#{1,6}) @@ANC:([^@]+)@@ ?(.*)$", re.M)


def _mark_anchors(html: str) -> str:
    """Injecte l'id des titres dans leur texte pour survivre à l'extraction."""
    from lxml import html as lh

    try:
        tree = lh.fromstring(html)
    except Exception:
        return html
    for h in tree.xpath("//h1|//h2|//h3|//h4|//h5|//h6"):
        anchor = h.get("id")
        if not anchor:
            for a in h.xpath(".//a[@id or @name]"):
                anchor = a.get("id") or a.get("name")
                break
        if not anchor:
            prev = h.getprevious()
            if prev is not None and prev.tag == "a" and (prev.get("id") or prev.get("name")) and not (prev.text or "").strip():
                anchor = prev.get("id") or prev.get("name")
        if not anchor:
            # SPA (hering.scout.ch) : l'id est sur un div parent dont ce titre
            # est le premier titre descendant.
            parent = h.getparent()
            while parent is not None and parent.tag not in ("body", "html"):
                if parent.get("id"):
                    first = parent.xpath(".//h1|.//h2|.//h3|.//h4|.//h5|.//h6")
                    if first and first[0] is h:
                        anchor = parent.get("id")
                    break
                parent = parent.getparent()
        if anchor:
            h.text = _ANCHOR.format(a=anchor) + (h.text or "")
    return lh.tostring(tree, encoding="unicode")


def html_to_markdown(html: str, url: str) -> str:
    import trafilatura

    md = trafilatura.extract(
        _mark_anchors(html), url=url, output_format="markdown",
        include_tables=True, include_links=True, include_images=False, favor_recall=True,
    )
    if not md:
        raise ConvertError(f"trafilatura n'a rien extrait de {url} (page vide ou SPA : essayer --render)")
    md = _ANCHOR_RE.sub(lambda m: f"<!-- #{m.group(2)} -->\n{m.group(1)} {m.group(3)}", md)
    return _tidy(md)


def render_html(url: str) -> str:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise ConvertError("playwright absent : installer avec `just install-web`")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Corpus français : les SPA qui choisissent la langue côté client (cudeschin) suivent la locale.
        page = browser.new_page(locale="fr-CH", extra_http_headers={"Accept-Language": "fr-CH,fr;q=0.9"})
        page.goto(url, wait_until="networkidle", timeout=60_000)
        page.wait_for_timeout(1_000)
        html = page.content()
        browser.close()
    return html


def render_path(source_id: str, slug: str) -> Path:
    """Copie de travail d'une page rendue : `build/render/<id>/<slug>.html`."""
    return reg.ROOT / "build" / "render" / source_id / f"{slug}.html"


def convert_web(data: dict[str, Any], sdir: Path, render: bool) -> list[Path]:
    import yaml

    raw_dir = sdir / "raw"
    if raw_dir.exists():
        shutil.rmtree(raw_dir)
    raw_dir.mkdir()
    written: list[Path] = []
    for page in data.get("web_pages") or []:
        html_path = sdir / "original" / f"{page['slug']}.html"
        if render:
            # L'original collecté n'est jamais touché : le rendu va dans build/ (git-ignoré).
            html = render_html(page["url"])
            rendered = render_path(data["id"], page["slug"])
            rendered.parent.mkdir(parents=True, exist_ok=True)
            rendered.write_text(html, encoding="utf-8")
        else:
            if not html_path.exists():
                raise ConvertError(f"{html_path} manquant")
            html = html_path.read_text(encoding="utf-8", errors="replace")
        body = html_to_markdown(html, page["url"])
        front = {"url": page["url"], "retrieved": data.get("retrieved"), "sha256": reg.sha256_bytes(body.encode())}
        out = raw_dir / f"{page['slug']}.md"
        out.write_text("---\n" + yaml.safe_dump(front, sort_keys=False, allow_unicode=True) + "---\n\n" + body, encoding="utf-8")
        written.append(out)
    return written


# --------------------------------------------------------------------------- #
# Commande
# --------------------------------------------------------------------------- #

CONVERTERS = {"pdf": pdf_to_markdown, "pptx": pptx_to_markdown, "docx": docx_to_markdown, "xlsx": xlsx_to_markdown}


def convert(source_id: str, render: bool = False) -> list[Path]:
    data = reg.load_source(source_id)
    sdir = reg.source_dir(source_id)
    extraction = data.get("extraction", "text")
    if extraction in ("catalogue", "none"):
        raise ConvertError(f"{source_id}: extraction `{extraction}`, rien à convertir")
    stype = data.get("type")
    if stype == "web":
        written = convert_web(data, sdir, render)
    elif stype == "image":
        raise ConvertError(f"{source_id}: type image, extraction différée (vision)")
    elif stype in CONVERTERS:
        files = [p for p in reg.original_files(source_id) if p.is_file()]
        if not files:
            raise ConvertError(f"{source_id}: aucun fichier dans original/")
        if len(files) > 1:
            raise ConvertError(f"{source_id}: plusieurs fichiers dans original/, une seule version attendue")
        text = CONVERTERS[stype](files[0])
        out = sdir / "raw.md"
        out.write_text(text, encoding="utf-8")
        written = [out]
    else:
        raise ConvertError(f"{source_id}: type `{stype}` inconnu")
    try:
        redact.redact_raw(source_id)
    except redact.RedactError as exc:
        for w in written:
            w.unlink()
        raise ConvertError(f"{exc} ; texte brut supprimé")
    if data.get("status") in ("collected", "triaged", "converted"):
        data["status"] = "converted"
        reg.save_source(data)
    return written


@app.command()
def main(
    id: str = typer.Argument(..., help="Identifiant de la source."),
    render: bool = typer.Option(False, "--render", help="Web : rendre la page avec playwright (SPA)."),
) -> None:
    """Convertit l'original en markdown brut (`raw.md`)."""
    try:
        written = convert(id, render=render)
    except (ConvertError, FileNotFoundError) as exc:
        typer.echo(f"refusé : {exc}", err=True)
        raise typer.Exit(1)
    for w in written:
        typer.echo(f"✓ {w.relative_to(reg.ROOT)}")


if __name__ == "__main__":
    app()

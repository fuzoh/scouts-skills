"""`ingest` : fait entrer un fichier, un dossier d'images, une page web ou un lot
dans `sources/<id>/` à l'état `collected`.

Formes :
  ingest <fichier> --id <id> [--title ...] [--issuer ...] [--type image]
  ingest --url <url> --id <id> [--title ...]
  ingest --batch documents/lot.yaml        (liste d'entrées, supprimé après)
  ingest --batch manifeste.yaml            (sortie de discover : pages + fichiers)
  ingest --match manifeste.yaml            (retrouve url/file_url par sha256)

Rien n'est déplacé si une entrée est refusée. L'original est déplacé, jamais
copié (sauf dossier d'images et téléchargements).
"""

from __future__ import annotations

import re
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import typer
import yaml

from scripts import referentiels as refs
from scripts import registry as reg

app = typer.Typer(add_completion=False, help=__doc__)

USER_AGENT = "skills-scoutisme-ingest/0.1"


class IngestError(Exception):
    """Refus d'ingestion : rien n'a été écrit."""


@dataclass
class Entry:
    """Une source à créer, déjà résolue (fichier local ou pages web)."""

    id: str
    type: str
    path: Path | None = None            # fichier ou dossier local (None pour web)
    file_url: str = ""
    url: str = ""
    title: str = ""
    issuer: str = ""
    ref: str = ""
    version: str = ""
    published: date | None = None
    audience: list[str] = field(default_factory=list)
    themes: list[str] = field(default_factory=list)
    web_pages: list[dict[str, Any]] = field(default_factory=list)   # {url, title, slug, html}
    sha256: str = ""
    pages: int = 0
    new_version: bool = False
    cleanup: Path | None = None         # dossier temporaire à supprimer après


# --------------------------------------------------------------------------- #
# Résolution et contrôle
# --------------------------------------------------------------------------- #

def _parse_date(value: Any) -> date | None:
    if value in (None, "", "null"):
        return None
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def _as_list(value: Any) -> list[str]:
    if value in (None, ""):
        return []
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    return list(value)


def prepare_local(entry: Entry) -> None:
    """Calcule type, sha256 et pages d'une entrée locale."""
    assert entry.path is not None
    path = entry.path
    if not path.exists():
        raise IngestError(f"{entry.id}: fichier introuvable `{path}`")
    if not entry.type:
        entry.type = reg.guess_type(path) or ""
    if not entry.type:
        raise IngestError(f"{entry.id}: type inconnu pour `{path.name}` (préciser --type)")
    if entry.type == "web":
        raise IngestError(f"{entry.id}: un fichier html s'ingère avec --url")
    if path.is_dir():
        if entry.type != "image":
            raise IngestError(f"{entry.id}: `{path}` est un dossier, seul `--type image` l'accepte")
        entry.sha256 = reg.sha256_dir(path)
        entry.pages = 0
    else:
        entry.sha256 = reg.sha256_file(path)
        entry.pages = reg.count_pages(path, entry.type)


def _check_entry(entry: Entry, known_shas: dict[str, str], known_ids: set[str]) -> list[str]:
    errors = reg.check_id(entry.id)
    if entry.type not in reg.TYPES:
        errors.append(f"{entry.id}: type `{entry.type}` inconnu")
    exists = reg.source_path(entry.id).exists()
    if exists and not entry.new_version:
        errors.append(f"{entry.id}: id déjà présent dans sources/ (utiliser --new-version pour remplacer)")
    if not exists and entry.new_version:
        errors.append(f"{entry.id}: --new-version mais la source n'existe pas")
    if entry.id in known_ids:
        errors.append(f"{entry.id}: id répété dans le lot")
    if entry.sha256:
        dup = reg.find_by_sha(entry.sha256)
        if dup and not (entry.new_version and dup.get("id") == entry.id and dup.get("sha256") != entry.sha256):
            errors.append(f"{entry.id}: sha256 déjà présent dans la source `{dup.get('id')}` (doublon)")
        if entry.sha256 in known_shas:
            errors.append(f"{entry.id}: même sha256 que `{known_shas[entry.sha256]}` dans le lot")
    issuer = entry.issuer or reg.issuer_of(entry.id)
    if issuer != reg.issuer_of(entry.id):
        errors.append(f"{entry.id}: issuer `{issuer}` ≠ préfixe de l'id")
    return errors


def check_entries(entries: list[Entry]) -> None:
    """Valide tout le lot avant de toucher au disque."""
    errors: list[str] = []
    shas: dict[str, str] = {}
    ids: set[str] = set()
    for e in entries:
        errors.extend(_check_entry(e, shas, ids))
        ids.add(e.id)
        if e.sha256:
            shas[e.sha256] = e.id
    if errors:
        raise IngestError("\n".join(errors))


# --------------------------------------------------------------------------- #
# Écriture
# --------------------------------------------------------------------------- #

def _history_entry(old: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": old.get("version", ""),
        "published": old.get("published"),
        "sha256": old.get("sha256", ""),
        "retired": reg.today(),
    }


def invalidate_derived(sdir: Path) -> list[str]:
    """Supprime ce qui dérive de l'ancien original : raw.md, raw/, index.md,
    NN-*.md, recovered/. Retourne les noms supprimés (jamais silencieux)."""
    removed: list[str] = []
    for path in sorted(sdir.iterdir()):
        name = path.name
        if name in ("raw.md", "raw", "index.md", "recovered") or (
            path.is_file() and re.match(r"^\d{2}-.+\.md$", name)
        ):
            removed.append(name + ("/" if path.is_dir() else ""))
            shutil.rmtree(path) if path.is_dir() else path.unlink()
    return removed


def write_source(entry: Entry) -> dict[str, Any]:
    """Crée (ou remplace avec --new-version) la source et place l'original."""
    sdir = reg.source_dir(entry.id)
    original = sdir / "original"
    today = reg.today()

    if entry.new_version:
        data = reg.load_source(entry.id)
        data.setdefault("history", [])
        data["history"].append(_history_entry(data))
        for old in reg.original_files(entry.id):
            shutil.rmtree(old) if old.is_dir() else old.unlink()
        removed = invalidate_derived(sdir)
        if removed:
            typer.echo(f"⚠ {entry.id}: nouvelle version, artefacts de l'ancienne supprimés "
                       f"(récupérables par git) : {', '.join(removed)}", err=True)
        # La fidélité décrit la conversion de l'ancien original : à réévaluer.
        data["fidelity"] = None
        data["fidelity_notes"] = ""
        to_review = [k for k in ("applies_from", "applies_until", "nature", "redactions") if data.get(k)]
        if to_review:
            typer.echo(f"⚠ {entry.id}: à revoir pour la nouvelle version : {', '.join(to_review)}", err=True)
        cited_by = refs.citing(entry.id)
        if cited_by:
            typer.echo(f"⚠ {entry.id}: référentiels à revérifier : {', '.join(cited_by)}", err=True)
    else:
        data = reg.load_template()
        data["history"] = []
        data["concepts"] = []
        data["supersedes"] = []
        data["notes"] = ""
        data["decision"] = ""
        data["rejected_reason"] = ""
        data["issuer_detail"] = ""
        data["lang"] = "fr"

    original.mkdir(parents=True, exist_ok=True)

    data["id"] = entry.id
    data["issuer"] = entry.issuer or reg.issuer_of(entry.id)
    data["type"] = entry.type
    data["status"] = "collected"
    data["extraction"] = "vision" if entry.type == "image" else "text"
    data["retrieved"] = today
    data["stale"] = False
    data["sha256"] = entry.sha256
    data["pages"] = entry.pages
    if entry.title or not entry.new_version:
        data["title"] = entry.title or _default_title(entry)
    if entry.ref or not entry.new_version:
        data["ref"] = entry.ref
    if entry.published or not entry.new_version:
        data["published"] = entry.published
    if entry.audience or not entry.new_version:
        data["audience"] = entry.audience
    if entry.themes or not entry.new_version:
        data["themes"] = entry.themes
    data["url"] = entry.url or (data.get("url") if entry.new_version else "")
    data["file_url"] = entry.file_url or (data.get("file_url") if entry.new_version else "")

    if entry.type == "web":
        data["version"] = today.isoformat()
        data["file_url"] = ""
        data["pages"] = 0
        data["web_pages"] = []
        for page in entry.web_pages:
            (original / f"{page['slug']}.html").write_bytes(page["html"])
            data["web_pages"].append({"url": page["url"], "title": page.get("title", ""), "slug": page["slug"]})
        data["url"] = entry.url or entry.web_pages[0]["url"]
    else:
        data["version"] = entry.version if (entry.version or not entry.new_version) else data.get("version", "")
        data["web_pages"] = []
        assert entry.path is not None
        if entry.path.is_dir():
            dest = original / entry.path.name
            shutil.copytree(entry.path, dest)
        else:
            dest = original / entry.path.name
            if entry.cleanup is not None:
                shutil.move(str(entry.path), dest)
            else:
                shutil.move(str(entry.path), dest)

    reg.save_source(data)
    if entry.cleanup is not None and entry.cleanup.exists():
        shutil.rmtree(entry.cleanup, ignore_errors=True)
    return data


def _default_title(entry: Entry) -> str:
    if entry.web_pages:
        return entry.web_pages[0].get("title") or entry.id
    if entry.path is not None:
        return entry.path.stem.replace("_", " ")
    return entry.id


# --------------------------------------------------------------------------- #
# Web
# --------------------------------------------------------------------------- #

def _http_client():
    import httpx

    return httpx.Client(timeout=30, follow_redirects=True, headers={"User-Agent": USER_AGENT})


def _html_title(html: bytes) -> str:
    import re

    m = re.search(rb"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    if not m:
        return ""
    import html as html_mod

    return html_mod.unescape(m.group(1).decode("utf-8", "replace")).strip()


def _page_slug(url: str, used: set[str]) -> str:
    parsed = urlparse(url)
    # SPA à routes en fragment (`#!/article/01`) : le fragment distingue les pages.
    route = parsed.path.strip("/") + ("/" + parsed.fragment.strip("!/") if parsed.fragment else "")
    base = reg.slugify(route.strip("/").replace("/", "-")) or "index"
    slug, n = base, 2
    while slug in used:
        slug, n = f"{base}-{n}", n + 1
    used.add(slug)
    return slug


def fetch_pages(urls: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Télécharge chaque page (html brut) ; retourne {url, title, slug, html}."""
    pages: list[dict[str, Any]] = []
    used: set[str] = set()
    with _http_client() as client:
        for item in urls:
            url = item["url"]
            resp = client.get(url)
            resp.raise_for_status()
            html = resp.content
            pages.append({
                "url": url,
                "title": item.get("title") or _html_title(html),
                "slug": _page_slug(url, used),
                "html": html,
            })
    return pages


def download_file(url: str, name: str, tmp: Path) -> Path:
    with _http_client() as client:
        resp = client.get(url)
        resp.raise_for_status()
        dest = tmp / (name or Path(urlparse(url).path).name or "fichier")
        dest.write_bytes(resp.content)
    return dest


# --------------------------------------------------------------------------- #
# Lots
# --------------------------------------------------------------------------- #

def entries_from_lot(items: list[dict[str, Any]], base: Path) -> list[Entry]:
    entries: list[Entry] = []
    for item in items:
        if "file" not in item or "id" not in item:
            raise IngestError(f"entrée de lot sans `file` ou `id` : {item}")
        path = Path(item["file"])
        if not path.is_absolute():
            path = (base / path) if (base / path).exists() else (reg.ROOT / path)
        e = Entry(
            id=str(item["id"]),
            type=str(item.get("type") or ""),
            path=path,
            title=str(item.get("title") or ""),
            issuer=str(item.get("issuer") or ""),
            ref=str(item.get("ref") or ""),
            version=str(item.get("version") or ""),
            published=_parse_date(item.get("published")),
            audience=_as_list(item.get("audience")),
            themes=_as_list(item.get("themes")),
            url=str(item.get("url") or ""),
            file_url=str(item.get("file_url") or ""),
            new_version=bool(item.get("new_version", False)),
        )
        prepare_local(e)
        entries.append(e)
    return entries


def entries_from_manifest(manifest: dict[str, Any]) -> list[Entry]:
    """Pages regroupées par colonne `source` → sources web ; fichiers avec `id` → sources locales."""
    entries: list[Entry] = []
    groups: dict[str, list[dict[str, Any]]] = {}
    for page in manifest.get("pages") or []:
        sid = str(page.get("source") or "").strip()
        if sid:
            groups.setdefault(sid, []).append(page)
    for sid, pages in groups.items():
        fetched = fetch_pages(pages)
        e = Entry(id=sid, type="web", web_pages=fetched, url=fetched[0]["url"],
                  title=fetched[0]["title"])
        e.sha256 = reg.sha256_bytes(b"".join(p["html"] for p in fetched))
        entries.append(e)
    for f in manifest.get("files") or []:
        sid = str(f.get("id") or "").strip()
        if not sid:
            continue
        tmp = Path(tempfile.mkdtemp(prefix="ingest-"))
        path = download_file(f["url"], f.get("name", ""), tmp)
        e = Entry(id=sid, type=str(f.get("type") or ""), path=path, file_url=f["url"],
                  url=str(f.get("found_on") or f.get("url")), title=str(f.get("title") or ""),
                  cleanup=tmp)
        prepare_local(e)
        if f.get("sha256") and f["sha256"] != e.sha256:
            typer.echo(f"⚠ {sid}: sha256 téléchargé ≠ manifeste (le fichier a changé)", err=True)
        entries.append(e)
    return entries


def match_manifest(manifest: dict[str, Any]) -> list[str]:
    """Remplit url/file_url des sources dont le sha256 est dans le manifeste ; `stale` si seul le nom correspond."""
    report: list[str] = []
    sources = reg.all_sources()
    by_sha = {s.get("sha256"): s for s in sources if s.get("sha256")}
    by_name: dict[str, dict[str, Any]] = {}
    for s in sources:
        for p in reg.original_files(s["id"]):
            by_name[p.name] = s
    for f in manifest.get("files") or []:
        src = by_sha.get(f.get("sha256"))
        if src:
            src["file_url"] = f["url"]
            if not src.get("url") or src["url"].startswith("https://pfadi.swiss/..."):
                src["url"] = f.get("found_on") or f["url"]
            src["stale"] = False
            reg.save_source(src)
            report.append(f"✓ {src['id']}: file_url = {f['url']}")
            continue
        src = by_name.get(f.get("name", ""))
        if src:
            src["stale"] = True
            src["file_url"] = src.get("file_url") or f["url"]
            reg.save_source(src)
            report.append(f"⚠ {src['id']}: même nom `{f['name']}` mais sha256 différent → stale: true")
    return report


# --------------------------------------------------------------------------- #
# Commande
# --------------------------------------------------------------------------- #

def run(entries: list[Entry]) -> list[dict[str, Any]]:
    """Contrôle puis écrit toutes les entrées. Lève IngestError sans rien écrire."""
    try:
        check_entries(entries)
    except IngestError:
        for e in entries:
            if e.cleanup is not None:
                shutil.rmtree(e.cleanup, ignore_errors=True)
        raise
    return [write_source(e) for e in entries]


@app.command()
def main(
    file: Path | None = typer.Argument(None, help="Fichier ou dossier (--type image) à ingérer."),
    id: str | None = typer.Option(None, "--id", help="Identifiant `<issuer>-<slug>`."),
    title: str = typer.Option("", help="Titre."),
    issuer: str = typer.Option("", help="Émetteur, déduit du préfixe de l'id sinon."),
    ref: str = typer.Option("", help="Numéro officiel (ex. 314201fr)."),
    version: str = typer.Option("", help="Version telle qu'écrite par l'éditeur."),
    published: str = typer.Option("", help="Date du document (AAAA-MM-JJ)."),
    audience: str = typer.Option("", help="Publics, séparés par des virgules."),
    themes: str = typer.Option("", help="Thèmes, séparés par des virgules."),
    type_: str = typer.Option("", "--type", help="pdf | docx | xlsx | pptx | image ; déduit de l'extension sinon."),
    url: str | None = typer.Option(None, "--url", help="Page web à ingérer comme source `web`."),
    batch: Path | None = typer.Option(None, "--batch", help="Lot (liste) ou manifeste de discover."),
    match: Path | None = typer.Option(None, "--match", help="Manifeste : retrouver url/file_url par sha256."),
    new_version: bool = typer.Option(False, "--new-version", help="Remplacer une source existante : ancienne version dans history, raw, index, sections et recovered/ supprimés."),
) -> None:
    """Fait entrer une source dans `sources/<id>/` à l'état `collected`."""
    try:
        if match is not None:
            data = yaml.safe_load(match.read_text(encoding="utf-8")) or {}
            for line in match_manifest(data):
                typer.echo(line)
            return

        if batch is not None:
            data = yaml.safe_load(batch.read_text(encoding="utf-8"))
            if isinstance(data, list):
                entries = entries_from_lot(data, batch.parent)
                created = run(entries)
                batch.unlink()
                typer.echo(f"lot `{batch}` supprimé")
            elif isinstance(data, dict) and ("pages" in data or "files" in data):
                created = run(entries_from_manifest(data))
            else:
                raise IngestError(f"`{batch}` : ni liste d'entrées, ni manifeste")
        elif url is not None:
            if not id:
                raise IngestError("--url exige --id")
            pages = fetch_pages([{"url": url, "title": title}])
            e = Entry(id=id, type="web", web_pages=pages, url=url, title=title or pages[0]["title"],
                      issuer=issuer, audience=_as_list(audience), themes=_as_list(themes),
                      new_version=new_version)
            e.sha256 = reg.sha256_bytes(pages[0]["html"])
            created = run([e])
        elif file is not None:
            if not id:
                raise IngestError("préciser --id (ou utiliser --batch)")
            e = Entry(id=id, type=type_, path=file, title=title, issuer=issuer, ref=ref, version=version,
                      published=_parse_date(published), audience=_as_list(audience),
                      themes=_as_list(themes), new_version=new_version)
            prepare_local(e)
            created = run([e])
        else:
            raise IngestError("rien à ingérer : fichier, --url, --batch ou --match")
    except IngestError as exc:
        typer.echo(f"refusé :\n{exc}", err=True)
        raise typer.Exit(1)
    except Exception as exc:  # réseau, yaml, fichiers
        typer.echo(f"erreur : {exc}", err=True)
        raise typer.Exit(1)

    for d in created:
        typer.echo(f"✓ {d['id']} ({d['type']}, {d['pages']} p.) → sources/{d['id']}/ [collected]")


if __name__ == "__main__":
    app()

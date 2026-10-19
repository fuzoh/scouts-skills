"""Découverte des pages et fichiers d'un site (même hôte) vers un manifeste yaml.

`discover` ne crée jamais de source et ne touche pas à `sources/` : il écrit
seulement un manifeste que l'humain complète (colonnes `source` et `id`) avant
`ingest --batch manifeste.yaml`.
"""

from __future__ import annotations

import hashlib
import posixpath
import re
import sys
import time
from collections import deque
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urldefrag, urljoin, urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser

import httpx
import lxml.etree
import lxml.html
import typer
import yaml

USER_AGENT = "skills-scoutisme-discover/0.1"
TIMEOUT = 20.0
RENDER_TIMEOUT_MS = 30_000
FILE_EXTENSIONS = {"pdf", "docx", "xlsx", "pptx", "doc", "xls", "ppt", "zip"}

app = typer.Typer(
    add_completion=False,
    help="Parcourt un site (même hôte) et écrit un manifeste yaml des pages et fichiers.",
)


class RenderIndisponible(RuntimeError):
    """Playwright n'est pas installé ou ne peut pas démarrer."""


def warn(message: str) -> None:
    typer.echo(f"Avertissement : {message}", err=True)


def normalize_url(url: str) -> str:
    """URL sans fragment, schéma et hôte en minuscules, sans slash final (sauf racine)."""
    url, _ = urldefrag(url.strip())
    parts = urlsplit(url)
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, parts.query, ""))


def has_file_extension(url: str) -> bool:
    ext = posixpath.splitext(urlsplit(url).path)[1].lstrip(".").lower()
    return ext in FILE_EXTENSIONS


def file_name(url: str) -> str:
    return posixpath.basename(unquote(urlsplit(url).path)) or "fichier"


def parse_html(html: str, base_url: str) -> tuple[str, list[str]]:
    """Retourne (titre, liens absolus) d'une page HTML."""
    try:
        try:
            doc = lxml.html.document_fromstring(html)
        except ValueError:  # déclaration d'encodage dans une chaîne str
            doc = lxml.html.document_fromstring(html.encode("utf-8"))
    except (lxml.etree.ParserError, lxml.etree.XMLSyntaxError):
        return "", []
    title = (doc.findtext(".//title") or "").strip()
    if not title:
        h1 = doc.find(".//h1")
        title = h1.text_content().strip() if h1 is not None else ""
    title = re.sub(r"\s+", " ", title)
    links = []
    for href in doc.xpath("//a[@href]/@href"):
        href = href.strip()
        if href:
            links.append(urljoin(base_url, href))
    return title, links


class Fetcher:
    """Requêtes httpx espacées dans le temps, soumises à robots.txt."""

    def __init__(self, root: str, delay: float, client: httpx.Client):
        self.client = client
        self.robots = RobotFileParser()
        self._load_robots(root)
        crawl_delay = self.robots.crawl_delay(USER_AGENT)
        self.interval = max(delay, float(crawl_delay or 0))
        self._last = 0.0

    def _load_robots(self, root: str) -> None:
        parts = urlsplit(root)
        robots_url = urlunsplit((parts.scheme, parts.netloc, "/robots.txt", "", ""))
        try:
            resp = self.client.get(robots_url)
        except httpx.HTTPError as exc:
            warn(f"robots.txt illisible ({exc}) ; tout est autorisé.")
            self.robots.parse([])
            return
        if resp.status_code in (401, 403):
            self.robots.disallow_all = True
        elif resp.status_code >= 400:
            self.robots.parse([])
        else:
            self.robots.parse(resp.text.splitlines())

    def allowed(self, url: str) -> bool:
        return self.robots.can_fetch(USER_AGENT, url)

    def _throttle(self) -> None:
        wait = self._last + self.interval - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        self._last = time.monotonic()

    def get(self, url: str, read_html_body: bool = True) -> dict:
        """Télécharge `url` en mémoire.

        Retourne {final_url, html: str|None, size, sha256}. `html` est None si le
        contenu n'est pas du HTML (le hash et la taille sont alors calculés) ou si
        `read_html_body` est faux.
        """
        self._throttle()
        with self.client.stream("GET", url) as resp:
            resp.raise_for_status()
            final_url = str(resp.url)
            ctype = resp.headers.get("content-type", "").split(";")[0].strip().lower()
            if ctype == "text/html" and not has_file_extension(final_url):
                html = None
                if read_html_body:
                    resp.read()
                    html = resp.text
                return {"final_url": final_url, "html": html, "is_html": True}
            digest = hashlib.sha256()
            size = 0
            for chunk in resp.iter_bytes():
                digest.update(chunk)
                size += len(chunk)
            return {
                "final_url": final_url,
                "html": None,
                "is_html": False,
                "size": size,
                "sha256": digest.hexdigest(),
            }


def _open_renderer():
    """Ouvre playwright ; retourne (contexte, navigateur, page)."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RenderIndisponible(
            "playwright n'est pas installé : installer avec `just install-web`."
        ) from exc
    pw = sync_playwright().start()
    try:
        browser = pw.chromium.launch()
    except Exception as exc:  # navigateur absent, etc.
        pw.stop()
        raise RenderIndisponible(
            f"playwright ne démarre pas ({exc}) : installer avec `just install-web`."
        ) from exc
    page = browser.new_page(user_agent=USER_AGENT, locale="fr-CH",
                            extra_http_headers={"Accept-Language": "fr-CH,fr;q=0.9"})
    page.set_default_timeout(RENDER_TIMEOUT_MS)
    return pw, browser, page


def crawl(
    root: str,
    depth: int = 1,
    render: bool = False,
    delay: float = 1.0,
    max_pages: int = 500,
) -> dict:
    """Parcours en largeur du même hôte ; retourne le manifeste sous forme de dict.

    Profondeur 0 = la page de départ seule. Les erreurs réseau sont signalées sur
    stderr et le parcours continue.
    """
    root = normalize_url(root)
    host = urlsplit(root).netloc
    renderer = _open_renderer() if render else None  # échoue tôt si indisponible
    pages: list[dict] = []
    files: dict[str, dict] = {}
    seen = {root}
    queue = deque([(root, 0, "")])
    limit_warned = False

    try:
        with httpx.Client(
            headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT, follow_redirects=True
        ) as client:
            fetcher = Fetcher(root, delay, client)
            while queue:
                url, level, found_on = queue.popleft()
                if not fetcher.allowed(url):
                    warn(f"{url} interdit par robots.txt, ignoré.")
                    continue
                if url in files:
                    continue
                is_file = has_file_extension(url)
                if not is_file and len(pages) >= max_pages:
                    if not limit_warned:
                        warn(f"limite de {max_pages} pages atteinte, parcours tronqué.")
                        limit_warned = True
                    continue
                try:
                    result = fetcher.get(url, read_html_body=renderer is None)
                except httpx.HTTPError as exc:
                    warn(f"{url} : {exc}")
                    continue
                final_url = normalize_url(result["final_url"])
                if urlsplit(final_url).netloc != host:
                    continue  # redirection hors hôte
                seen.add(final_url)

                if not result["is_html"]:
                    if final_url in files or url in files:
                        continue
                    # Un lien qui redirige vers le fichier (page de détail d'un catalogue)
                    # est la page d'origine canonique : `url` = fichier final, `found_on` = ce lien.
                    files[final_url] = {
                        "url": final_url,
                        "name": file_name(final_url),
                        "size": result["size"],
                        "sha256": result["sha256"],
                        "found_on": url if url != final_url else found_on,
                        "id": "",
                    }
                    continue

                html = result["html"]
                if renderer is not None:
                    try:
                        page = renderer[2]
                        page.goto(final_url, wait_until="networkidle")
                        html = page.content()
                    except Exception as exc:
                        warn(f"{url} : rendu impossible ({exc})")
                        continue
                title, links = parse_html(html, final_url)
                pages.append({"url": url, "title": title, "source": ""})

                # À la profondeur maximale, on ne garde que les liens vers des fichiers.
                for link in links:
                    if urlsplit(link).scheme not in ("http", "https"):
                        continue
                    link = normalize_url(link)
                    if urlsplit(link).netloc != host or link in seen:
                        continue
                    if level >= depth and not has_file_extension(link):
                        continue
                    seen.add(link)
                    queue.append((link, level + 1, url))
    finally:
        if renderer is not None:
            renderer[1].close()
            renderer[0].stop()

    return {
        "root": root,
        "retrieved": date.today().isoformat(),
        "pages": pages,
        "files": list(files.values()),
    }


def write_manifest(data: dict, path: Path) -> None:
    path = Path(path)
    with path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(data, fh, allow_unicode=True, sort_keys=False)


@app.command()
def discover(
    url: str = typer.Argument(..., help="URL de départ (le parcours reste sur le même hôte)."),
    depth: int = typer.Option(1, "--depth", min=0, help="Profondeur du parcours (0 = page de départ seule)."),
    render: bool = typer.Option(False, "--render", help="Rendre les pages avec playwright (sites SPA)."),
    out: Path = typer.Option(Path("manifeste.yaml"), "--out", help="Fichier manifeste à écrire."),
    delay: float = typer.Option(1.0, "--delay", min=0.0, help="Délai minimum entre deux requêtes, en secondes (au moins le Crawl-delay de robots.txt)."),
    max_pages: int = typer.Option(500, "--max-pages", min=1, help="Nombre maximal de pages à parcourir."),
) -> None:
    """Parcourt un site et écrit un manifeste yaml (pages, fichiers) pour `ingest --batch`."""
    if urlsplit(url).scheme not in ("http", "https") or not urlsplit(url).netloc:
        typer.echo(f"URL invalide : {url}", err=True)
        raise typer.Exit(1)
    try:
        data = crawl(url, depth=depth, render=render, delay=delay, max_pages=max_pages)
    except RenderIndisponible as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1)
    write_manifest(data, out)
    typer.echo(
        f"{len(data['pages'])} page(s), {len(data['files'])} fichier(s) → {out}"
    )


if __name__ == "__main__":
    app()

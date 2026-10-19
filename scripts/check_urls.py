"""Veille des sources : compare le registre aux URL publiées.

`check-urls` parcourt `sources/*/source.yaml` (hors `rejected` et `superseded`) et
vérifie, poliment, chaque `file_url`, `url` et `web_pages[].url` :

- `ok`       : l'URL répond et rien n'a visiblement changé ;
- `change`   : fichier dont le sha256 distant diffère de `sha256` du registre
               (ou, si le fichier est trop gros pour être téléchargé, dont
               `Last-Modified` est postérieur à `retrieved`) ;
- `redirige` : l'URL finale diffère de l'URL du registre ;
- `mort`     : 4xx/5xx ou erreur réseau après 2 essais ;
- `ignore`   : non vérifiée, `robots.txt` l'interdit.

Les pages web ne sont jamais comparées au sha256 du registre (html trop instable) :
seuls leur état (vivante, redirigée, morte) et `Last-Modified` sont relevés.

Le script ne modifie jamais le registre ni aucun fichier versionné : `stale: true`
reste posé à la main après une ré-ingestion locale (METHODE.md, « Versions et mise
à jour »). Code de sortie 0 même s'il y a des changements (le workflow décide), 2
sur erreur d'usage.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from email.utils import parsedate_to_datetime
from enum import Enum
from pathlib import Path
from urllib.parse import urldefrag, urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser

import httpx
import typer

from scripts import registry as reg
from scripts.discover import TIMEOUT, normalize_url, warn

USER_AGENT = "scouts-skills-veille (+https://github.com/fuzoh/scouts-skills)"
ROBOTS_TOKEN = "scouts-skills-veille"  # jeton d'agent cherché dans robots.txt
ATTEMPTS = 2
DEFAULT_DELAY = 1.0
DEFAULT_MAX_MB = 50
# Une issue GitHub accepte 65 536 caractères ; marge pour la note de troncature.
DEFAULT_MAX_CHARS = 60_000
SKIPPED_STATUSES = ("rejected", "superseded")
CATEGORIES = ("change", "mort", "redirige", "ignore", "ok")
CATEGORY_TITLES = {
    "change": "Changés",
    "mort": "Morts",
    "redirige": "Redirigés",
    "ignore": "Non vérifiés (robots.txt)",
    "ok": "Sans changement",
}

app = typer.Typer(
    add_completion=False,
    help="Compare le registre aux URL publiées (changées, mortes, redirigées). Ne modifie rien.",
)


class Format(str, Enum):
    md = "md"
    json = "json"


@dataclass
class Target:
    """Une URL à vérifier, rattachée à une source du registre."""

    id: str
    title: str
    url: str
    kind: str  # file | page | web_page
    sha256: str = ""
    retrieved: date | None = None
    # autres URL de la même source : une redirection vers l'une d'elles est attendue
    # (page de détail d'un catalogue qui redirige vers le fichier)
    siblings: tuple[str, ...] = ()


@dataclass
class Result:
    id: str
    title: str
    url: str
    kind: str
    category: str
    detail: str = ""
    status: int | None = None
    final_url: str = ""
    redirects: list[str] = field(default_factory=list)
    sha256_distant: str = ""
    last_modified: str = ""
    etag: str = ""


@dataclass
class Probe:
    """Réponse brute à une requête (ou erreur)."""

    status: int = 0
    final_url: str = ""
    redirects: list[str] = field(default_factory=list)
    error: str = ""
    sha256: str = ""
    size: int | None = None  # octets lus si téléchargé
    oversize: bool = False  # trop gros : non téléchargé
    content_length: int | None = None
    last_modified: str = ""
    etag: str = ""


# --- Cibles ---------------------------------------------------------------


def _url(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def _as_date(value: object) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


def checkable(sources: list[dict]) -> list[dict]:
    """Sources à vérifier : ni `rejected` ni `superseded`."""
    return [s for s in sources if s.get("status") not in SKIPPED_STATUSES]


def targets_of(source: dict) -> list[Target]:
    """URL d'une source : `file_url`, `url`, puis chaque `web_pages[].url` (sans doublon)."""
    sid = source.get("id", "")
    title = str(source.get("title") or sid)
    retrieved = _as_date(source.get("retrieved"))
    out: list[Target] = []
    seen: set[str] = set()

    def add(url: str, kind: str, label: str, sha: str = "") -> None:
        if url and url not in seen:
            seen.add(url)
            out.append(Target(sid, label, url, kind, sha, retrieved))

    add(_url(source.get("file_url")), "file", title, str(source.get("sha256") or ""))
    add(_url(source.get("url")), "page", title)
    for page in source.get("web_pages") or []:
        if isinstance(page, dict):
            page_title = str(page.get("title") or "").strip()
            add(_url(page.get("url")), "web_page", f"{title} : {page_title}" if page_title else title)
    siblings = tuple(t.url for t in out)
    for t in out:
        t.siblings = siblings
    return out


# --- Politesse ------------------------------------------------------------


class Gate:
    """robots.txt et espacement des requêtes, par hôte."""

    def __init__(self, client: httpx.Client, delay: float):
        self.client = client
        self.delay = delay
        self._robots: dict[str, RobotFileParser] = {}
        self._last: dict[str, float] = {}

    def wait(self, host: str, extra: float = 0.0) -> None:
        """Bloque jusqu'à ce que `delay` (ou `extra`, Crawl-delay) se soit écoulé pour `host`."""
        interval = max(self.delay, extra)
        wait = self._last.get(host, 0.0) + interval - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        self._last[host] = time.monotonic()

    def _load(self, url: str) -> RobotFileParser:
        parts = urlsplit(url)
        host = parts.netloc.lower()
        if host in self._robots:
            return self._robots[host]
        parser = RobotFileParser()
        robots_url = urlunsplit((parts.scheme, parts.netloc, "/robots.txt", "", ""))
        self.wait(host)
        try:
            resp = self.client.get(robots_url)
        except (httpx.HTTPError, httpx.InvalidURL) as exc:
            warn(f"robots.txt illisible pour {host} ({exc}) ; tout est autorisé.")
            parser.parse([])
        else:
            if resp.status_code in (401, 403):
                parser.disallow_all = True
            elif resp.status_code >= 400:
                parser.parse([])
            else:
                parser.parse(resp.text.splitlines())
        self._robots[host] = parser
        return parser

    def allowed(self, url: str) -> bool:
        return self._load(url).can_fetch(ROBOTS_TOKEN, url)

    def pause(self, url: str) -> None:
        host = urlsplit(url).netloc.lower()
        crawl_delay = self._load(url).crawl_delay(ROBOTS_TOKEN)
        self.wait(host, float(crawl_delay or 0))


def make_client() -> httpx.Client:
    return httpx.Client(headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT, follow_redirects=True)


# --- Requêtes -------------------------------------------------------------


class Checker:
    def __init__(self, client: httpx.Client, delay: float = DEFAULT_DELAY, max_mb: float = DEFAULT_MAX_MB):
        self.gate = Gate(client, delay)
        self.client = client
        self.max_bytes = int(max_mb * 1024 * 1024)
        self._cache: dict[tuple[str, bool], Probe | None] = {}

    def _probe(self, method: str, url: str, download: bool = False) -> Probe:
        """Une requête, redirections suivies ; `download` hache le corps (jusqu'à `max_bytes`)."""
        self.gate.pause(url)
        probe = Probe()
        try:
            with self.client.stream(method, url) as resp:
                probe.status = resp.status_code
                probe.final_url = str(resp.url)
                probe.redirects = [str(r.url) for r in resp.history]
                headers = resp.headers
                probe.last_modified = headers.get("last-modified", "")
                probe.etag = headers.get("etag", "")
                try:
                    probe.content_length = int(headers["content-length"])
                except (KeyError, ValueError):
                    pass
                if download and resp.status_code < 400:
                    if probe.content_length is not None and probe.content_length > self.max_bytes:
                        probe.oversize = True
                        return probe
                    digest = hashlib.sha256()
                    size = 0
                    for chunk in resp.iter_bytes():
                        size += len(chunk)
                        if size > self.max_bytes:
                            probe.oversize = True
                            return probe
                        digest.update(chunk)
                    probe.size = size
                    probe.sha256 = digest.hexdigest()
        except (httpx.HTTPError, httpx.InvalidURL) as exc:
            probe.error = f"{type(exc).__name__}: {exc}".strip(": ")
        return probe

    def _once(self, target: Target) -> Probe:
        if target.kind == "file":
            return self._probe("GET", target.url, download=True)  # le GET sert aussi à hacher
        probe = self._probe("HEAD", target.url)
        if probe.error or probe.status >= 400:  # HEAD refusé ou mal géré : GET sans lire le corps
            probe = self._probe("GET", target.url)
        return probe

    def _fetch(self, target: Target) -> Probe:
        probe = Probe()
        for _ in range(ATTEMPTS):
            probe = self._once(target)
            if not probe.error and probe.status < 500 and probe.status != 429:
                break
        return probe

    def check(self, target: Target) -> Result:
        res = Result(target.id, target.title, target.url, target.kind, "ok")
        scheme = urlsplit(target.url).scheme.lower()
        if scheme not in ("http", "https") or not urlsplit(target.url).netloc:
            res.category, res.detail = "mort", "URL invalide (ni http ni https)"
            return res
        try:
            allowed = self.gate.allowed(target.url)
        except (ValueError, httpx.InvalidURL) as exc:
            res.category, res.detail = "mort", f"URL invalide : {exc}"
            return res
        if not allowed:
            res.category, res.detail = "ignore", "interdit par robots.txt"
            return res

        # Un même fichier ou une même page (ex. SPA à fragments) n'est requêté qu'une fois.
        key = (urldefrag(target.url)[0], target.kind == "file")
        probe = self._cache.get(key) or self._fetch(target)
        self._cache[key] = probe
        return classify(target, probe, res)


def classify(target: Target, probe: Probe, res: Result) -> Result:
    res.status = probe.status or None
    res.final_url = probe.final_url
    res.redirects = probe.redirects
    res.last_modified = probe.last_modified
    res.etag = probe.etag
    res.sha256_distant = probe.sha256

    if probe.error:
        res.category = "mort"
        res.detail = f"erreur réseau après {ATTEMPTS} essais : {probe.error}"
        return res
    if probe.status >= 400:
        res.category = "mort"
        res.detail = f"HTTP {probe.status}"
        return res

    notes: list[str] = []
    if target.kind == "file":
        if probe.oversize:
            size = f"{probe.content_length} octets" if probe.content_length else "taille inconnue"
            notes.append(f"non téléchargé ({size} > max), sha256 non vérifié")
            if _modified_since(probe.last_modified, target.retrieved):
                res.category = "change"
                notes.append(f"Last-Modified {probe.last_modified} postérieur à la collecte ({target.retrieved})")
        elif not target.sha256:
            notes.append("sha256 du registre vide, non comparé")
        elif probe.sha256 != target.sha256:
            res.category = "change"
            notes.append(f"sha256 distant {probe.sha256[:12]}… ≠ registre {target.sha256[:12]}…")
        if probe.last_modified and res.category != "change":
            notes.append(f"Last-Modified {probe.last_modified}")
    elif probe.last_modified:
        notes.append(f"Last-Modified {probe.last_modified}")

    if probe.final_url and normalize_url(probe.final_url) != normalize_url(target.url):
        expected = normalize_url(probe.final_url) in {normalize_url(u) for u in target.siblings}
        if expected:
            notes.insert(0, "redirige vers une autre URL de la source (attendu)")
        else:
            if res.category == "ok":
                res.category = "redirige"
            notes.insert(0, f"redirigé vers {probe.final_url} (HTTP {probe.status})")
    res.detail = " ; ".join(notes)
    return res


def _modified_since(last_modified: str, retrieved: date | None) -> bool:
    if not last_modified or retrieved is None:
        return False
    try:
        return parsedate_to_datetime(last_modified).date() > retrieved
    except (TypeError, ValueError):
        return False


# --- Rapport --------------------------------------------------------------


def run_checks(targets: list[Target], checker: Checker) -> list[Result]:
    return [checker.check(t) for t in targets]


def counts(results: list[Result]) -> dict[str, int]:
    return {c: sum(1 for r in results if r.category == c) for c in CATEGORIES}


def _cell(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


def render_md(results: list[Result], without_url: int, day: date, max_chars: int = 0) -> str:
    """Rapport markdown ; `max_chars` > 0 tronque proprement les tableaux (note finale)."""
    n = counts(results)
    head = [
        "# Veille des sources",
        "",
        f"Date : {day.isoformat()}. URL vérifiées : {len(results)}.",
        "",
        "| Catégorie | Nombre |",
        "|---|---|",
    ]
    head += [f"| {CATEGORY_TITLES[c]} | {n[c]} |" for c in CATEGORIES]
    head += ["", f"Sources sans aucune URL (non vérifiables) : {without_url}.", ""]
    head += [
        "Le rapport ne modifie pas le registre. Pour un changement : ré-ingérer en local "
        "(`ingest --new-version`, METHODE.md) puis poser `stale: true` à la main si besoin.",
        "",
    ]

    lines = list(head)
    for cat in CATEGORIES[:-1]:  # `ok` : compteur seulement
        rows = [r for r in results if r.category == cat]
        if not rows:
            continue
        lines += [f"## {CATEGORY_TITLES[cat]} ({len(rows)})", "", "| Id | Titre | URL | Détail |", "|---|---|---|---|"]
        lines += [f"| `{r.id}` | {_cell(r.title)} | {_cell(r.url)} | {_cell(r.detail)} |" for r in rows]
        lines.append("")

    if max_chars <= 0:
        return "\n".join(lines) + "\n"

    # Troncature par lignes entières, en gardant la place de la note finale.
    budget = max_chars - 300
    kept: list[str] = []
    omitted = 0
    for line in lines:
        budget -= len(line) + 1
        if budget < 0 and line.startswith("| `"):
            omitted += 1
        else:
            kept.append(line)
    if omitted:
        kept += [
            f"> Rapport tronqué : {omitted} ligne(s) omise(s) pour rester sous la limite d'une issue. "
            "Relancer `just check-urls --format json` en local pour le détail complet.",
            "",
        ]
    return "\n".join(kept) + "\n"


def render_json(results: list[Result], without_url: int, day: date) -> str:
    data = {
        "date": day.isoformat(),
        "compteurs": counts(results),
        "verifiees": len(results),
        "sans_url": without_url,
        "resultats": [asdict(r) for r in results],
    }
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


# --- CLI ------------------------------------------------------------------


@app.command()
def check_urls(
    format: Format = typer.Option(Format.md, "--format", help="Format du rapport : md ou json."),
    out: Path | None = typer.Option(None, "--out", help="Fichier de sortie (défaut : sortie standard)."),
    only: str | None = typer.Option(None, "--only", help="Vérifier une seule source (id)."),
    limit: int | None = typer.Option(None, "--limit", min=1, help="Ne vérifier que les N premières URL (essai)."),
    delay: float = typer.Option(DEFAULT_DELAY, "--delay", min=0.0, help="Délai minimum entre deux requêtes sur un même hôte, en secondes."),
    max_mb: float = typer.Option(DEFAULT_MAX_MB, "--max-mb", min=0.1, help="Taille maximale d'un fichier téléchargé pour le hacher, en Mo."),
    max_chars: int = typer.Option(DEFAULT_MAX_CHARS, "--max-chars", min=0, help="Taille maximale du rapport md en caractères (0 = pas de limite)."),
) -> None:
    """Vérifie les URL du registre : changées (sha256), mortes, redirigées. Ne modifie rien."""
    sources = checkable(reg.all_sources())
    if only is not None:
        sources = [s for s in sources if s.get("id") == only]
        if not sources:
            typer.echo(f"Source `{only}` introuvable (ou rejected / superseded).", err=True)
            raise typer.Exit(2)

    targets: list[Target] = []
    without_url = 0
    for source in sources:
        found = targets_of(source)
        if not found:
            without_url += 1
        targets += found
    if limit is not None:
        targets = targets[:limit]

    with make_client() as client:
        results = run_checks(targets, Checker(client, delay=delay, max_mb=max_mb))

    day = reg.today()
    if format is Format.json:
        report = render_json(results, without_url, day)
    else:
        report = render_md(results, without_url, day, max_chars=max_chars)
    if out is None:
        typer.echo(report, nl=False)
    else:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        n = counts(results)
        typer.echo(
            f"{len(results)} URL vérifiée(s) : {n['change']} changée(s), {n['mort']} morte(s), "
            f"{n['redirige']} redirigée(s), {n['ignore']} non vérifiée(s) → {out}"
        )


if __name__ == "__main__":
    app()

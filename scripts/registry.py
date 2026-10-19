"""Registre des sources : chargement, schéma, taxonomie, règles d'identifiant.

Partagé par toutes les commandes. Le fichier `sources/<id>/source.yaml` est la
vérité ; ce module sait le lire, l'écrire (en gardant les commentaires du
template) et le valider contre `docs/taxonomie.md`.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Iterator

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"
REFERENTIELS = ROOT / "referentiels"
DOCS = ROOT / "docs"
SKILLS = ROOT / "skills-src"      # sources d'écriture des skills
PACKS = ROOT / "skills"          # packs générés par `build`, commités (npx skills add)
DIST = ROOT / "dist"             # zips (assets de release), git-ignoré
PYPROJECT = ROOT / "pyproject.toml"
GLOSSARY = ROOT / "GLOSSARY.md"
CONCEPTS = DOCS / "concepts"
TEMPLATE = SOURCES / "_template.yaml"
TAXONOMY = DOCS / "taxonomie.md"
INVENTORY = ROOT / "INVENTORY.md"

ISSUERS = ("msds", "cofor", "js", "cudesch", "autre")
TYPES = ("pdf", "docx", "xlsx", "pptx", "web", "image")
STATUSES = ("collected", "triaged", "converted", "indexed", "verified", "superseded", "rejected")
EXTRACTIONS = ("text", "vision", "catalogue", "none")
DECISIONS = ("", "keep", "rejected")
LANGS = ("fr", "de", "en")
FIDELITIES = ("complete", "partial")
NATURES = ("prescription", "recommandation", "exemple")

REQUIRED = (
    "id", "title", "issuer", "type", "status", "extraction",
    "retrieved", "sha256", "pages", "audience", "themes",
)
MAX_THEMES = 3
MAX_ID_LEN = 40
ID_RE = re.compile(r"^(?P<issuer>[a-z]+)-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)$")

EXT_TO_TYPE = {
    ".pdf": "pdf", ".docx": "docx", ".xlsx": "xlsx", ".pptx": "pptx",
    ".png": "image", ".jpg": "image", ".jpeg": "image", ".html": "web", ".htm": "web",
}


# --------------------------------------------------------------------------- #
# Identifiants et slugs
# --------------------------------------------------------------------------- #

def slugify(text: str, max_len: int = 60) -> str:
    """Minuscules, sans accents, tirets ; tronqué sur un tiret."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    text = re.sub(r"-{2,}", "-", text)
    if len(text) > max_len:
        text = text[:max_len].rsplit("-", 1)[0] or text[:max_len]
    return text


def check_id(source_id: str) -> list[str]:
    """Erreurs de forme d'un identifiant `<issuer>-<slug>`."""
    errors: list[str] = []
    if not source_id:
        return ["id vide"]
    if len(source_id) > MAX_ID_LEN:
        errors.append(f"id `{source_id}` dépasse {MAX_ID_LEN} caractères")
    m = ID_RE.match(source_id)
    if not m:
        errors.append(f"id `{source_id}` : forme attendue `<issuer>-<slug>` (minuscules, chiffres, tirets, sans accents)")
    elif m.group("issuer") not in ISSUERS:
        errors.append(f"id `{source_id}` : émetteur `{m.group('issuer')}` inconnu ({', '.join(ISSUERS)})")
    return errors


def issuer_of(source_id: str) -> str:
    return source_id.split("-", 1)[0]


# --------------------------------------------------------------------------- #
# Taxonomie
# --------------------------------------------------------------------------- #

@dataclass
class Taxonomy:
    audience: list[str] = field(default_factory=list)
    themes: list[str] = field(default_factory=list)


def load_taxonomy(path: Path = TAXONOMY) -> Taxonomy:
    """Lit les tables `## audience` et `## themes` de docs/taxonomie.md."""
    tax = Taxonomy()
    current: list[str] | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            name = line[3:].strip()
            current = getattr(tax, name) if name in ("audience", "themes") else None
            continue
        if current is None or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells or not cells[0].startswith("`"):
            continue
        current.append(cells[0].strip("`"))
    return tax


# --------------------------------------------------------------------------- #
# Lecture / écriture des source.yaml
# --------------------------------------------------------------------------- #

def project_version() -> str:
    """Version du dépôt (`pyproject.toml`, tenue par release-please)."""
    import tomllib

    return str(tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["project"]["version"])


def source_dir(source_id: str) -> Path:
    return SOURCES / source_id


def source_path(source_id: str) -> Path:
    return source_dir(source_id) / "source.yaml"


def load_template() -> dict[str, Any]:
    return yaml.safe_load(TEMPLATE.read_text(encoding="utf-8"))


def load_source(source_id: str) -> dict[str, Any]:
    path = source_path(source_id)
    if not path.exists():
        raise FileNotFoundError(f"source `{source_id}` introuvable ({path})")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data


def iter_source_dirs() -> Iterator[Path]:
    if not SOURCES.exists():
        return
    for d in sorted(SOURCES.iterdir()):
        if d.is_dir() and not d.name.startswith("_") and (d / "source.yaml").exists():
            yield d


def all_sources() -> list[dict[str, Any]]:
    return [yaml.safe_load((d / "source.yaml").read_text(encoding="utf-8")) or {} for d in iter_source_dirs()]


def find_by_sha(sha256: str) -> dict[str, Any] | None:
    if not sha256:
        return None
    for src in all_sources():
        if src.get("sha256") == sha256:
            return src
        for h in src.get("history") or []:
            if isinstance(h, dict) and h.get("sha256") == sha256:
                return src
    return None


def _scalar(value: Any) -> str:
    """Rend une valeur yaml sur une ligne (flow style)."""
    if value is None:
        return "null"
    if isinstance(value, date):
        return value.isoformat()
    dumped = yaml.safe_dump(value, default_flow_style=True, allow_unicode=True, width=10_000).strip()
    if dumped.endswith("\n..."):
        dumped = dumped[:-4].strip()
    return dumped


_KEY_LINE = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_]*):(?P<rest>.*)$")
_COMMENT = re.compile(r"\s+(#.*)$")


def render_source(data: dict[str, Any]) -> str:
    """Écrit un source.yaml en reprenant l'ordre et les commentaires du template.

    Les clés absentes du template sont ajoutées à la fin. Les listes de
    dictionnaires (history, web_pages) sont écrites en bloc.
    """
    out: list[str] = []
    seen: set[str] = set()
    lines = TEMPLATE.read_text(encoding="utf-8").splitlines()
    for line in lines:
        m = _KEY_LINE.match(line)
        if not m:
            if line.startswith("#  ") or line.startswith("#    "):
                continue  # exemple d'history dans le template
            out.append(line)
            continue
        key = m.group("key")
        seen.add(key)
        comment = ""
        cm = _COMMENT.search(m.group("rest"))
        if cm:
            comment = cm.group(1)
        value = data.get(key)
        out.append(_render_entry(key, value, comment))
    for key, value in data.items():
        if key not in seen:
            out.append(_render_entry(key, value, ""))
    return "\n".join(out).rstrip() + "\n"


def _render_entry(key: str, value: Any, comment: str) -> str:
    block = isinstance(value, list) and value and all(isinstance(v, dict) for v in value)
    if block:
        body = yaml.safe_dump({key: value}, allow_unicode=True, sort_keys=False, width=10_000).rstrip()
        head, _, tail = body.partition("\n")
        return (f"{head}{(' ' * 2 + comment) if comment else ''}\n{tail}") if tail else head
    text = f"{key}: {_scalar(value)}"
    if comment:
        pad = max(1, 40 - len(text))
        text = f"{text}{' ' * pad}{comment}"
    return text


def save_source(data: dict[str, Any]) -> Path:
    path = source_path(data["id"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_source(data), encoding="utf-8")
    return path


def set_status(source_id: str, status: str) -> None:
    if status not in STATUSES:
        raise ValueError(f"statut `{status}` inconnu")
    data = load_source(source_id)
    data["status"] = status
    save_source(data)


# --------------------------------------------------------------------------- #
# Hashes et comptage de pages
# --------------------------------------------------------------------------- #

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_dir(path: Path) -> str:
    """Hash déterministe d'un dossier : sha256 de « chemin relatif\\nsha256 » triés."""
    h = hashlib.sha256()
    for f in sorted(p for p in path.rglob("*") if p.is_file()):
        h.update(f.relative_to(path).as_posix().encode())
        h.update(b"\n")
        h.update(sha256_file(f).encode())
        h.update(b"\n")
    return h.hexdigest()


def count_pages(path: Path, source_type: str) -> int:
    """Pages PDF, diapos pptx, 0 sinon."""
    if source_type == "pdf":
        import pymupdf  # import local : lourd

        with pymupdf.open(path) as doc:
            return doc.page_count
    if source_type == "pptx":
        import zipfile

        with zipfile.ZipFile(path) as z:
            return sum(1 for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n))
    return 0


def original_sha256(data: dict[str, Any]) -> str:
    """Recalcule le sha256 de l'original tel qu'`ingest` l'a calculé.

    Fichier : sha256 du fichier ; dossier d'images : `sha256_dir` ; web :
    sha256 de la concaténation des `original/<slug>.html` dans l'ordre de
    `web_pages`. Lève ValueError si l'original est absent ou ambigu.
    """
    sid = data["id"]
    if data.get("type") == "web":
        blobs: list[bytes] = []
        for page in data.get("web_pages") or []:
            path = source_dir(sid) / "original" / f"{page.get('slug')}.html"
            if not path.exists():
                raise ValueError(f"page web `original/{path.name}` absente")
            blobs.append(path.read_bytes())
        return sha256_bytes(b"".join(blobs))
    files = original_files(sid)
    if not files:
        raise ValueError("aucun fichier dans `original/`")
    if len(files) > 1:
        raise ValueError(f"{len(files)} fichiers dans `original/`, une seule version attendue")
    return sha256_dir(files[0]) if files[0].is_dir() else sha256_file(files[0])


def guess_type(path: Path) -> str | None:
    if path.is_dir():
        return "image"
    return EXT_TO_TYPE.get(path.suffix.lower())


def original_files(source_id: str) -> list[Path]:
    d = source_dir(source_id) / "original"
    if not d.exists():
        return []
    return sorted(p for p in d.iterdir() if not p.name.startswith("."))


# --------------------------------------------------------------------------- #
# Validation
# --------------------------------------------------------------------------- #

def validate_source(data: dict[str, Any], folder: Path, tax: Taxonomy | None = None) -> list[str]:
    """Liste des erreurs d'un source.yaml. Vide si la source est valide."""
    tax = tax or load_taxonomy()
    sid = str(data.get("id") or "")
    tag = sid or folder.name
    errors = [f"{tag}: {e}" for e in check_id(sid)]

    for key in REQUIRED:
        if key not in data or data[key] is None or data[key] == "":
            if key in ("sha256",) and data.get("status") == "rejected":
                continue
            errors.append(f"{tag}: champ obligatoire `{key}` manquant ou vide")

    if folder.name != sid:
        errors.append(f"{tag}: dossier `{folder.name}` ≠ id `{sid}`")

    def check_enum(key: str, allowed: tuple[str, ...], required: bool = True) -> None:
        val = data.get(key)
        if val is None or val == "":
            if required:
                return  # déjà signalé comme manquant
            return
        if val not in allowed:
            errors.append(f"{tag}: `{key}: {val}` hors de ({', '.join(a or '\"\"' for a in allowed)})")

    check_enum("type", TYPES)
    check_enum("status", STATUSES)
    check_enum("extraction", EXTRACTIONS)
    check_enum("issuer", ISSUERS)
    check_enum("decision", DECISIONS, required=False)
    check_enum("lang", LANGS, required=False)

    if sid and data.get("issuer") and issuer_of(sid) != data.get("issuer"):
        errors.append(f"{tag}: préfixe de l'id `{issuer_of(sid)}` ≠ `issuer: {data.get('issuer')}`")
    if data.get("issuer") == "autre" and not data.get("issuer_detail"):
        errors.append(f"{tag}: `issuer_detail` obligatoire quand `issuer: autre`")

    for key, allowed in (("audience", tax.audience), ("themes", tax.themes)):
        vals = data.get(key)
        if vals is None or vals == "":
            continue
        if not isinstance(vals, list):
            errors.append(f"{tag}: `{key}` doit être une liste")
            continue
        for v in vals:
            if v not in allowed:
                errors.append(f"{tag}: `{key}` contient `{v}`, absent de docs/taxonomie.md")
        if key == "themes" and len(vals) > MAX_THEMES:
            errors.append(f"{tag}: au plus {MAX_THEMES} thèmes ({len(vals)} donnés)")

    if not isinstance(data.get("pages", 0), int):
        errors.append(f"{tag}: `pages` doit être un entier")

    if data.get("status") == "rejected":
        if data.get("decision") not in ("rejected", None, ""):
            errors.append(f"{tag}: `status: rejected` mais `decision: {data.get('decision')}`")
    elif (source_dir(sid) / "original").is_dir() and not original_files(sid):
        # `original/` absent = clone public (originaux hors git) ; présent mais vide = erreur.
        errors.append(f"{tag}: aucun fichier dans `original/`")
    if data.get("decision") == "rejected" and data.get("status") != "rejected":
        errors.append(f"{tag}: `decision: rejected` mais `status: {data.get('status')}`")

    if data.get("type") == "web":
        pages = data.get("web_pages")
        if not pages or not isinstance(pages, list):
            errors.append(f"{tag}: source web sans `web_pages`")

    errors.extend(f"{tag}: {e}" for e in check_phase3b_fields(data))
    return errors


def fidelity_of(data: dict[str, Any]) -> str:
    """`fidelity` effective : vide ou absent = `complete`."""
    return data.get("fidelity") or "complete"


def _as_date(value: Any) -> date | None:
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def check_phase3b_fields(data: dict[str, Any]) -> list[str]:
    """Champs optionnels : fidelity, applies_*, nature, redactions. Absents = défauts."""
    errors: list[str] = []
    fid = data.get("fidelity")
    if fid not in (None, "") and fid not in FIDELITIES:
        errors.append(f"`fidelity: {fid}` hors de ({', '.join(FIDELITIES)})")
    if fid == "partial" and not str(data.get("fidelity_notes") or "").strip():
        errors.append("`fidelity: partial` exige un motif dans `fidelity_notes`")
    nature = data.get("nature")
    if nature not in (None, "") and nature not in NATURES:
        errors.append(f"`nature: {nature}` hors de ({', '.join(NATURES)})")
    bounds: dict[str, date] = {}
    for key in ("applies_from", "applies_until"):
        val = data.get(key)
        if val in (None, ""):
            continue
        try:
            bounds[key] = _as_date(val)
        except ValueError:
            errors.append(f"`{key}: {val}` n'est pas une date AAAA-MM-JJ")
    if len(bounds) == 2 and bounds["applies_until"] < bounds["applies_from"]:
        errors.append("`applies_until` antérieur à `applies_from`")
    reds = data.get("redactions")
    if reds not in (None, ""):
        if not isinstance(reds, list):
            errors.append("`redactions` doit être une liste")
        else:
            for i, r in enumerate(reds, 1):
                if not isinstance(r, dict) or not r.get("section") or not r.get("pattern") or "replace" not in r:
                    errors.append(f"`redactions` n°{i} : {{section, pattern, replace}} attendus")
                    continue
                try:
                    re.compile(str(r["pattern"]))
                except re.error as exc:
                    errors.append(f"`redactions` n°{i} : regex invalide ({exc})")
    return errors


def validate_all() -> tuple[list[dict[str, Any]], list[str]]:
    """Charge et valide toutes les sources. Retourne (sources, erreurs)."""
    tax = load_taxonomy()
    sources: list[dict[str, Any]] = []
    errors: list[str] = []
    seen_ids: dict[str, str] = {}
    seen_sha: dict[str, str] = {}
    for d in iter_source_dirs():
        try:
            data = yaml.safe_load((d / "source.yaml").read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            errors.append(f"{d.name}: yaml invalide : {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{d.name}: source.yaml n'est pas un dictionnaire")
            continue
        errors.extend(validate_source(data, d, tax))
        sid = str(data.get("id") or d.name)
        if sid in seen_ids:
            errors.append(f"{sid}: id en double (dossiers `{seen_ids[sid]}` et `{d.name}`)")
        seen_ids[sid] = d.name
        sha = data.get("sha256")
        if sha:
            if sha in seen_sha:
                errors.append(f"{sid}: sha256 identique à `{seen_sha[sha]}` (doublon)")
            seen_sha[sha] = sid
        sources.append(data)
    return sources, errors


def today() -> date:
    return date.today()

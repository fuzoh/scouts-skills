"""`light` : contrôle des limites du skill `scouts` (skills-src/scouts/).

  light check [--root DIR] [--max-files N] [--table]
  light index [--root DIR]        # régénère savoirs/README.md

Règles : 200 fichiers au plus, 1 200 mots au plus par `.md` (`len(text.split())`,
comme `wc -w` ; 2 500 pour les descriptifs de cours `savoirs/formation-cours-*.md`), aucune citation de corpus, SKILL.md valide, référentiels et
savoirs avec leur frontmatter et leurs sections. Un référentiel est un dossier
`referentiels/<slug>/` de fichiers `NN-*.md` (frontmatter sur le premier ; sections et suite N
vérifiées sur la concaténation) ou, par compatibilité, un fichier `referentiels/<slug>.md`. Code 1 si erreur.
"""

from __future__ import annotations

import re
from fnmatch import fnmatch
from dataclasses import dataclass, field
from pathlib import Path

import typer
import yaml

from scripts import registry as reg

app = typer.Typer(add_completion=False, help=__doc__)

MAX_FILES = 200
MAX_WORDS = 1_200
# Exceptions : motif de chemin relatif → plafond. Descriptifs de cours du modèle de formation
# (buts et objectifs numérotés), qu'on ne coupe pas sans multiplier les fichiers.
WORD_EXCEPTIONS = {"savoirs/formation-cours-*.md": 2_500}
MAX_DESCRIPTION = 1_024
SKILL_NAME = "scouts"
SECTIONS = ("Non-négociables", "Selon la date", "Critères de qualité", "Pièges", "Trame de conception")
REF_KEYS = ("slug", "derive_de", "statut")
SAVOIR_KEYS = ("titre", "sert_a", "derive_de", "statut")
CITATION_PATTERNS = (
    (re.compile(r"`[a-z0-9-]+#[0-9]{2}-"), "citation `id#NN-slug`"),
    (re.compile(r"corpus/"), "chemin `corpus/`"),
    (re.compile(r"\bp\.[0-9]+"), "numéro de page `p.N`"),
)
FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.DOTALL)
HEADING_RE = re.compile(r"^## (.+?)\s*$", re.MULTILINE)
N_RE = re.compile(r"^\s*(?:[-*]\s*)?\**N(\d+)\b", re.MULTILINE)


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    files: int = 0
    words: int = 0
    per_file: dict[str, int] = field(default_factory=dict)

    @property
    def max_file(self) -> tuple[str, int]:
        if not self.per_file:
            return ("-", 0)
        name = max(self.per_file, key=lambda k: self.per_file[k])
        return name, self.per_file[name]


def max_words(rel: str) -> int:
    """Plafond de mots d'un fichier, `rel` relatif à la racine du skill."""
    return next((cap for pat, cap in WORD_EXCEPTIONS.items() if fnmatch(rel, pat)), MAX_WORDS)


def default_root() -> Path:
    return reg.SKILLS / SKILL_NAME


def parse_front(text: str) -> tuple[dict | None, str]:
    m = FRONT_RE.match(text)
    if not m:
        return None, text
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None, text
    return (data if isinstance(data, dict) else None), m.group(2)


def _check_keys(rel: str, front: dict | None, keys: tuple[str, ...], errors: list[str]) -> bool:
    if front is None:
        errors.append(f"{rel} : frontmatter YAML manquant ou invalide")
        return False
    for k in keys:
        if front.get(k) in (None, "", []):
            errors.append(f"{rel} : clé `{k}` manquante dans le frontmatter")
    return True


def _check_skill(root: Path, errors: list[str]) -> None:
    p = root / "SKILL.md"
    if not p.is_file():
        errors.append("SKILL.md : absent")
        return
    front, _ = parse_front(p.read_text(encoding="utf-8"))
    if not _check_keys("SKILL.md", front, ("name", "description"), errors) or front is None:
        return
    if front.get("name") != SKILL_NAME:
        errors.append(f"SKILL.md : `name` doit valoir `{SKILL_NAME}` (trouvé `{front.get('name')}`)")
    desc = str(front.get("description") or "")
    if len(desc) > MAX_DESCRIPTION:
        errors.append(f"SKILL.md : `description` fait {len(desc)} caractères (max {MAX_DESCRIPTION})")


def referentiel_parts(root: Path) -> list[tuple[str, list[Path]]]:
    """(slug, fichiers ordonnés) : dossiers `referentiels/<slug>/*.md` et fichiers plats."""
    base = root / "referentiels"
    out: list[tuple[str, list[Path]]] = []
    for p in sorted(base.iterdir()) if base.is_dir() else []:
        if p.is_dir():
            files = sorted(p.glob("*.md"))
            if files:
                out.append((p.name, files))
        elif p.suffix == ".md":
            out.append((p.stem, [p]))
    return out


def _check_referentiel(slug: str, files: list[Path], root: Path, errors: list[str]) -> None:
    rel = files[0].relative_to(root).as_posix() if len(files) == 1 else f"referentiels/{slug}/"
    front, body = parse_front(files[0].read_text(encoding="utf-8"))
    for extra in files[1:]:
        body += "\n" + extra.read_text(encoding="utf-8")
    if _check_keys(files[0].relative_to(root).as_posix(), front, REF_KEYS, errors) and front is not None:
        if front.get("slug") and front["slug"] != slug:
            errors.append(f"{rel} : `slug` (`{front['slug']}`) différent du nom du référentiel (`{slug}`)")
    titles = [t.strip() for t in HEADING_RE.findall(body)]
    pos = -1
    for s in SECTIONS:
        if s not in titles:
            errors.append(f"{rel} : section `## {s}` manquante")
            continue
        i = titles.index(s)
        if i < pos:
            errors.append(f"{rel} : section `## {s}` hors ordre")
        pos = max(pos, i)
    nums = [int(n) for n in N_RE.findall(body)]
    if not nums:
        errors.append(f"{rel} : aucun non-négociable N1..Nk")
    elif nums != list(range(1, len(nums) + 1)):
        errors.append(f"{rel} : suite N non contiguë ({', '.join(f'N{n}' for n in nums)})")


def check(root: Path, max_files: int = MAX_FILES) -> Report:
    rep = Report()
    if not root.is_dir():
        rep.errors.append(f"{root} : dossier absent")
        return rep
    files = sorted(f for f in root.rglob("*") if f.is_file())
    rep.files = len(files)
    if len(files) > max_files:
        rep.errors.append(f"{len(files)} fichiers (max {max_files})")
    for f in files:
        rel = f.relative_to(root).as_posix()
        if f.suffix != ".md":
            continue
        text = f.read_text(encoding="utf-8")
        n = len(text.split())
        rep.per_file[rel] = n
        rep.words += n
        cap = max_words(rel)
        if n > cap:
            rep.errors.append(f"{rel} : {n} mots (max {cap})")
        for rx, label in CITATION_PATTERNS:
            for m in rx.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                rep.errors.append(f"{rel}:{line} : {label} interdit(e) (`{m.group(0)}`)")
    _check_skill(root, rep.errors)
    for slug, parts in referentiel_parts(root):
        _check_referentiel(slug, parts, root, rep.errors)
    for f in sorted((root / "savoirs").glob("*.md")):
        if f.name == "README.md":
            continue
        rel = f.relative_to(root).as_posix()
        front, _ = parse_front(f.read_text(encoding="utf-8"))
        _check_keys(rel, front, SAVOIR_KEYS, rep.errors)
    return rep


@app.callback()
def _main() -> None:
    """Contrôles du skill scouts."""


@app.command("check")
def check_cmd(
    root: Path = typer.Option(None, "--root", help="Défaut skills-src/scouts."),
    max_files: int = typer.Option(MAX_FILES, "--max-files", help="Plafond de fichiers."),
    table: bool = typer.Option(False, "--table", help="Affiche le tableau fichier → mots."),
) -> None:
    """Vérifie fichiers, mots, citations et formats de scouts."""
    rep = check(root or default_root(), max_files)
    if table:
        for name, n in sorted(rep.per_file.items()):
            typer.echo(f"{n:>6}  {name}")
    if rep.errors:
        for e in rep.errors:
            typer.echo(f"- {e}", err=True)
        raise typer.Exit(1)
    name, n = rep.max_file
    typer.echo(f"✓ scouts : {rep.files} fichiers, {rep.words} mots, max {n} mots ({name})")


def build_index(root: Path) -> str:
    """`savoirs/README.md` : un tableau fichier → `sert_a` tiré des frontmatters."""
    rows = []
    for f in sorted((root / "savoirs").glob("*.md")):
        if f.name == "README.md":
            continue
        front, _ = parse_front(f.read_text(encoding="utf-8"))
        front = front or {}
        rows.append(f"| `{f.name}` | {front.get('titre', '')} | {front.get('sert_a', '')} |")
    head = ("# Index des savoirs\n\nGénéré par `light index`, ne pas éditer. Lire le fichier dont la colonne "
            "« sert à » répond à la question ; plusieurs fichiers d'un même thème se complètent.\n\n"
            "| fichier | titre | sert à |\n|---|---|---|\n")
    return head + "\n".join(rows) + "\n"


@app.command("index")
def index_cmd(root: Path = typer.Option(None, "--root", help="Défaut skills-src/scouts.")) -> None:
    """Régénère savoirs/README.md depuis les frontmatters des savoirs."""
    r = root or default_root()
    out = r / "savoirs" / "README.md"
    out.write_text(build_index(r), encoding="utf-8")
    typer.echo(f"✓ {out}")


if __name__ == "__main__":
    app()

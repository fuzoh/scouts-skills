"""`light` : contrôle des limites du skill `scouts` (skills-src/scouts/).

  light check [--root DIR] [--max-files N] [--table]
  light index [--root DIR]        # régénère savoirs/README.md

`scouts` doit s'installer par zip sur les applis web (claude.ai, ChatGPT, Gemini). Limites dures,
la plus basse des plateformes (`docs/contraintes-plateformes.md`) : 100 fichiers dans le pack
(Gemini échoue à 150 ; le build ajoute MANIFEST.md, d'où 99 dans la source), 50 Mo au total
et 25 Mo par fichier (OpenAI), aucun format binaire bureautique (.docx, .doc, .xlsx, .xls : refusés
par Gemini), un seul SKILL.md, `name` au format agentskills (minuscules, tirets, ≤ 64 car., = nom
du dossier), `description` ≤ 1 024 car. (avertissement au-delà des 200 annoncés par l'aide
claude.ai, non appliqués à ce jour), aucun appel réseau dans `scripts/` (Gemini).

Budget de lecture (choix de performance, pas une limite de plateforme) : 5 000 tokens estimés par
`.md` (`ceil(caractères / 3,5)`, recommandation agentskills pour SKILL.md étendue à chaque fichier,
puisqu'un fichier se lit en entier), SKILL.md sous 500 lignes. Aussi : aucune citation de corpus,
référentiels et savoirs avec leur frontmatter et leurs sections. Un référentiel est un dossier
`referentiels/<slug>/` de fichiers `NN-*.md` (frontmatter sur le premier ; sections et suite N
vérifiées sur la concaténation) ou, par compatibilité, un fichier `referentiels/<slug>.md`. Code 1 si erreur.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path

import typer
import yaml

from scripts import registry as reg

app = typer.Typer(add_completion=False, help=__doc__)

MAX_FILES = 100            # pack : Gemini passe à 100, échoue à 150 et 200 (essais du mainteneur)
PACK_EXTRA_FILES = 1       # MANIFEST.md ajouté par le build
MAX_FILE_BYTES = 25 * 1024 * 1024   # OpenAI : fichier décompressé
MAX_TOTAL_BYTES = 50 * 1024 * 1024  # OpenAI : zip ; Gemini : 100 Mo
MAX_TOKENS = 5_000         # budget de lecture par fichier .md (estimation)
CHARS_PER_TOKEN = 3.5      # français, prudent
MAX_SKILL_LINES = 500      # agentskills : SKILL.md
MAX_DESCRIPTION = 1_024    # agentskills
WARN_DESCRIPTION = 200     # aide claude.ai, non appliqué à ce jour
MAX_NAME = 64
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
BINARY_EXT = (".docx", ".doc", ".xlsx", ".xls")
NETWORK_RE = re.compile(r"\b(requests|urllib|httpx|aiohttp|socket|fetch\(|axios|curl|wget)\b")
SKILL_NAME = "scouts"
SECTIONS = ("Non-négociables", "Selon la date", "Critères de qualité", "Pièges", "Trame de conception")
REF_KEYS = ("slug", "derive_de", "statut")
SAVOIR_KEYS = ("titre", "theme", "sert_a", "derive_de", "statut")
# `theme` d'un savoir → rubrique de savoirs/README.md, dans cet ordre
THEMES = {
    "camp": "Camp : démarches, lieu, matériel, cuisine, budget",
    "js": "J+S : règles 2026 et 2027, formes, rôles, coach",
    "securite": "Sécurité, urgence et protection",
    "programme": "Profil, programme et branches",
    "sport": "Jeux, sport et pédagogie de terrain",
    "prevention": "Prévention et inclusion",
    "groupe": "Groupe, maîtrise et encadrement",
    "formation": "Formation : cours, UA, qualification",
}
MAX_SERT_A = 300           # caractères : une ligne de l'index par savoir
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
    warnings: list[str] = field(default_factory=list)
    files: int = 0
    words: int = 0
    bytes: int = 0
    per_file: dict[str, int] = field(default_factory=dict)  # tokens estimés

    @property
    def max_file(self) -> tuple[str, int]:
        if not self.per_file:
            return ("-", 0)
        name = max(self.per_file, key=lambda k: self.per_file[k])
        return name, self.per_file[name]


def estimate_tokens(text: str) -> int:
    """Tokens estimés : `ceil(caractères / 3,5)`, sans tokeniseur (aucun n'est celui de toutes les plateformes)."""
    return math.ceil(len(text) / CHARS_PER_TOKEN)


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


def _check_skill(root: Path, rep: Report) -> None:
    errors = rep.errors
    p = root / "SKILL.md"
    if not p.is_file():
        errors.append("SKILL.md : absent")
        return
    text = p.read_text(encoding="utf-8")
    if (n := len(text.splitlines())) > MAX_SKILL_LINES:
        errors.append(f"SKILL.md : {n} lignes (max {MAX_SKILL_LINES})")
    front, _ = parse_front(text)
    if not _check_keys("SKILL.md", front, ("name", "description"), errors) or front is None:
        return
    name = str(front.get("name") or "")
    if name != SKILL_NAME:
        errors.append(f"SKILL.md : `name` doit valoir `{SKILL_NAME}` (trouvé `{front.get('name')}`)")
    elif len(name) > MAX_NAME or not NAME_RE.match(name):
        errors.append(f"SKILL.md : `name` `{name}` hors format agentskills (minuscules, chiffres, tirets, ≤ {MAX_NAME})")
    desc = str(front.get("description") or "")
    if len(desc) > MAX_DESCRIPTION:
        errors.append(f"SKILL.md : `description` fait {len(desc)} caractères (max {MAX_DESCRIPTION})")
    elif len(desc) > WARN_DESCRIPTION:
        rep.warnings.append(f"SKILL.md : `description` fait {len(desc)} caractères "
                            f"(l'aide claude.ai annonce {WARN_DESCRIPTION} ; accepté à ce jour, à retester)")


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
    """`max_files` = plafond du pack ; la source en a `PACK_EXTRA_FILES` de moins."""
    rep = Report()
    if not root.is_dir():
        rep.errors.append(f"{root} : dossier absent")
        return rep
    files = sorted(f for f in root.rglob("*") if f.is_file())
    rep.files = len(files)
    if len(files) + PACK_EXTRA_FILES > max_files:
        rep.errors.append(f"{len(files)} fichiers (max {max_files - PACK_EXTRA_FILES} : "
                          f"le pack en ajoute {PACK_EXTRA_FILES}, plafond {max_files})")
    skill_md = [f for f in files if f.name.lower() == "skill.md"]
    if len(skill_md) > 1:
        rep.errors.append(f"{len(skill_md)} fichiers SKILL.md (un seul admis) : "
                          + ", ".join(f.relative_to(root).as_posix() for f in skill_md))
    for f in files:
        rel = f.relative_to(root).as_posix()
        size = f.stat().st_size
        rep.bytes += size
        if size > MAX_FILE_BYTES:
            rep.errors.append(f"{rel} : {size / 1e6:.1f} Mo (max {MAX_FILE_BYTES // 2**20} Mo)")
        if f.suffix.lower() in BINARY_EXT:
            rep.errors.append(f"{rel} : format {f.suffix} refusé par Gemini (convertir en .md ou .csv)")
        if rel.startswith("scripts/") and f.suffix not in (".md",):
            m = NETWORK_RE.search(f.read_text(encoding="utf-8", errors="ignore"))
            if m:
                rep.errors.append(f"{rel} : appel réseau (`{m.group(0)}`) impossible sur Gemini")
        if f.suffix != ".md":
            continue
        text = f.read_text(encoding="utf-8")
        rep.words += len(text.split())
        tokens = estimate_tokens(text)
        rep.per_file[rel] = tokens
        if tokens > MAX_TOKENS:
            rep.errors.append(f"{rel} : ~{tokens} tokens (max {MAX_TOKENS})")
        for rx, label in CITATION_PATTERNS:
            for m in rx.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                rep.errors.append(f"{rel}:{line} : {label} interdit(e) (`{m.group(0)}`)")
    if rep.bytes > MAX_TOTAL_BYTES:
        rep.errors.append(f"{rep.bytes / 1e6:.1f} Mo au total (max {MAX_TOTAL_BYTES // 2**20} Mo)")
    _check_skill(root, rep)
    for slug, parts in referentiel_parts(root):
        _check_referentiel(slug, parts, root, rep.errors)
    for f in sorted((root / "savoirs").glob("*.md")):
        if f.name == "README.md":
            continue
        rel = f.relative_to(root).as_posix()
        front, _ = parse_front(f.read_text(encoding="utf-8"))
        if not _check_keys(rel, front, SAVOIR_KEYS, rep.errors):
            continue
        if front.get("theme") and front["theme"] not in THEMES:
            rep.errors.append(f"{rel} : `theme` `{front['theme']}` inconnu ({', '.join(THEMES)})")
        if len(str(front.get("sert_a", ""))) > MAX_SERT_A:
            rep.warnings.append(f"{rel} : `sert_a` de {len(str(front['sert_a']))} car. (index : {MAX_SERT_A} conseillés)")
    return rep


@app.callback()
def _main() -> None:
    """Contrôles du skill scouts."""


@app.command("check")
def check_cmd(
    root: Path = typer.Option(None, "--root", help="Défaut skills-src/scouts."),
    max_files: int = typer.Option(MAX_FILES, "--max-files", help="Plafond de fichiers du pack."),
    table: bool = typer.Option(False, "--table", help="Affiche le tableau fichier → tokens estimés."),
) -> None:
    """Vérifie limites des plateformes web, budget de lecture, citations et formats de scouts."""
    rep = check(root or default_root(), max_files)
    if table:
        for name, n in sorted(rep.per_file.items()):
            typer.echo(f"{n:>6}  {name}")
    for w in rep.warnings:
        typer.echo(f"! {w}", err=True)
    if rep.errors:
        for e in rep.errors:
            typer.echo(f"- {e}", err=True)
        raise typer.Exit(1)
    name, n = rep.max_file
    typer.echo(f"✓ scouts : {rep.files} fichiers, {rep.bytes / 1e3:.0f} Ko, {rep.words} mots, "
               f"max ~{n} tokens ({name})")


def build_index(root: Path) -> str:
    """`savoirs/README.md` : une rubrique par `theme` (ordre de THEMES), une ligne fichier → `sert_a`."""
    groups: dict[str, list[str]] = {}
    for f in sorted((root / "savoirs").glob("*.md")):
        if f.name == "README.md":
            continue
        front, _ = parse_front(f.read_text(encoding="utf-8"))
        front = front or {}
        groups.setdefault(front.get("theme", ""), []).append(f"| `{f.name}` | {front.get('sert_a', '')} |")
    out = ["# Index des savoirs\n\nGénéré par `light index`, ne pas éditer. Repérer la rubrique, puis lire le "
           "ou les fichiers dont la colonne « sert à » répond à la question ; les fichiers d'une rubrique "
           "se complètent.\n"]
    for key in [*THEMES, *sorted(k for k in groups if k not in THEMES)]:
        if key not in groups:
            continue
        out.append(f"## {THEMES.get(key, key or 'Sans thème')}\n\n| fichier | sert à |\n|---|---|\n"
                   + "\n".join(groups[key]) + "\n")
    return "\n".join(out)


@app.command("index")
def index_cmd(root: Path = typer.Option(None, "--root", help="Défaut skills-src/scouts.")) -> None:
    """Régénère savoirs/README.md depuis les frontmatters des savoirs."""
    r = root or default_root()
    out = r / "savoirs" / "README.md"
    out.write_text(build_index(r), encoding="utf-8")
    typer.echo(f"✓ {out}")


if __name__ == "__main__":
    app()

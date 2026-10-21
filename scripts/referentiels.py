"""`referentiels` : validation des référentiels (`referentiels/*.md`).

Règles : docs/skills-design.md § 2 et § 6. Les erreurs bloquent, les
avertissements informent. API réutilisable par `build` : `load_referentiel`,
`all_referentiels`, `parse_citations`, `resolve_section`, `citing`, `validate`.

  referentiels check            valide tous les référentiels (défaut)
  referentiels --citing <id>    liste les référentiels qui citent une source
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import typer
import yaml

from scripts import registry as reg
from scripts import split as sp

app = typer.Typer(add_completion=False, help=__doc__)

REQUIRED_KEYS = ("slug", "titre", "signaux", "role", "verbes", "parametres",
                 "canevas", "sources", "inclut", "statut", "relu_le")
STATUTS = ("brouillon", "relu", "valide")
VERBES = ("chercher", "expliquer", "corriger", "concevoir")
SECTIONS = ("Non-négociables", "Selon la date", "Critères de qualité", "Critères non officiels",
            "Questions à poser avant de juger", "Pièges", "Trame de conception")
WORDS_WARN = 4_000
WORDS_ERROR = 6_000
MAX_COLUMNS = 6

TOKEN_RE = re.compile(r"`([^`\n]+)`")
CITE_RE = re.compile(r"^(?P<id>[^\s#`]+)(?:#(?P<section>[^\s#`]+))?(?:\s+p\.(?P<page>\d+(?:-\d+)?))?$")


@dataclass
class Citation:
    source_id: str
    section: str | None
    page: str | None
    line: int
    raw: str


@dataclass
class Referentiel:
    path: Path
    slug: str
    front: dict[str, Any]
    body: str
    citations: list[Citation] = field(default_factory=list)
    source_ids: set[str] = field(default_factory=set)
    words: int = 0
    body_offset: int = 0      # lignes du frontmatter : ligne fichier = ligne du corps + body_offset


# --------------------------------------------------------------------------- #
# Lecture
# --------------------------------------------------------------------------- #

def _is_source_id(token: str) -> bool:
    m = reg.ID_RE.match(token)
    return bool(m) and m.group("issuer") in reg.ISSUERS


def parse_citations(body: str) -> list[Citation]:
    """Citations de sources entre accents graves ; `line` = ligne dans `body` (1 = première)."""
    found: list[Citation] = []
    for lineno, line in enumerate(body.splitlines(), start=1):
        for m in TOKEN_RE.finditer(line):
            cm = CITE_RE.match(m.group(1).strip())
            if not cm or not _is_source_id(cm.group("id")):
                continue
            found.append(Citation(cm.group("id"), cm.group("section"), cm.group("page"), lineno, m.group(1)))
    return found


def load_referentiel(path: Path) -> Referentiel:
    text = path.read_text(encoding="utf-8")
    try:
        front, body = sp.read_front(text)
    except yaml.YAMLError as exc:
        front, body = {"_yaml_invalide": str(exc)}, text
    if not isinstance(front, dict):
        front = {"_yaml_invalide": "le frontmatter n'est pas un dictionnaire"}
    citations = parse_citations(body)
    # Les lignes sont comptées dans le fichier entier : le corps commence après le frontmatter.
    offset = text[: len(text) - len(body)].count("\n") if body and text.endswith(body) else 0
    for c in citations:
        c.line += offset
    return Referentiel(path=path, slug=path.stem, front=front, body=body, citations=citations,
                       source_ids={c.source_id for c in citations}, words=len(body.split()), body_offset=offset)


def all_referentiels() -> list[Referentiel]:
    if not reg.REFERENTIELS.exists():
        return []
    return [load_referentiel(p) for p in sorted(reg.REFERENTIELS.glob("*.md"))]


def _candidates(source_id: str, section: str) -> list[Path]:
    sdir = reg.source_dir(source_id)
    if re.fullmatch(r"\d+", section):
        return sorted(p for p in sdir.glob(f"{section}-*.md") if sp.SECTION_FILE_RE.match(p.name))
    path = sdir / sp.section_key(section)
    return [path] if path.is_file() else []


def resolve_section(source_id: str, section: str) -> Path | None:
    """Fichier d'une section : `NN-slug` exact, ou `NN` seul si un seul fichier `NN-*.md`."""
    found = _candidates(source_id, section)
    return found[0] if len(found) == 1 else None


def citing(source_id: str) -> list[str]:
    """Slugs des référentiels qui citent `source_id`."""
    return [r.slug for r in all_referentiels() if source_id in r.source_ids]


# --------------------------------------------------------------------------- #
# Validation
# --------------------------------------------------------------------------- #

def _headings(body: str) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    fenced = False
    for lineno, line in enumerate(body.splitlines(), start=1):
        if line.startswith("```"):
            fenced = not fenced
        if not fenced and line.startswith("## "):
            out.append((lineno, line[3:].strip()))
    return out


def _section_lines(body: str, name: str) -> list[tuple[int, str]]:
    """(numéro de ligne dans body, texte) des lignes d'une section `## name`."""
    lines = body.splitlines()
    out: list[tuple[int, str]] = []
    inside = False
    for lineno, line in enumerate(lines, start=1):
        if line.startswith("## "):
            inside = line[3:].strip() == name
            continue
        if inside:
            out.append((lineno, line))
    return out


def _check_sequence(label: str, numbers: list[int]) -> list[str]:
    warnings: list[str] = []
    if not numbers:
        return warnings
    for n in sorted({n for n in numbers if numbers.count(n) > 1}):
        warnings.append(f"{label}{n} en double")
    for n in range(1, max(numbers) + 1):
        if n not in numbers:
            warnings.append(f"{label}{n} manquant dans la suite 1..{max(numbers)}")
    return warnings


def _check_front(ref: Referentiel) -> list[str]:
    front, errors = ref.front, []
    if "_yaml_invalide" in front:
        return [f"frontmatter illisible : {front['_yaml_invalide']}"]
    if not front:
        return ["frontmatter `---` absent"]
    for key in REQUIRED_KEYS:
        if key not in front:
            errors.append(f"frontmatter : clé obligatoire `{key}` manquante")
    for key in front:
        if key not in REQUIRED_KEYS:
            errors.append(f"frontmatter : clé inconnue `{key}`")
    if "slug" in front and front["slug"] != ref.slug:
        errors.append(f"frontmatter : `slug: {front['slug']}` ≠ nom de fichier `{ref.slug}`")
    if "statut" in front and front["statut"] not in STATUTS:
        errors.append(f"frontmatter : `statut: {front['statut']}` hors de ({', '.join(STATUTS)})")
    for key in ("signaux", "role", "verbes", "canevas", "sources", "inclut"):
        if key in front and not isinstance(front[key], list):
            errors.append(f"frontmatter : `{key}` doit être une liste")
    verbes = front.get("verbes")
    if isinstance(verbes, list):
        for v in verbes:
            if v not in VERBES:
                errors.append(f"frontmatter : verbe `{v}` hors de ({', '.join(VERBES)})")
    params = front.get("parametres")
    if "parametres" in front:
        if not isinstance(params, list):
            errors.append("frontmatter : `parametres` doit être une liste")
        else:
            for i, p in enumerate(params, 1):
                if not (isinstance(p, dict) and set(p) == {"nom", "obligatoire"}
                        and isinstance(p["nom"], str) and isinstance(p["obligatoire"], bool)):
                    errors.append(f"frontmatter : `parametres` n°{i} : {{nom: texte, obligatoire: booléen}} attendu")
    if "relu_le" in front and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(front["relu_le"])):
        errors.append(f"frontmatter : `relu_le: {front['relu_le']}` n'est pas une date AAAA-MM-JJ")
    return errors


def _check_sections(ref: Referentiel) -> list[str]:
    errors: list[str] = []
    heads = _headings(ref.body)
    names = [n for _, n in heads]
    for req in SECTIONS:
        if req not in names:
            errors.append(f"section obligatoire `## {req}` absente")
    last = -1
    for _, n in heads:
        if n in SECTIONS:
            i = SECTIONS.index(n)
            if i < last:
                errors.append(f"section `## {n}` hors d'ordre (attendue avant `## {SECTIONS[last]}`)")
            last = max(last, i)
    q_idx, non_off_idx, trame_idx = SECTIONS.index("Questions à poser avant de juger"), 3, SECTIONS.index("Trame de conception")
    seen = -1
    for lineno, n in heads:
        if n in SECTIONS:
            seen = SECTIONS.index(n)
            continue
        if n.startswith("Annexe"):
            if seen < trame_idx:
                errors.append(f"ligne {lineno}: `## {n}` doit venir après `## Trame de conception`")
            continue
        if seen < non_off_idx or seen >= q_idx:
            errors.append(f"ligne {lineno}: section libre `## {n}` hors de l'emplacement permis "
                          "(entre `## Critères non officiels` et `## Questions à poser avant de juger`)")
    return errors


def _index_files(source_id: str, cache: dict[str, set[str] | None]) -> set[str] | None:
    if source_id not in cache:
        idx = reg.source_dir(source_id) / "index.md"
        try:
            _, roots = sp.parse_index(idx.read_text(encoding="utf-8"))
            cache[source_id] = {s.file for s in sp.walk(roots)}
        except (OSError, sp.SplitError):
            cache[source_id] = None
    return cache[source_id]


def _check_citations(ref: Referentiel, known: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    cache: dict[str, set[str] | None] = {}
    for c in ref.citations:
        where = f"ligne {c.line}: `{c.raw}`"
        if c.source_id not in known:
            errors.append(f"{where} : source inconnue `{c.source_id}`")
            continue
        if c.section is None:
            continue
        cands = _candidates(c.source_id, c.section)
        if not cands:
            errors.append(f"{where} : section introuvable dans `sources/{c.source_id}/`")
            continue
        if len(cands) > 1:
            errors.append(f"{where} : `#{c.section}` ambigu ({', '.join(p.name for p in cands)})")
            continue
        indexed = _index_files(c.source_id, cache)
        if indexed is None:
            errors.append(f"{where} : `sources/{c.source_id}/index.md` absent ou illisible")
        elif cands[0].name not in indexed:
            errors.append(f"{where} : `{cands[0].name}` ne figure pas dans l'index de `{c.source_id}`")
    return errors


def _check_non_negociables(ref: Referentiel) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    numbers: list[int] = []
    cited_lines = {c.line for c in ref.citations}
    lines = _section_lines(ref.body, "Non-négociables")
    base = ref.body_offset
    i = 0
    while i < len(lines):
        lineno, text = lines[i]
        m = re.match(r"^N(\d+)\.\s", text + " ")
        if not m:
            i += 1
            continue
        numbers.append(int(m.group(1)))
        block = [lineno + base]
        j = i + 1
        while j < len(lines) and lines[j][1].strip() and not re.match(r"^N\d+\.\s", lines[j][1] + " "):
            block.append(lines[j][0] + base)
            j += 1
        if not re.search(r"\bretiré\b", text) and not any(n in cited_lines for n in block):
            errors.append(f"ligne {lineno + base}: N{m.group(1)} sans citation de source")
        i = j
    return errors, _check_sequence("N", numbers)


def _check_numbering(ref: Referentiel) -> list[str]:
    warnings: list[str] = []
    q = [int(m.group(1)) for _, t in _section_lines(ref.body, "Critères de qualité")
         if (m := re.match(r"^Q(\d+)\.\s", t + " "))]
    warnings += _check_sequence("Q", q)
    qs = [int(m.group(1)) for _, t in _section_lines(ref.body, "Questions à poser avant de juger")
          if (m := re.match(r"^(\d+)\.\s", t + " "))]
    warnings += [f"Questions à poser, {w}" for w in _check_sequence("n°", qs)]
    return warnings


def _check_tables(ref: Referentiel) -> list[str]:
    out: list[str] = []
    base = ref.body_offset
    for lineno, line in enumerate(ref.body.splitlines(), start=1):
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            cols = len(re.split(r"(?<!\\)\|", s)) - 2
            if cols > MAX_COLUMNS:
                out.append(f"ligne {lineno + base}: tableau de {cols} colonnes (maximum {MAX_COLUMNS})")
    return out


def _inclut_cycle(slug: str, fronts: dict[str, Any]) -> list[str] | None:
    """Premier cycle d'`inclut` atteignable depuis `slug`, sous forme de chemin, sinon None."""
    def visit(node: str, path: list[str]) -> list[str] | None:
        for nxt in (fronts.get(node) or {}).get("inclut") or []:
            if nxt in path:
                return path[path.index(nxt):] + [nxt]
            if nxt in fronts:
                found = visit(nxt, path + [nxt])
                if found:
                    return found
        return None
    return visit(slug, [slug])


def validate(ref: Referentiel, known_sources: dict[str, Any]) -> tuple[list[str], list[str]]:
    """(erreurs, avertissements) d'un référentiel."""
    errors = _check_front(ref)
    warnings: list[str] = []
    errors += _check_sections(ref)
    errors += _check_citations(ref, known_sources)
    n_err, n_warn = _check_non_negociables(ref)
    errors += n_err
    warnings += n_warn + _check_numbering(ref) + _check_tables(ref)

    front = ref.front
    if isinstance(front.get("sources"), list):
        declared = {str(s) for s in front["sources"]}
        missing = sorted(ref.source_ids - declared)
        extra = sorted(declared - ref.source_ids)
        if missing:
            errors.append(f"`sources:` : cités dans le corps mais absents du frontmatter : {', '.join(missing)}")
        if extra:
            errors.append(f"`sources:` : listés mais jamais cités dans le corps : {', '.join(extra)}")

    if isinstance(front.get("inclut"), list):
        existing = {p.stem for p in reg.REFERENTIELS.glob("*.md")} if reg.REFERENTIELS.exists() else set()
        for slug in front["inclut"]:
            if slug not in existing:
                errors.append(f"`inclut:` : référentiel `{slug}` inexistant")
        fronts = {r.slug: r.front for r in all_referentiels()}
        fronts[ref.slug] = front
        cycle = _inclut_cycle(ref.slug, fronts)
        if cycle:
            errors.append(f"`inclut:` : cycle {' → '.join(cycle)}")

    if isinstance(front.get("canevas"), list):
        for cid in front["canevas"]:
            if cid not in known_sources:
                errors.append(f"`canevas:` : source inconnue `{cid}`")
            elif (known_sources[cid] or {}).get("nature") != "exemple":
                warnings.append(f"`canevas:` : `{cid}` n'a pas `nature: exemple`")

    if ref.words > WORDS_ERROR:
        errors.append(f"corps de {ref.words} mots (maximum {WORDS_ERROR})")
    elif ref.words > WORDS_WARN:
        warnings.append(f"corps de {ref.words} mots (au-delà de {WORDS_WARN})")
    return errors, warnings


CATALOG_ROW = re.compile(r"^\| `([a-z0-9-]+)` \|", re.M)


def catalogues() -> tuple[Path, Path]:
    """Chemins calculés à l'appel : `reg.SKILLS` est redirigé dans les tests."""
    return (
        reg.SKILLS / "scouts" / "SKILL.md",
        reg.SKILLS / "scouts-ressources" / "SKILL.md",
    )


def catalogue_slugs(path: Path) -> set[str] | None:
    """Slugs de la table catalogue, ou None si le fichier n'existe pas (dépôt jouet)."""
    if not path.is_file():
        return None
    return set(CATALOG_ROW.findall(path.read_text(encoding="utf-8")))


def _iso(value: Any) -> str:
    if hasattr(value, "isoformat"):
        return value.isoformat()[:10]
    return str(value or "")


def check_routing() -> list[str]:
    """Chaque référentiel est dans les deux catalogues ; `derive_de.relu_le` égale le racine.

    Sans fichier catalogue, ne dit rien : le dépôt jouet n'a pas de `SKILL.md`.
    Un catalogue présent est comparé même s'il n'y a aucun référentiel.
    """
    refs = all_referentiels()
    errors: list[str] = []
    found = [(path, catalogue_slugs(path)) for path in catalogues()]
    # Les deux catalogues, ou rien : un dépôt jouet n'a souvent qu'un SKILL.md sans table.
    if all(slugs is not None for _, slugs in found):
        known = {r.slug for r in refs}
        for path, slugs in found:
            label = path.relative_to(reg.ROOT).as_posix()
            if slugs is None:
                errors.append(f"catalogue absent : {label}")
                continue
            for ref in refs:
                if ref.slug not in slugs:
                    errors.append(f"referentiels/{ref.slug}.md absent du catalogue {label}")
            for slug in sorted(slugs - known):
                errors.append(f"catalogue {label} : `{slug}` sans referentiels/{slug}.md")
    derived = reg.SKILLS / "scouts" / "referentiels"
    if derived.is_dir():
        for ref in refs:
            folder = derived / ref.slug
            if not folder.is_dir():
                errors.append(f"skills-src/scouts/referentiels/{ref.slug}/ absent")
                continue
            parts = sorted(p for p in folder.glob("*.md"))
            if not parts:
                errors.append(f"skills-src/scouts/referentiels/{ref.slug}/ : aucun fichier")
                continue
            front, _ = sp.read_front(parts[0].read_text(encoding="utf-8"))
            derive = front.get("derive_de") if isinstance(front, dict) else None
            got = _iso(derive.get("relu_le") if isinstance(derive, dict) else None)
            want = _iso(ref.front.get("relu_le") if isinstance(ref.front, dict) else None)
            if got != want:
                errors.append(
                    f"skills-src/scouts/referentiels/{ref.slug}/ : "
                    f"derive_de.relu_le `{got}` ≠ relu_le `{want}`"
                )
    return errors


def check_all(known_sources: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Valide tous les référentiels ; messages préfixés par `referentiels/<slug>.md`."""
    errors: list[str] = []
    warnings: list[str] = []
    for ref in all_referentiels():
        e, w = validate(ref, known_sources)
        tag = f"referentiels/{ref.path.name}"
        errors += [f"{tag}: {m}" for m in e]
        warnings += [f"{tag}: {m}" for m in w]
    errors += check_routing()
    return errors, warnings


def run(check_only: bool = True) -> int:
    """Valide les référentiels (`check_only` : seule opération pour l'instant)."""
    known = {str(s.get("id")): s for s in reg.all_sources()}
    refs = all_referentiels()
    errors, warnings = check_all(known)
    if errors:
        typer.echo(f"{len(errors)} erreur(s) :", err=True)
        for e in errors:
            typer.echo(f"  - {e}", err=True)
    if warnings:
        typer.echo(f"{len(warnings)} avertissement(s) :", err=True)
        for w in warnings:
            typer.echo(f"  - {w}", err=True)
    if errors:
        return 1
    typer.echo(f"✓ {len(refs)} référentiel(s) valides")
    return 0


def _main(citing_id: str | None) -> None:
    if citing_id:
        for slug in citing(citing_id):
            typer.echo(slug)
        return
    raise typer.Exit(run(check_only=True))


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context,
         citing_id: str = typer.Option(None, "--citing", help="Lister les référentiels qui citent cette source.")) -> None:
    """Valide les référentiels (commande par défaut)."""
    if ctx.invoked_subcommand is None:
        _main(citing_id)


@app.command()
def check(citing_id: str = typer.Option(None, "--citing", help="Lister les référentiels qui citent cette source.")) -> None:
    """Valide tous les référentiels ; code 1 si une erreur."""
    _main(citing_id)


if __name__ == "__main__":
    app()

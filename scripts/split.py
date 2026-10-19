"""`split <id>` : découpe `raw.md` en `NN-<slug>.md` selon les plages d'`index.md`.

Rejouable : supprime les `NN-*.md` avant d'écrire. Un nœud reçoit ses pages
moins celles de ses descendants (le chapitre garde son introduction, les
sous-sections leurs pages). Refuse si une plage chevauche une plage voisine,
dépasse `pages` ou sort de son parent, ou si deux lignes visent le même fichier.
Web : copie `raw/<slug>.md` avec le frontmatter {source, version, url, sha256}.
Refuse un `index.md` dont la `version` diffère de celle de `source.yaml`.
`fidelity: partial` est recopié (avec `fidelity_notes`) dans chaque section.
`recovered/*.md` (frontmatter {source, pages, title, method[, version]} + tableau) est
ajouté en fin de la section la plus profonde qui couvre ses pages.
`redactions: [{section, pattern, replace}]` du yaml est appliqué à la sortie (le texte
brut l'est déjà par `convert` / `redact`) ; une règle qui ne trouve ni son motif ni
son `replace` dans sa section est un refus (caviardage jamais perdu en silence).
Ne change pas le statut : `indexed` est posé par l'humain après validation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import typer
import yaml

from scripts import redact
from scripts import registry as reg
from scripts.convert import PAGE_MARK
from scripts.index import pages_of_raw

app = typer.Typer(add_completion=False, help=__doc__)

LINE_RE = re.compile(
    r"^(?P<indent> *)- (?:§(?P<chapter>\S+) )?(?P<title>.*?)"
    r"(?: (?:p\.(?P<a>\d+)(?:-(?P<b>\d+))?|(?P<url>https?://\S+)))?"
    r" → (?P<file>\S+\.md)(?: :(?: (?P<summary>.*))?)?$"
)
SECTION_FILE_RE = re.compile(r"^\d{2}-.+\.md$")


class SplitError(Exception):
    pass


@dataclass
class Section:
    title: str
    file: str
    level: int
    start: int = 0
    end: int = 0
    chapter: str = ""
    url: str = ""
    summary: str = ""
    children: list["Section"] = field(default_factory=list)


def parse_index(text: str) -> tuple[dict[str, Any], list[Section]]:
    """Frontmatter et arbre de sections d'un index.md."""
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise SplitError("index.md : frontmatter `---` manquant")
    front = yaml.safe_load(m.group(1)) or {}
    roots: list[Section] = []
    stack: list[Section] = []
    for lineno, line in enumerate(m.group(2).splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        lm = LINE_RE.match(line)
        if not lm:
            raise SplitError(f"index.md ligne {lineno} illisible : `{line.strip()}`")
        indent = len(lm.group("indent"))
        if indent % 2:
            raise SplitError(f"index.md ligne {lineno} : indentation impaire")
        level = indent // 2
        start = int(lm.group("a")) if lm.group("a") else 0
        end = int(lm.group("b")) if lm.group("b") else start
        sec = Section(
            title=lm.group("title").strip(), file=lm.group("file"), level=level,
            start=start, end=end, chapter=lm.group("chapter") or "", url=lm.group("url") or "",
            summary=(lm.group("summary") or "").strip(),
        )
        while stack and stack[-1].level >= level:
            stack.pop()
        if level > len(stack):
            raise SplitError(f"index.md ligne {lineno} : niveau {level} sans parent")
        (stack[-1].children if stack else roots).append(sec)
        stack.append(sec)
    return front, roots


def walk(nodes: list[Section]):
    for n in nodes:
        yield n
        yield from walk(n.children)


def check_tree(roots: list[Section], total: int) -> None:
    errors: list[str] = []
    files: dict[str, str] = {}
    for s in walk(roots):
        if s.file in files:
            errors.append(f"`{s.file}` visé par « {files[s.file]} » et « {s.title} »")
        files[s.file] = s.title
        if not SECTION_FILE_RE.match(s.file):
            errors.append(f"« {s.title} » : fichier `{s.file}` doit être de la forme NN-slug.md")
        if s.url:
            continue
        if s.start and s.end < s.start:
            errors.append(f"« {s.title} » : plage p.{s.start}-{s.end} inversée")
        if total and s.end > total:
            errors.append(f"« {s.title} » : p.{s.end} dépasse les {total} pages")

    def check_siblings(nodes: list[Section], parent: Section | None) -> None:
        ranged = [n for n in nodes if n.start]
        for a, b in zip(ranged, ranged[1:]):
            if b.start <= a.end:
                errors.append(f"« {a.title} » p.{a.start}-{a.end} chevauche « {b.title} » p.{b.start}-{b.end}")
        for n in nodes:
            if parent is not None and parent.start and n.start and (n.start < parent.start or n.end > parent.end):
                errors.append(f"« {n.title} » p.{n.start}-{n.end} sort de « {parent.title} » p.{parent.start}-{parent.end}")
            check_siblings(n.children, n)

    check_siblings(roots, None)
    if errors:
        raise SplitError("\n".join(errors))


def own_pages(section: Section) -> list[int]:
    """Pages du nœud moins celles de ses descendants."""
    if not section.start:
        return []
    taken: set[int] = set()
    for child in walk(section.children):
        if child.start:
            taken.update(range(child.start, child.end + 1))
    return [p for p in range(section.start, section.end + 1) if p not in taken]


def section_of_raw(raw_text: str, title: str) -> str:
    """Sans pagination (xlsx, docx) : le bloc `# <title>` de raw.md, sinon tout raw.md.

    `convert` écrit un titre `#` par feuille xlsx ; un index à plusieurs entrées
    sans plage de pages découpe donc par feuille.
    """
    blocks = re.split(r"^(?=# )", raw_text, flags=re.M)
    wanted = title.strip().casefold()
    for block in blocks:
        first = block.split("\n", 1)[0]
        if first.startswith("# ") and first[2:].strip().casefold() == wanted:
            return block
    return raw_text


def _frontmatter(fields: dict[str, Any]) -> str:
    return "---\n" + yaml.safe_dump(fields, sort_keys=False, allow_unicode=True) + "---\n\n"


FRONT_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.S)


def read_front(text: str) -> tuple[dict[str, Any], str]:
    """(frontmatter, corps) d'un md ; frontmatter vide si absent."""
    m = FRONT_RE.match(text)
    if not m:
        return {}, text
    return (yaml.safe_load(m.group(1)) or {}), m.group(2)


def version_mismatch(front: dict[str, Any], data: dict[str, Any]) -> str:
    """Message d'erreur si la version d'index.md diffère du registre, "" sinon."""
    if "version" not in front:
        return "index.md sans `version` dans son frontmatter (réécrire avec `index --force` ou l'ajouter)"
    iv, yv = str(front.get("version") or ""), str(data.get("version") or "")
    if iv != yv:
        return (f"index.md porte la version `{iv}`, source.yaml `{yv}` : "
                "index d'une autre version, le refaire (`index --force`) ou corriger sa version")
    return ""


def section_key(name: str) -> str:
    """`04-utiliser-le-manuel` ou `04-utiliser-le-manuel.md` → nom de fichier."""
    return name if name.endswith(".md") else f"{name}.md"


def _page_range(value: Any) -> tuple[int, int]:
    m = re.fullmatch(r"\s*(\d+)\s*(?:-\s*(\d+))?\s*", str(value))
    if not m:
        raise ValueError(value)
    a = int(m.group(1))
    return a, int(m.group(2) or a)


def recovered_tables(source_id: str, sdir: Path, version: Any = None) -> list[tuple[Path, dict[str, Any], str]]:
    """Fichiers `recovered/*.md` triés : (chemin, frontmatter, tableau).

    Refuse un fichier d'une autre source ou, s'il porte `version`, d'une autre version."""
    rdir = sdir / "recovered"
    out: list[tuple[Path, dict[str, Any], str]] = []
    if not rdir.is_dir():
        return out
    for path in sorted(rdir.glob("*.md")):
        front, body = read_front(path.read_text(encoding="utf-8"))
        missing = [k for k in ("source", "pages", "title") if not front.get(k)]
        if missing:
            raise SplitError(f"{source_id}: recovered/{path.name} sans {', '.join(missing)} dans le frontmatter")
        if front["source"] != source_id:
            raise SplitError(f"{source_id}: recovered/{path.name} porte `source: {front['source']}`")
        if "version" in front and str(front["version"] or "") != str(version or ""):
            raise SplitError(f"{source_id}: recovered/{path.name} porte la version `{front['version']}`, "
                             f"source.yaml `{version}` : relancer la récupération")
        out.append((path, front, body.strip("\n")))
    return out


def covering_section(roots: list[Section], a: int, b: int) -> Section | None:
    """La section la plus profonde dont la plage couvre p.a-b (la première à égalité)."""
    best: Section | None = None
    for s in walk(roots):
        if s.start and s.start <= a and b <= s.end and (best is None or s.level > best.level):
            best = s
    return best


def apply_redactions(source_id: str, data: dict[str, Any], bodies: dict[str, str]) -> None:
    """Caviardage déclaré dans `redactions:` du yaml ; refuse une règle sans effet."""
    for i, r in enumerate(data.get("redactions") or [], 1):
        target = section_key(str(r.get("section", "")))
        if target not in bodies:
            raise SplitError(f"{source_id}: redactions n°{i} vise `{target}`, absent d'index.md")
        new, hit = redact.substitute(bodies[target], r)
        if not hit:
            raise SplitError(f"{source_id}: redactions n°{i} ne trouve rien dans `{target}` "
                             "(texte déplacé ? vérifier la section avant de retirer la règle)")
        bodies[target] = new


def split(source_id: str) -> list[Path]:
    data = reg.load_source(source_id)
    sdir = reg.source_dir(source_id)
    index_path = sdir / "index.md"
    if not index_path.exists():
        raise SplitError(f"{source_id}: index.md absent, lancer `index` d'abord")
    front, roots = parse_index(index_path.read_text(encoding="utf-8"))
    mismatch = version_mismatch(front, data)
    if mismatch:
        raise SplitError(f"{source_id}: {mismatch}")
    total = int(data.get("pages") or 0)
    check_tree(roots, total)
    version = data.get("version", "")
    is_web = data.get("type") == "web"
    partial = reg.fidelity_of(data) == "partial"

    raw_pages: dict[int, str] = {}
    raw_text = ""
    if not is_web:
        raw_path = sdir / "raw.md"
        if not raw_path.exists():
            raise SplitError(f"{source_id}: raw.md absent, lancer `convert` d'abord")
        raw_text = raw_path.read_text(encoding="utf-8")
        raw_pages = pages_of_raw(raw_text)

    # 1. Tout calculer en mémoire : rien n'est écrit si une étape refuse.
    heads: dict[str, dict[str, Any]] = {}
    bodies: dict[str, str] = {}
    for s in walk(roots):
        if is_web:
            candidates = list((sdir / "raw").glob("*.md")) if (sdir / "raw").exists() else []
            match = next((c for c in candidates if c.stem == Path(s.file).stem[3:]), None)
            if match is None:
                match = next((c for c in candidates if yaml_url(c) == s.url), None)
            if match is None:
                raise SplitError(f"{source_id}: aucune page raw/ pour « {s.title} » ({s.url})")
            page_front, body = read_front(match.read_text(encoding="utf-8"))
            fields: dict[str, Any] = {"source": source_id, "version": version, "title": s.title,
                                      "url": s.url or page_front.get("url", ""), "sha256": page_front.get("sha256", "")}
            body = body.lstrip("\n")
        else:
            fields = {"source": source_id, "version": version, "title": s.title}
            if s.chapter:
                fields["chapter"] = s.chapter
            if s.start:
                fields["pages"] = f"{s.start}-{s.end}" if s.end != s.start else str(s.start)
                body = "".join(
                    PAGE_MARK.format(n=p) + "\n" + raw_pages.get(p, "\n") for p in own_pages(s)
                )
            else:
                body = section_of_raw(raw_text, s.title)
            if not body.strip():
                typer.echo(f"  ! {s.file} : aucune page propre (tout est dans les enfants)", err=True)
            body = body.strip("\n") + "\n"
        if partial:
            fields["fidelity"] = "partial"
            fields["fidelity_notes"] = str(data.get("fidelity_notes") or "")
        heads[s.file] = fields
        bodies[s.file] = body

    # 2. Tableaux récupérés (recovered/*.md) en fin de la section qui couvre leurs pages.
    for path, rfront, table in recovered_tables(source_id, sdir, version):
        try:
            a, b = _page_range(rfront["pages"])
        except ValueError:
            raise SplitError(f"{source_id}: recovered/{path.name} : `pages: {rfront['pages']}` illisible (ex. \"16-18\")")
        target = covering_section(roots, a, b)
        if target is None:
            typer.echo(f"  ! recovered/{path.name} : aucune section ne couvre p.{a}-{b}, tableau non fusionné", err=True)
            continue
        method = f", méthode {rfront['method']}" if rfront.get("method") else ""
        bodies[target.file] = (
            bodies[target.file].rstrip("\n")
            + f"\n\n### Tableau récupéré : {rfront['title']}\n\n"
            + f"<!-- recovered/{path.name} p.{rfront['pages']}{method} -->\n\n"
            + table + "\n"
        )

    # 3. Caviardage déclaré dans le yaml.
    apply_redactions(source_id, data, bodies)

    # 4. Écriture.
    for old in sdir.iterdir():
        if old.is_file() and SECTION_FILE_RE.match(old.name):
            old.unlink()
    written: list[Path] = []
    for name, fields in heads.items():
        out = sdir / name
        out.write_text(_frontmatter(fields) + bodies[name], encoding="utf-8")
        written.append(out)
    return written


def yaml_url(path: Path) -> str:
    m = re.match(r"^---\n(.*?)\n---", path.read_text(encoding="utf-8"), re.S)
    return (yaml.safe_load(m.group(1)) or {}).get("url", "") if m else ""


@app.command()
def main(id: str = typer.Argument(..., help="Identifiant de la source.")) -> None:
    """Découpe `raw.md` en sections selon `index.md`."""
    try:
        written = split(id)
    except (SplitError, FileNotFoundError) as exc:
        typer.echo(f"refusé : {exc}", err=True)
        raise typer.Exit(1)
    for w in written:
        typer.echo(f"✓ {w.relative_to(reg.ROOT)}")


if __name__ == "__main__":
    app()

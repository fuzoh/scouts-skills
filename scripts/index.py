"""`index <id>` : squelette `sources/<id>/index.md`, arbre des sections.

Sources de l'arbre : signets du PDF (`toc_source: bookmarks`), sinon titres
markdown de `raw.md` (`toc_source: headings`) ou, avec `--pageindex`, l'arbre
PageIndex Flash sans LLM (`toc_source: pageindex`, venv dédié : `just
install-pageindex`). `toc_source: agent` est posé à la main quand l'arbre est
réécrit. Les résumés restent vides.

Format : frontmatter {source, version, pages, page_offset, toc_source} puis une
ligne par nœud, deux espaces d'indentation par niveau :

    - §3.2 Titre p.18-24 → 04-slug.md : résumé

`p.N` = page physique. `page_offset` = page physique − page imprimée (0 si
inconnu). Un document < 15 pages : une seule entrée `01-contenu.md`.
"""

from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import typer
import yaml

from scripts import registry as reg
from scripts.convert import PAGE_RE

app = typer.Typer(add_completion=False, help=__doc__)

SHORT_DOC = 15
MAX_LEVELS = 3
CHAPTER_RE = re.compile(r"^(?:§\s*)?(?P<num>\d+(?:\.\d+)*)\.?[\s   ]+(?P<title>\S.*)$")
PRINTED_RE = re.compile(r"^(?:page|seite|p\.)?\s*(\d{1,3})$", re.I)


class IndexError_(Exception):
    pass


@dataclass
class Node:
    title: str
    level: int                 # 1 = racine
    start: int                 # page physique
    end: int = 0
    chapter: str = ""
    file: str = ""
    url: str = ""
    summary: str = ""
    children: list["Node"] = field(default_factory=list)


# --------------------------------------------------------------------------- #
# Extraction des titres
# --------------------------------------------------------------------------- #

def clean_title(text: str) -> str:
    text = re.sub(r"\*\*|__|`", "", text)
    text = re.sub(r"[\s   ]+", " ", text).strip(" -–—:")
    return text


def split_chapter(title: str) -> tuple[str, str]:
    """`3.2 Qualifier` → ('3.2', 'Qualifier')."""
    m = CHAPTER_RE.match(title)
    if m and len(m.group("num")) <= 8:
        return m.group("num"), m.group("title").strip()
    return "", title


def pages_of_raw(raw: str) -> dict[int, str]:
    """{page physique: texte} depuis les marqueurs `<!-- p.N -->`."""
    marks = list(PAGE_RE.finditer(raw))
    pages: dict[int, str] = {}
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(raw)
        pages[int(m.group(1))] = raw[m.end():end]
    return pages


def headings_from_raw(raw: str) -> list[tuple[int, int, str]]:
    """[(page, niveau markdown, titre)] après filtrage du bruit."""
    heads: list[tuple[int, int, str]] = []
    for page, text in pages_of_raw(raw).items():
        for m in re.finditer(r"^(#{1,6})\s+(.+?)\s*$", text, re.M):
            title = clean_title(m.group(2))
            if len(title) < 3 or re.fullmatch(r"[\d\W]+", title):
                continue
            heads.append((page, len(m.group(1)), title))
    # titres courants (en-têtes répétés) et doublons sur une même page
    repeated = {t for t, n in Counter(h[2].lower() for h in heads).items() if n > 2}
    heads = [h for h in heads if h[2].lower() not in repeated]
    seen: set[tuple[int, str]] = set()
    out = []
    for h in heads:
        key = (h[0], h[2].lower())
        if key in seen:
            continue
        seen.add(key)
        out.append(h)
    return out


def bookmarks_of_pdf(path: Path) -> list[tuple[int, int, str]]:
    import pymupdf

    with pymupdf.open(path) as doc:
        toc = doc.get_toc()
    return [(max(1, page), level, clean_title(title)) for level, title, page in toc if clean_title(title)]


PAGEINDEX_PYTHON = reg.ROOT / ".venv-pageindex" / "bin" / "python"
PAGEINDEX_SCRIPT = Path(__file__).with_name("pageindex_tree.py")


def pageindex_of_pdf(path: Path) -> list[tuple[int, int, str]]:
    """Arbre PageIndex Flash (sans LLM) via le venv dédié → [(page, niveau, titre)]."""
    if not PAGEINDEX_PYTHON.exists():
        raise IndexError_("PageIndex absent : `just install-pageindex`")
    proc = subprocess.run(
        [str(PAGEINDEX_PYTHON), "-I", str(PAGEINDEX_SCRIPT), str(path)],
        capture_output=True, text=True, cwd=reg.ROOT,
    )
    if proc.returncode != 0:
        raise IndexError_(f"PageIndex a échoué : {proc.stderr.strip()[-500:]}")
    nodes = json.loads(proc.stdout)
    return [(max(1, n["page"]), n["level"], clean_title(n["title"])) for n in nodes if clean_title(n["title"])]


def normalize_levels(heads: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    """Niveaux relatifs 1..MAX_LEVELS ; retire un titre de document isolé en tête."""
    if not heads:
        return []
    ranks = {lvl: i + 1 for i, lvl in enumerate(sorted({h[1] for h in heads}))}
    heads = [(p, ranks[l], t) for p, l, t in heads]
    top = [h for h in heads if h[1] == 1]
    if len(top) == 1 and top[0][0] <= 2 and len(heads) > 1:
        heads = [(p, l - 1, t) for p, l, t in heads if l > 1]
    return [(p, min(l, MAX_LEVELS), t) for p, l, t in heads]


# --------------------------------------------------------------------------- #
# Arbre
# --------------------------------------------------------------------------- #

def build_tree(heads: list[tuple[int, int, str]], total_pages: int) -> list[Node]:
    flat: list[Node] = []
    for page, level, title in heads:
        chapter, title = split_chapter(title)
        flat.append(Node(title=title, level=level, start=page, chapter=chapter))
    # le numéro de chapitre est plus fiable que la police : `2.1` → niveau 2
    numbered = [n for n in flat if n.chapter]
    if len(numbered) >= 2:
        for n in numbered:
            n.level = min(n.chapter.count(".") + 1, MAX_LEVELS)
    for i, node in enumerate(flat):
        node.end = total_pages
        for nxt in flat[i + 1:]:
            if nxt.level <= node.level:
                node.end = max(node.start, nxt.start - 1)
                break
    roots: list[Node] = []
    stack: list[Node] = []
    for node in flat:
        while stack and stack[-1].level >= node.level:
            stack.pop()
        (stack[-1].children if stack else roots).append(node)
        stack.append(node)
    return roots


def walk(nodes: list[Node], depth: int = 0):
    for n in nodes:
        yield n, depth
        yield from walk(n.children, depth + 1)


def assign_files(roots: list[Node]) -> None:
    used: set[str] = set()
    for i, (node, _) in enumerate(walk(roots), start=1):
        base = reg.slugify(node.title, max_len=40) or "section"
        slug, k = base, 2
        while slug in used:
            slug, k = f"{base}-{k}", k + 1
        used.add(slug)
        node.file = f"{i:02d}-{slug}.md"


# --------------------------------------------------------------------------- #
# page_offset
# --------------------------------------------------------------------------- #

def detect_page_offset(pages: dict[int, str]) -> int:
    """Page physique − numéro imprimé, par vote majoritaire ; 0 si rien de net."""
    votes: Counter[int] = Counter()
    for phys, text in pages.items():
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        for cand in lines[:2] + lines[-2:]:
            m = PRINTED_RE.match(cand)
            if m:
                printed = int(m.group(1))
                if 0 < printed <= phys + 5:
                    votes[phys - printed] += 1
                    break
    if not votes:
        return 0
    offset, n = votes.most_common(1)[0]
    return offset if n >= max(3, len(pages) // 4) else 0


# --------------------------------------------------------------------------- #
# Rendu
# --------------------------------------------------------------------------- #

def render(data: dict[str, Any], roots: list[Node], toc_source: str, page_offset: int) -> str:
    front = {
        "source": data["id"],
        "version": data.get("version", ""),
        "pages": data.get("pages", 0),
        "page_offset": page_offset,
        "toc_source": toc_source,
    }
    lines = ["---", yaml.safe_dump(front, sort_keys=False, allow_unicode=True).rstrip(),
             "# p.N = page physique ; page imprimée = p.N - page_offset", "---", ""]
    for node, depth in walk(roots):
        parts = ["  " * depth + "-"]
        if node.chapter:
            parts.append(f"§{node.chapter}")
        parts.append(node.title)
        if node.url:
            parts.append(node.url)
        elif node.start:
            parts.append(f"p.{node.start}" if node.start == node.end else f"p.{node.start}-{node.end}")
        parts.append(f"→ {node.file} : {node.summary}".rstrip())
        lines.append(" ".join(parts))
    return "\n".join(lines) + "\n"


def web_page_title(sdir: Path, page: dict[str, Any]) -> str:
    """Premier titre `#` de raw/<slug>.md (le <title> du manifeste est souvent faux sur une SPA)."""
    raw = sdir / "raw" / f"{page.get('slug')}.md"
    if raw.exists():
        for line in raw.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return clean_title(re.sub(r"<!--.*?-->", "", line[2:]))
    return page.get("title") or page["slug"]


def build_index(source_id: str, pageindex: bool = False) -> tuple[str, str]:
    """Retourne (contenu d'index.md, toc_source). `pageindex` : PDF sans signets via PageIndex."""
    data = reg.load_source(source_id)
    sdir = reg.source_dir(source_id)
    total = int(data.get("pages") or 0)
    title = data.get("title") or source_id
    stype = data.get("type")

    if data.get("extraction") == "catalogue":
        # Catalogue : une ligne par ressource, écrite par l'agent ; web ou pdf.
        roots = [Node(title=title, level=1, start=0 if stype == "web" else 1,
                      end=0 if stype == "web" else (total or 1),
                      url=data.get("url", "") if stype == "web" else "", file="01-contenu.md")]
        return render(data, roots, "agent", 0), "agent"

    if stype == "web":
        roots = [
            Node(title=web_page_title(sdir, p), level=1, start=0, url=p["url"])
            for p in data.get("web_pages") or []
        ]
        if not roots:
            raise IndexError_(f"{source_id}: aucune page web")
        for i, n in enumerate(roots, 1):
            n.file = f"{i:02d}-{reg.slugify(n.title, 40) or 'page'}.md"
        return render(data, roots, "headings", 0), "headings"

    raw_path = sdir / "raw.md"
    if not raw_path.exists():
        raise IndexError_(f"{source_id}: raw.md absent, lancer `convert` d'abord")
    raw = raw_path.read_text(encoding="utf-8")
    pages = pages_of_raw(raw)
    page_offset = detect_page_offset(pages) if stype == "pdf" else 0

    if total == 0 or total < SHORT_DOC:
        node = Node(title=title, level=1, start=1 if total else 0, end=total, file="01-contenu.md")
        return render(data, [node], "headings", page_offset), "headings"

    heads: list[tuple[int, int, str]] = []
    toc_source = "headings"
    if stype == "pdf":
        files = [p for p in reg.original_files(source_id) if p.is_file()]
        if files:
            heads = bookmarks_of_pdf(files[0])
            if heads:
                toc_source = "bookmarks"
            elif pageindex:
                heads = pageindex_of_pdf(files[0])
                if heads:
                    toc_source = "pageindex"
    if not heads:
        heads = headings_from_raw(raw)
        toc_source = "headings"
    heads = normalize_levels(heads)
    if not heads:
        node = Node(title=title, level=1, start=1, end=total, file="01-contenu.md")
        return render(data, [node], "headings", page_offset), "headings"
    roots = build_tree(heads, total)
    assign_files(roots)
    return render(data, roots, toc_source, page_offset), toc_source


@app.command()
def main(
    id: str = typer.Argument(..., help="Identifiant de la source."),
    force: bool = typer.Option(False, "--force", help="Écraser un index.md existant."),
    pageindex: bool = typer.Option(False, "--pageindex", help="PDF sans signets : arbre PageIndex Flash (just install-pageindex)."),
) -> None:
    """Écrit le squelette `index.md` d'une source."""
    out = reg.source_dir(id) / "index.md"
    if out.exists() and not force:
        typer.echo(f"refusé : {out.relative_to(reg.ROOT)} existe (--force pour écraser)", err=True)
        raise typer.Exit(1)
    try:
        text, toc_source = build_index(id, pageindex=pageindex)
    except (IndexError_, FileNotFoundError) as exc:
        typer.echo(f"refusé : {exc}", err=True)
        raise typer.Exit(1)
    out.write_text(text, encoding="utf-8")
    n = sum(1 for l in text.splitlines() if l.lstrip().startswith("- "))
    typer.echo(f"✓ {out.relative_to(reg.ROOT)} ({n} nœud(s), toc_source: {toc_source})")


if __name__ == "__main__":
    app()

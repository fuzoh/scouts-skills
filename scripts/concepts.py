"""`concepts` : génère `docs/concepts/<slug>.md`, un fichier par concept, depuis
les `concepts:` des `source.yaml` (index inversé) et la définition du glossaire.

Un fichier est régénéré à chaque appel, jamais édité à la main. Les anciens
fichiers dont le slug n'est plus utilisé sont supprimés.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import typer

from scripts import registry as reg

app = typer.Typer(add_completion=False, help=__doc__)

OUT = reg.ROOT / "docs" / "concepts"
GLOSSARY = reg.ROOT / "GLOSSARY.md"
STATUSES = ("converted", "indexed", "verified")


def glossary_rows() -> dict[str, dict[str, str]]:
    """{slug: {terme, sigle, definition, source}} depuis le tableau de GLOSSARY.md."""
    rows: dict[str, dict[str, str]] = {}
    if not GLOSSARY.exists():
        return rows
    header: list[str] = []
    for line in GLOSSARY.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not header:
            header = [c.lower() for c in cells]
            continue
        if set(cells[0]) <= {"-", " "}:
            continue
        row = dict(zip(header, cells))
        slug = row.get("slug", "")
        if slug:
            rows[slug.strip("`")] = row
    return rows


def sections_count(sdir: Path) -> int:
    return sum(1 for p in sdir.iterdir() if re.match(r"^\d{2}-.+\.md$", p.name))


def build() -> list[Path]:
    by_concept: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for src in reg.all_sources():
        if src.get("decision") != "keep" or src.get("status") not in STATUSES:
            continue
        for c in src.get("concepts") or []:
            by_concept[c].append(src)

    gloss = glossary_rows()
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.md"):
        if old.stem not in by_concept:
            old.unlink()

    written: list[Path] = []
    for slug, sources in sorted(by_concept.items()):
        g = gloss.get(slug, {})
        title = g.get("terme") or slug.replace("-", " ")
        lines = [f"# {title}", ""]
        if g.get("sigle") and g["sigle"] not in ("—", "-"):
            lines.append(f"Sigle : {g['sigle']}  ")
        if g.get("définition") or g.get("definition"):
            lines.append(g.get("définition") or g.get("definition"))
        else:
            lines.append("_Définition à écrire dans `GLOSSARY.md` (colonne slug)._")
        lines += ["", "## Sources", "",
                  "Chaque source porte le concept dans son `source.yaml` ; ouvrir `index.md` pour choisir la section.", ""]
        for src in sorted(sources, key=lambda s: s["id"]):
            sdir = reg.source_dir(src["id"])
            n = sections_count(sdir)
            ver = f"@{src['version']}" if src.get("version") else ""
            lines.append(f"- `{src['id']}{ver}` — {src['title']} ({n} section{'s' if n != 1 else ''}, "
                         f"[index](../../sources/{src['id']}/index.md))")
        related: Counter[str] = Counter()
        for src in sources:
            for c in src.get("concepts") or []:
                if c != slug:
                    related[c] += 1
        if related:
            lines += ["", "## Concepts liés", ""]
            lines.append(", ".join(f"[{c}]({c}.md)" for c, _ in related.most_common(8)))
        lines.append("")
        out = OUT / f"{slug}.md"
        out.write_text("\n".join(lines), encoding="utf-8")
        written.append(out)

    index = ["# Concepts", "", "Index inversé généré par `just concepts`, un fichier par concept. Ne pas éditer.", ""]
    for slug, sources in sorted(by_concept.items()):
        index.append(f"- [{slug}]({slug}.md) ({len(sources)})")
    (OUT / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    return written


@app.command()
def main() -> None:
    """Génère docs/concepts/<slug>.md depuis les `concepts:` des sources."""
    written = build()
    typer.echo(f"✓ {len(written)} concept(s) → docs/concepts/")


if __name__ == "__main__":
    app()

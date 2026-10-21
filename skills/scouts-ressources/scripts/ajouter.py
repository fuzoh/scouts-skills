#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["pymupdf4llm>=0.0.20,<2", "markitdown[docx,pptx,xlsx]>=0.1"]
# ///
"""Ajoute un document à `scouts-perso/` : original, fiches par titres, ligne d'index.

    uv run ajouter.py FICHIER --dossier {ac,groupe,cours} [--perso DIR] [--titre TITRE]

Contrat : `references/personnaliser.md` (§ 4 procédure, § 6 formats). Le script
copie l'original dans `originaux/`, découpe le texte converti par titres en
fiches de 17 000 caractères au plus, refuse un doublon (même sha256) et ajoute
`| <dossier>/<slug>/ | À COMPLÉTER |` à la table « Fiches » du `README.md`.

Formats : pdf, docx, pptx, xlsx, md, txt. Codes de sortie : 0 succès, 1 refus,
2 usage. Fichier autonome : ne dépend d'aucun autre module du dépôt.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path

LIMIT = 17_000        # caractères par fiche (~ 5 000 tokens)
README_MAX = 7_000    # caractères du README (~ 2 000 tokens)
FORMATS = {".pdf", ".docx", ".pptx", ".xlsx", ".md", ".txt"}
RESERVED = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)), *(f"lpt{i}" for i in range(1, 10))}
HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t#]*$")


class Refus(Exception):
    pass


def slugify(text: str, default: str = "document") -> str:
    """Minuscules, tirets, sans accents, 60 caractères au plus, sûr sous Windows."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60].strip("-")
    if not slug:
        return default
    return slug + "-doc" if slug in RESERVED else slug


# --------------------------------------------------------------------------- #
# Conversion (imports lourds dans les fonctions)
# --------------------------------------------------------------------------- #

def tidy(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def pdf_to_markdown(path: Path) -> str:
    import pymupdf
    import pymupdf4llm

    pymupdf4llm.use_layout(False)  # le mode layout désactive la détection de titres
    parts = []
    with pymupdf.open(path) as doc:
        for i, chunk in enumerate(pymupdf4llm.to_markdown(doc, page_chunks=True, show_progress=False)):
            text = chunk["text"]
            expected = len(doc[i].get_text().split())
            # Graphismes vectoriels qui masquent le texte : reprise sans graphismes.
            if expected >= 20 and len(text.split()) < 0.85 * expected:
                retry = pymupdf4llm.to_markdown(
                    doc, pages=[i], show_progress=False, ignore_graphics=True, ignore_images=True
                )
                if len(retry.split()) > len(text.split()):
                    text = retry
            parts.append(text)
    return "\n\n".join(parts)


def office_to_markdown(path: Path) -> str:
    from markitdown import MarkItDown

    return MarkItDown().convert(str(path)).text_content


def to_markdown(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".pdf":
        text = pdf_to_markdown(path)
    elif ext in (".docx", ".pptx", ".xlsx"):
        text = office_to_markdown(path)
    else:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    return tidy(text)


# --------------------------------------------------------------------------- #
# Découpage
# --------------------------------------------------------------------------- #

def clean_title(raw: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[*_`]|<!--.*?-->", "", raw)).strip()


def headings(text: str, min_level: int = 1) -> list[tuple[int, int, str]]:
    """(position, niveau, titre) des titres de niveau >= min_level, hors blocs de code."""
    found, pos, fence = [], 0, False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
        elif not fence and (m := HEADING.match(line.rstrip("\n"))) and len(m[1]) >= min_level:
            found.append((pos, len(m[1]), clean_title(m[2])))
        pos += len(line)
    return found


def heading_only(text: str) -> bool:
    return all(HEADING.match(ln) for ln in text.splitlines() if ln.strip())


def by_headings(text: str, intro: str, min_level: int, keep_lead: bool = False) -> list[tuple[str, str]] | None:
    """Parties au niveau de titre le plus haut qui en donne au moins deux, sinon None.

    Un préambule fait de titres seuls n'est pas une partie : abandonné, ou
    gardé en tête de la première partie si `keep_lead` (aucune perte).
    """
    heads = headings(text, min_level)
    for level in sorted({h[1] for h in heads}):
        cuts = [h for h in heads if h[1] == level]
        lead = text[: cuts[0][0]]
        has_lead = bool(lead.strip()) and not heading_only(lead)
        if len(cuts) + has_lead < 2:
            continue
        ends = [c[0] for c in cuts[1:]] + [len(text)]
        parts = [(c[2], text[c[0] : end]) for c, end in zip(cuts, ends)]
        if has_lead:
            return [(intro, lead)] + parts
        if keep_lead and lead:
            parts[0] = (parts[0][0], lead + parts[0][1])
        return parts
    return None


def hard_cut(para: str, limit: int) -> list[str]:
    """Paragraphe seul trop long : coupe à une fin de ligne, sinon à un espace."""
    out = []
    while len(para) > limit:
        cut = max(para.rfind("\n", 0, limit), para.rfind(" ", 0, limit))
        cut = cut + 1 if cut > 0 else limit
        out.append(para[:cut])
        para = para[cut:]
    return out + [para]


def pack(text: str, title: str, limit: int) -> list[tuple[str, str]]:
    """Regroupe des paragraphes entiers en chunks <= limit."""
    pieces = []
    for chunk in re.split(r"(?<=\n\n)(?=\S)", text):  # paragraphe + ses sauts de ligne
        pieces += hard_cut(chunk, limit)
    chunks = [""]
    for piece in pieces:
        if chunks[-1] and len(chunks[-1]) + len(piece) > limit:
            chunks.append("")
        chunks[-1] += piece
    return [(f"{title} ({i}/{len(chunks)})", c) for i, c in enumerate(chunks, 1)]


def split_parts(text: str, title: str, limit: int = LIMIT, min_level: int = 1, intro: str = "Introduction",
                prefix: str = "") -> list[tuple[str, str]]:
    """Découpe `text` en (titre, corps) ; la concaténation des corps redonne le texte.

    Seul échappe le préambule de titres seuls du document entier (son titre est
    porté par `document`). Une partie trop longue se recoupe au niveau de titre
    suivant (titre « Parent — Sous-titre »), puis aux paragraphes.
    """
    parts = by_headings(text, intro, min_level, keep_lead=bool(prefix))
    if parts is None:
        return pack(text, title, limit) if len(text) > limit else [(title, text)]
    out = []
    for name, body in parts:
        full = prefix + name if prefix and name != intro else name
        if len(body) <= limit:
            out.append((full, body))
            continue
        first = headings(body)[:1]
        level = first[0][1] if first and first[0][0] == 0 else min_level - 1
        out += split_parts(body, full, limit, level + 1, intro=full, prefix=full + " — ")
    return out


def document_title(text: str, stem: str) -> str:
    return next((t for _, lvl, t in headings(text) if lvl == 1), stem)


# --------------------------------------------------------------------------- #
# Dossier perso
# --------------------------------------------------------------------------- #

def resolve_perso(perso: Path | None) -> Path:
    candidates = [perso] if perso else [Path.cwd() / "scouts-perso", Path.home() / "scouts-perso"]
    for c in candidates:
        if (c / "README.md").is_file():
            return c
    raise Refus("dossier perso introuvable : le créer d'abord (personnaliser.md § 2)")


def known_hashes(perso: Path) -> dict[str, Path]:
    """sha256 du frontmatter de toutes les fiches -> dossier de fiches."""
    found = {}
    for fiche in perso.glob("*/*/*.md"):
        head = fiche.read_text(encoding="utf-8", errors="replace").split("\n---", 1)[0]
        if m := re.search(r"^sha256:\s*(\w+)\s*$", head, re.M):
            found[m[1]] = fiche.parent
    return found


def free_name(directory: Path, name: str) -> str:
    """`name`, ou `stem-2.ext`, `stem-3.ext`… tant que le nom est pris."""
    stem, ext = Path(name).stem, Path(name).suffix
    candidate, n = name, 1
    while (directory / candidate).exists():
        n += 1
        candidate = f"{stem}-{n}{ext}"
    return candidate


def yaml_value(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    if not value or re.search(r"[:#'\"\[\]{}&*!|>%@`,]|^[-?]", value):
        return json.dumps(value, ensure_ascii=False)
    return value


def fiche_text(doc: str, part: str, body: str, original: str, sha: str, today: str) -> str:
    lines = body.lstrip("\n").split("\n", 1)
    if (m := HEADING.match(lines[0])) and clean_title(m[2]) == part:
        body = lines[1] if len(lines) > 1 else ""  # titre déjà porté par `# partie`
    front = (f"---\ndocument: {yaml_value(doc)}\npartie: {yaml_value(part)}\noriginal: {original}\n"
             f"sha256: {sha}\najoute_le: {today}\n---\n\n")
    return f"{front}# {part}\n\n{body.strip(chr(10))}\n"


def add_index_row(readme: str, row: str) -> str:
    lines = readme.rstrip("\n").split("\n")
    start = next((i for i, ln in enumerate(lines) if re.fullmatch(r"##\s+Fiches\s*", ln)), None)
    if start is None:
        return "\n".join(lines) + f"\n\n## Fiches\n| dossier | sert à |\n|---|---|\n{row}\n"
    end = start + 1
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    if end == start + 1:  # section sans table
        lines[end:end] = ["| dossier | sert à |", "|---|---|"]
        end += 2
    lines.insert(end, row)
    return "\n".join(lines) + "\n"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def ajouter(source: Path, dossier: str, perso: Path, titre: str | None = None) -> list[Path]:
    if not source.is_file():
        raise Refus(f"fichier introuvable : {source}")
    if source.suffix.lower() not in FORMATS:
        raise Refus(f"format non pris en charge : {source.suffix or source.name} (pdf, docx, pptx, xlsx, md, txt)")
    data = source.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    if sha in (known := known_hashes(perso)):
        raise Refus(f"déjà ajouté : {known[sha]}")

    text = to_markdown(source)
    doc = re.sub(r"\s+", " ", titre).strip() if titre else document_title(text, source.stem)
    parts = split_parts(text, doc)

    # Tout est calculé avant la première écriture : un refus ne laisse rien.
    originals = perso / "originaux"
    name = free_name(originals, source.name)
    slug = slugify(doc)
    unique = free_name(perso / dossier, slug)
    base = perso / dossier / unique
    today = dt.date.today().isoformat()
    created = []
    if not (originals / name).exists():
        originals.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, originals / name)
        created.append(originals / name)
    for n, (part, body) in enumerate(parts, 1):
        path = base / f"{n:02d}-{slugify(part, 'partie')}.md"
        write(path, fiche_text(doc, part, body, f"originaux/{name}", sha, today))
        created.append(path)

    readme = perso / "README.md"
    new = add_index_row(readme.read_text(encoding="utf-8"), f"| {dossier}/{unique}/ | À COMPLÉTER |")
    write(readme, new)
    if len(new) > README_MAX:
        print(f"avertissement : README.md fait {len(new)} caractères (plus de {README_MAX}) : "
              "raccourcir les « sert à » (personnaliser.md § 5)", file=sys.stderr)
    return created


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Ajoute un document à scouts-perso/ (voir personnaliser.md § 4).")
    ap.add_argument("fichier", type=Path, help="pdf, docx, pptx, xlsx, md ou txt")
    ap.add_argument("--dossier", required=True, choices=["ac", "groupe", "cours"])
    ap.add_argument("--perso", type=Path, help="dossier scouts-perso (défaut : ./scouts-perso puis ~/scouts-perso)")
    ap.add_argument("--titre", help="titre du document (défaut : premier titre #, sinon nom du fichier)")
    args = ap.parse_args(argv)
    try:
        perso = resolve_perso(args.perso)
        created = ajouter(args.fichier, args.dossier, perso, args.titre)
    except Refus as exc:
        print(f"refusé : {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # conversion impossible (fichier corrompu, protégé…)
        print(f"refusé : conversion impossible ({type(exc).__name__}: {exc})", file=sys.stderr)
        return 1
    for path in created:
        print(f"✓ {path}")
    print("Remplacer À COMPLÉTER dans scouts-perso/README.md par le « sert à »")
    return 0


if __name__ == "__main__":
    sys.exit(main())

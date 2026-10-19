"""Benchmark jetable : arbre PageIndex Flash vs squelette `index` vs TDM imprimée.

Deux rôles dans un seul fichier :

    # (a) PageIndex, dans le venv séparé, aucun appel réseau
    .venv-bench/bin/python -I scripts/bench_index.py pageindex <pdf> <out.json> [merge|off]

    # (b) + (c) + comparaison, dans le venv principal ; lance (a) en sous-processus
    uv run python scripts/bench_index.py run <pdf>...

Sorties dans `build/bench/`. Pas d'entry point : script jetable (voir DECISIONS.md).
"""

from __future__ import annotations

import difflib
import json
import re
import subprocess
import sys
import time
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "bench"
BENCH_PY = ROOT / ".venv-bench" / "bin" / "python"


# --------------------------------------------------------------------------- #
# (a) PageIndex — exécuté par .venv-bench/bin/python
# --------------------------------------------------------------------------- #

def _forbid_network() -> None:
    import os
    import socket

    os.environ["LITELLM_LOCAL_MODEL_COST_MAP"] = "True"
    for key in list(os.environ):
        if key.endswith("_API_KEY"):
            del os.environ[key]

    def deny(*_a, **_k):
        raise RuntimeError("bench: appel réseau interdit")

    socket.socket.connect = deny  # type: ignore[method-assign]
    socket.socket.connect_ex = deny  # type: ignore[method-assign]
    socket.create_connection = deny  # type: ignore[assignment]
    socket.getaddrinfo = deny  # type: ignore[assignment]


def run_pageindex(pdf: str, out: str, mode: str = "merge") -> None:
    _forbid_network()
    t0 = time.perf_counter()
    from pageindex.flash import page_index_flash
    t1 = time.perf_counter()
    res = page_index_flash(pdf, summary=False, optimize=False if mode == "off" else mode)
    t2 = time.perf_counter()
    res["_bench"] = {"import_s": round(t1 - t0, 2), "run_s": round(t2 - t1, 2), "mode": mode}
    Path(out).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")


# --------------------------------------------------------------------------- #
# Normalisation et appariement
# --------------------------------------------------------------------------- #

NUM_RE = re.compile(r"^\s*(?:§\s*)?\d+(?:\.\d+)*\.?\s+")


def norm(title: str, keep_num: bool = False) -> str:
    t = title if keep_num else NUM_RE.sub("", NUM_RE.sub("", title))  # « 3.2 3.2 Titre »
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    t = re.sub(r"(\w)-\s+(\w)", r"\1\2", t)          # césure
    t = re.sub(r"[^\w]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def similar(a: str, b: str) -> bool:
    if not a or not b:
        return False
    if a == b:
        return True
    short, long_ = sorted((a, b), key=len)
    if long_.startswith(short) and len(short) >= 0.6 * len(long_):
        return True
    return difflib.SequenceMatcher(None, a, b).ratio() >= 0.85


def compare(ref: list[dict], cand: list[dict]) -> dict:
    """ref/cand : [{title, page, level}] ; level 1 = racine."""
    used: set[int] = set()
    found = page_err = depth_ok = 0
    misses, page_errors = [], []
    for r in ref:
        rn = norm(r["title"])
        head = norm(re.split(r"\s[–:]\s", NUM_RE.sub("", r["title"]))[0])  # titre sans sous-titre
        variants = [rn] + ([head] if head != rn and len(head) >= 8 else [])
        best, best_score = None, 0.0
        for j, c in enumerate(cand):
            if j in used:
                continue
            cn = norm(c["title"])
            if any(similar(v, cn) for v in variants):
                score = difflib.SequenceMatcher(None, rn, cn).ratio() - 0.01 * abs(c["page"] - r["page"])
                if score > best_score:
                    best, best_score = j, score
        if best is None:
            misses.append(r["title"])
            continue
        used.add(best)
        found += 1
        c = cand[best]
        if abs(c["page"] - r["page"]) > 1:
            page_err += 1
            page_errors.append(f"{r['title']} : réf p.{r['page']}, outil p.{c['page']}")
        if c["level"] == r["level"]:
            depth_ok += 1
    synthetic = [c for j, c in enumerate(cand) if j not in used and c.get("synthetic")]
    parasites = [c for j, c in enumerate(cand) if j not in used and not c.get("synthetic")]
    return {
        "ref": len(ref), "nodes": len(cand), "found": found,
        "parasites": len(parasites), "synthetic": len(synthetic),
        "page_err": page_err, "depth_ok": depth_ok,
        "max_depth": max((c["level"] for c in cand), default=0),
        "misses": misses, "page_errors": page_errors,
        "parasite_titles": [c["title"] for c in parasites],
    }


# --------------------------------------------------------------------------- #
# (c) Référence : TDM imprimée
# --------------------------------------------------------------------------- #

def level_of(title: str) -> int:
    m = re.match(r"^\s*(\d+(?:\.\d+)*)\.?\s", title)
    return m.group(1).count(".") + 1 if m else 1


def page_texts(pdf: Path) -> list[str]:
    import pymupdf

    with pymupdf.open(pdf) as doc:
        return [p.get_text() for p in doc]


def toc_le_cours(texts: list[str]) -> list[dict]:
    """Pages 3-5 : entrées sur plusieurs lignes, numéro de page seul sur sa ligne."""
    entries, buf = [], []
    for page in texts[2:5]:
        for line in page.splitlines():
            line = line.strip()
            if not line or re.fullmatch(r"Page \d+|TABLE DES MATI[ÈE]RES", line):
                continue
            if re.fullmatch(r"\d{1,3}", line) or line.startswith("Fehler!"):
                printed = int(line) if line.isdigit() else 0
                entries.append({"title": " ".join(buf), "printed": printed})
                buf = []
            else:
                buf.append(line)
    for e in entries:
        e["title"] = re.sub(r"^(\d+)\.\s+", r"\1. ", e["title"])
        e["level"] = level_of(e["title"])
    # correction à la main : entrée cassée (« Fehler! Textmarke… »), le corps titre « 2. Concevoir un cours » p.8
    for e in entries:
        if e["title"].startswith("2. ") and e["printed"] == 0:
            e["title"], e["printed"] = "2. Concevoir un cours", 8
    return entries


def toc_manuel_esa(texts: list[str]) -> list[dict]:
    """Page 3 : titres sur une ou deux lignes, page seule ou en fin de ligne."""
    entries, buf = [], []
    for line in texts[2].splitlines():
        line = line.strip()
        if not line or line == "Sommaire":
            continue
        m = re.fullmatch(r"(.*?)\s*(\d{1,3})", line)
        if m and (not m.group(1) or re.search(r"\D$", m.group(1))):
            if m.group(1):
                buf.append(m.group(1))
            entries.append({"title": re.sub(r"\s+", " ", " ".join(buf)), "printed": int(m.group(2))})
            buf = []
        else:
            buf.append(line)
    for e in entries:
        e["level"] = level_of(e["title"])
    return entries


def toc_pfadiprofil(texts: list[str]) -> list[dict]:
    """Page 3 : page imprimée seulement pour les chapitres ; sous-chapitres sans page."""
    entries, pending, num = [], None, None
    for line in texts[2].splitlines():
        line = line.strip()
        if not line or line in ("3", "TABLE DES MATIÈRES"):
            continue
        if re.fullmatch(r"\d{2}", line):
            pending = int(line)
            continue
        if re.fullmatch(r"\d+\.\d+", line):
            num = line
            continue
        title = re.sub(r"\s+", " ", f"{num} {line}" if num else line)
        num = None
        entries.append({"title": title, "printed": pending if level_of(title) == 1 else 0,
                        "level": level_of(title)})
        pending = None
    return entries


def printed_to_physical_pfadiprofil(texts: list[str]) -> dict[int, int]:
    """Doubles pages : les deux premières lignes portent les numéros imprimés gauche/droite."""
    mapping: dict[int, int] = {}
    for phys, text in enumerate(texts, start=1):
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        for l in lines[:2]:
            if l.isdigit():
                mapping.setdefault(int(l), phys)
    return mapping


# Correction à la main : titres sans numéro (ou numéro après le titre) dans le corps,
# pages relevées en lisant le PDF (doubles pages 15-19).
MANUAL_PAGES = {
    "212002fr_pfadiprofil": {"4.1": 15, "4.2": 16, "4.3": 17, "4.4": 18, "4.5": 19,
                             "5.2": 23, "5.6": 31, "5.7": 33, "5.8": 35},
}


def locate(title: str, texts: list[str], near: int, skip: int, window: int = 4) -> int | None:
    """Page physique où le titre apparaît, la plus proche de `near` (recherche dans le corps)."""
    key = norm(title, keep_num=True)
    key_short = key[:30]
    order = sorted(range(skip, len(texts)), key=lambda i: abs(i + 1 - near))
    for k in (key, key_short):
        for i in order:
            if near and abs(i + 1 - near) > window:
                continue
            if k in norm(texts[i], keep_num=True):
                return i + 1
    return None


def reference(pdf: Path, texts: list[str]) -> tuple[list[dict], list[str]]:
    name = pdf.name
    notes: list[str] = []
    if name.startswith("01_Le cours"):
        entries, skip, mapping = toc_le_cours(texts), 5, None
    elif name.startswith("Manuel J+S esa"):
        entries, skip, mapping = toc_manuel_esa(texts), 3, None
    elif name.startswith("212002fr_pfadiprofil"):
        entries, skip = toc_pfadiprofil(texts), 3
        mapping = printed_to_physical_pfadiprofil(texts)
    else:
        raise SystemExit(f"pas de référence pour {name}")
    ref, chapter_page = [], 1
    for e in entries:
        if e["printed"]:
            guess = mapping.get(e["printed"], e["printed"]) if mapping else e["printed"]
            chapter_page = guess
            found = locate(e["title"], texts, guess, skip)
        else:  # sous-chapitre sans page imprimée : première occurrence après le chapitre
            guess = 0
            found = None
            for i in range(chapter_page - 1, len(texts)):
                if norm(e["title"], keep_num=True)[:30] in norm(texts[i], keep_num=True):
                    found = i + 1
                    break
        manual = next((v for k, v in MANUAL_PAGES.items() if name.startswith(k)), {})
        num = e["title"].split(" ")[0]
        if not found and num in manual:
            found = manual[num]
            notes.append(f"{e['title']} : page relevée à la main p.{found}")
        page = found or guess
        if found and guess and found != guess:
            notes.append(f"{e['title']} : imprimé→physique p.{guess}, trouvé dans le corps p.{found}")
        if not page:
            notes.append(f"{e['title']} : page introuvable")
        ref.append({"title": e["title"], "page": page, "level": e["level"]})
    return ref, notes


# --------------------------------------------------------------------------- #
# (b) Squelette `index` (signets sinon titres de raw)
# --------------------------------------------------------------------------- #

def index_skeleton(pdf: Path) -> tuple[list[dict], str, str, float]:
    from scripts.convert import pdf_to_markdown
    from scripts.index import (assign_files, bookmarks_of_pdf, build_tree, headings_from_raw,
                               normalize_levels, render, walk)

    t0 = time.perf_counter()
    import pymupdf

    with pymupdf.open(pdf) as doc:
        total = doc.page_count
    heads = bookmarks_of_pdf(pdf)
    toc_source = "bookmarks"
    if not heads:
        heads = headings_from_raw(pdf_to_markdown(pdf))
        toc_source = "headings"
    roots = build_tree(normalize_levels(heads), total)
    assign_files(roots)
    md = render({"id": pdf.stem, "pages": total}, roots, toc_source, 0)
    elapsed = time.perf_counter() - t0
    nodes = [{"title": (f"{n.chapter} " if n.chapter else "") + n.title, "page": n.start, "level": d + 1}
             for n, d in walk(roots)]
    return nodes, toc_source, md, elapsed


def pageindex_nodes(res: dict) -> list[dict]:
    out: list[dict] = []

    def rec(nodes, depth):
        for n in nodes:
            title = n.get("title", "")
            synthetic = title == "Preface" or title.endswith("(intro)")
            # optimize="merge" concatène les titres fusionnés par « ; » : chaque titre reste candidat
            for part in title.split("; ") if not synthetic else [title]:
                out.append({"title": part, "page": n.get("start_index", 0), "level": depth,
                            "synthetic": synthetic})
            rec(n.get("nodes") or [], depth + 1)

    rec(res.get("structure") or [], 1)
    return out


def count_nodes(nodes: list[dict]) -> int:
    return sum(1 + count_nodes(n.get("nodes") or []) for n in nodes)


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #

def slug(pdf: Path) -> str:
    return re.sub(r"[^a-z0-9]+", "-", norm(pdf.stem)).strip("-")[:40]


def run(pdfs: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summary = {}
    for p in pdfs:
        pdf = Path(p).resolve()
        s = slug(pdf)
        texts = page_texts(pdf)
        ref, notes = reference(pdf, texts)
        (OUT / f"{s}.ref.json").write_text(json.dumps({"ref": ref, "notes": notes}, ensure_ascii=False, indent=1),
                                           encoding="utf-8")

        idx_nodes, toc_source, md, idx_s = index_skeleton(pdf)
        (OUT / f"{s}.index.md").write_text(md, encoding="utf-8")

        pi = {}
        for mode in ("merge", "off"):
            out = OUT / f"{s}.pageindex-{mode}.json"
            t0 = time.perf_counter()
            subprocess.run([str(BENCH_PY), "-I", str(Path(__file__).resolve()), "pageindex", str(pdf), str(out), mode],
                           check=True, cwd=ROOT)
            wall = time.perf_counter() - t0
            res = json.loads(out.read_text(encoding="utf-8"))
            cmp = compare(ref, pageindex_nodes(res))
            cmp["nodes"] = count_nodes(res.get("structure") or [])
            cmp.update(toc_source=res.get("toc_source"), run_s=res["_bench"]["run_s"],
                       import_s=res["_bench"]["import_s"], wall_s=round(wall, 2),
                       optimize=res.get("optimize", {}) and {k: res["optimize"][k] for k in
                                                              ("merges", "same_page_merges", "same_page_dropped")})
            pi[mode] = cmp

        idx = compare(ref, idx_nodes)
        idx.update(toc_source=toc_source, run_s=round(idx_s, 2))
        summary[pdf.name] = {"pages": len(texts), "ref_notes": notes, "index": idx,
                             "pageindex_merge": pi["merge"], "pageindex_off": pi["off"]}

    (OUT / "results.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, r in summary.items():
        print(f"\n### {name} ({r['pages']} p., réf. {r['index']['ref']} nœuds)\n")
        print("| outil | source | nœuds | retrouvés | parasites (+synth.) | page ±1 KO | profondeur OK | prof. max | temps |")
        print("|---|---|---|---|---|---|---|---|---|")
        for label, key in (("index", "index"), ("PageIndex merge", "pageindex_merge"), ("PageIndex off", "pageindex_off")):
            c = r[key]
            print(f"| {label} | {c['toc_source']} | {c['nodes']} | {c['found']}/{c['ref']} | {c['parasites']} (+{c['synthetic']}) "
                  f"| {c['page_err']} | {c['depth_ok']}/{c['found']} | {c['max_depth']} | {c['run_s']} s"
                  + (f" (+{c['import_s']} s import)" if "import_s" in c else "") + " |")


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "pageindex":
        run_pageindex(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "merge")
    elif len(sys.argv) >= 3 and sys.argv[1] == "run":
        run(sys.argv[2:])
    else:
        raise SystemExit(__doc__)

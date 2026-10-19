from __future__ import annotations

from pathlib import Path

from scripts import convert, index, ingest, registry as reg


def _ingest(path: Path, sid: str, **kw) -> dict:
    e = ingest.Entry(id=sid, type=kw.pop("type", ""), path=path, **kw)
    ingest.prepare_local(e)
    return ingest.run([e])[0]


def test_short_doc_single_entry(repo: Path, pdf_factory):
    _ingest(pdf_factory("a.pdf", n=4), "cofor-a", title="Checklist", version="v1")
    convert.convert("cofor-a")
    text, toc = index.build_index("cofor-a")
    assert "toc_source: headings" in text and "pages: 4" in text
    assert "- Checklist p.1-4 → 01-contenu.md :" in text


def test_headings_tree_chapters_and_offset(repo: Path, pdf_factory):
    titles = ["", "", "1. Introduction", "", "", "2. Concevoir", "2.1 Objectifs", "", "", "", "", "", "", "", "", "", "3. Évaluer", "", "", ""]
    _ingest(pdf_factory("m.pdf", n=20, titles=titles), "js-m", title="Manuel", version="2024")
    convert.convert("js-m")
    text, toc = index.build_index("js-m")
    assert toc == "headings"
    lines = [l for l in text.splitlines() if l.lstrip().startswith("- ")]
    assert lines[0].startswith("- §1 Introduction p.3-5 → 01-introduction.md")
    assert lines[1].startswith("- §2 Concevoir p.6-16 → 02-concevoir.md")
    assert lines[2].startswith("  - §2.1 Objectifs p.7-16 → 03-objectifs.md")
    assert lines[3].startswith("- §3 Evaluer p.17-20 → 04-evaluer.md") or lines[3].startswith("- §3 Évaluer p.17-20 → 04-evaluer.md")
    assert "page_offset: 0" in text  # numéros imprimés = pages physiques


def test_split_chapter():
    assert index.split_chapter("3.2 Qualifier") == ("3.2", "Qualifier")
    assert index.split_chapter("1.1 Modèle de formation") == ("1.1", "Modèle de formation")
    assert index.split_chapter("2. CONCEVOIR UN COURS") == ("2", "CONCEVOIR UN COURS")
    assert index.split_chapter("Annexe bibliographie") == ("", "Annexe bibliographie")
    assert index.clean_title("**2. CONCEVOIR** **UN COURS**") == "2. CONCEVOIR UN COURS"


def test_page_offset_detection():
    pages = {i: f"Page {i - 2}\ncorps\n" for i in range(3, 20)}
    pages[1] = "couverture"
    pages[2] = "sommaire"
    assert index.detect_page_offset(pages) == 2

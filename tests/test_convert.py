from __future__ import annotations

from pathlib import Path

import pytest

from scripts import convert, ingest, registry as reg


def _ingest(path: Path, sid: str, **kw) -> dict:
    e = ingest.Entry(id=sid, type=kw.pop("type", ""), path=path, **kw)
    ingest.prepare_local(e)
    return ingest.run([e])[0]


def test_pdf_page_markers_and_status(repo: Path, pdf_factory):
    _ingest(pdf_factory("a.pdf", n=3, titles=["Intro", "", "Fin"]), "cofor-a")
    (out,) = convert.convert("cofor-a")
    text = out.read_text()
    assert text.startswith("<!-- p.1 -->")
    assert convert.PAGE_RE.findall(text) == ["1", "2", "3"]
    assert "# Intro" in text or "Intro" in text
    assert reg.load_source("cofor-a")["status"] == "converted"
    # rejouable : écrase raw.md seulement
    (repo / "sources/cofor-a/index.md").write_text("x")
    convert.convert("cofor-a")
    assert (repo / "sources/cofor-a/index.md").read_text() == "x"


def test_refuse_catalogue(repo: Path, pdf_factory):
    _ingest(pdf_factory("a.pdf"), "autre-a")
    data = reg.load_source("autre-a")
    data["extraction"] = "catalogue"
    reg.save_source(data)
    with pytest.raises(convert.ConvertError, match="catalogue"):
        convert.convert("autre-a")


def test_html_anchors_and_frontmatter(repo: Path):
    html = """<html><head><title>Guide</title></head><body><main>
    <h1 id="intro">Introduction générale</h1><p>Un paragraphe assez long pour que trafilatura le garde, avec du texte utile sur le scoutisme suisse.</p>
    <h2 id="methodes">Les méthodes</h2><p>Encore un paragraphe assez long pour que trafilatura le garde, décrivant les méthodes scoutes.</p>
    </main></body></html>"""
    md = convert.html_to_markdown(html, "https://h/guide")
    assert "<!-- #intro -->\n# Introduction générale" in md
    assert "<!-- #methodes -->\n## Les méthodes" in md
    assert "@@ANC" not in md


HTML_RENDERED = """<html><body><main><h1 id="a">Article rendu</h1>
<p>Un paragraphe assez long pour que trafilatura le garde, avec du texte utile sur le scoutisme suisse.</p>
</main></body></html>"""


def test_render_keeps_original(repo: Path, monkeypatch: pytest.MonkeyPatch):
    sdir = repo / "sources/cudesch-spa"
    (sdir / "original").mkdir(parents=True)
    shell = b"<html><body><div id='app'></div></body></html>"
    (sdir / "original/article-01.html").write_bytes(shell)
    data = reg.load_template()
    data.update(id="cudesch-spa", title="SPA", issuer="cudesch", type="web", sha256=reg.sha256_bytes(shell),
                pages=0, version="2026-10-17", retrieved="2026-10-17",
                web_pages=[{"url": "https://h/#!/article/01", "title": "A", "slug": "article-01"}])
    reg.save_source(data)
    monkeypatch.setattr(convert, "render_html", lambda url: HTML_RENDERED)
    (out,) = convert.convert("cudesch-spa", render=True)
    assert (sdir / "original/article-01.html").read_bytes() == shell, "l'original collecté reste intact"
    assert convert.render_path("cudesch-spa", "article-01") == repo / "build/render/cudesch-spa/article-01.html"
    assert "Article rendu" in convert.render_path("cudesch-spa", "article-01").read_text()
    assert "Article rendu" in out.read_text()
    after = reg.load_source("cudesch-spa")
    assert after["sha256"] == reg.sha256_bytes(shell) and str(after["retrieved"]) == "2026-10-17"
    assert reg.original_sha256(after) == after["sha256"]

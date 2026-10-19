from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts import convert, index, ingest, registry as reg, split


def _ingest(path: Path, sid: str, **kw) -> dict:
    e = ingest.Entry(id=sid, type=kw.pop("type", ""), path=path, **kw)
    ingest.prepare_local(e)
    return ingest.run([e])[0]


INDEX = """---
source: js-m
version: '2024'
pages: 20
page_offset: 0
toc_source: agent
# commentaire
---

- §1 Introduction p.1-5 → 01-introduction.md : ouverture
- §2 Concevoir p.6-16 → 02-concevoir.md :
  - §2.1 Objectifs p.8-12 → 03-objectifs.md : les objectifs
  - §2.2 Contenus p.13-16 → 04-contenus.md
- Annexes p.17-20 → 05-annexes.md :
"""


def _setup(repo: Path, pdf_factory, index_text: str = INDEX) -> Path:
    _ingest(pdf_factory("m.pdf", n=20), "js-m", title="Manuel", version="2024")
    convert.convert("js-m")
    sdir = repo / "sources/js-m"
    (sdir / "index.md").write_text(index_text)
    return sdir


def test_parse_index_tree():
    front, roots = split.parse_index(INDEX)
    assert front["toc_source"] == "agent"
    assert [r.title for r in roots] == ["Introduction", "Concevoir", "Annexes"]
    assert roots[0].summary == "ouverture" and roots[0].chapter == "1"
    assert [c.file for c in roots[1].children] == ["03-objectifs.md", "04-contenus.md"]
    assert roots[1].children[1].summary == ""


def test_split_pages_minus_children_and_replay(repo: Path, pdf_factory):
    sdir = _setup(repo, pdf_factory)
    (sdir / "99-vieux.md").write_text("ancien découpage")
    written = split.split("js-m")
    assert not (sdir / "99-vieux.md").exists()
    assert [w.name for w in written] == ["01-introduction.md", "02-concevoir.md", "03-objectifs.md", "04-contenus.md", "05-annexes.md"]
    concevoir = (sdir / "02-concevoir.md").read_text()
    assert convert.PAGE_RE.findall(concevoir) == ["6", "7"], "le chapitre garde ses pages hors sous-sections"
    front = yaml.safe_load(concevoir.split("---")[1])
    assert front == {"source": "js-m", "version": "2024", "title": "Concevoir", "chapter": "2", "pages": "6-16"}
    assert convert.PAGE_RE.findall((sdir / "03-objectifs.md").read_text()) == ["8", "9", "10", "11", "12"]
    assert "corps page 17" in (sdir / "05-annexes.md").read_text()
    assert reg.load_source("js-m")["status"] == "converted", "split ne change pas le statut"


@pytest.mark.parametrize("bad, msg", [
    (INDEX.replace("p.17-20", "p.15-20"), "chevauche"),
    (INDEX.replace("p.17-20", "p.17-25"), "dépasse"),
    (INDEX.replace("p.13-16", "p.13-18"), "sort de"),
    (INDEX.replace("04-contenus.md", "03-objectifs.md"), "visé par"),
])
def test_split_refuses(repo: Path, pdf_factory, bad: str, msg: str):
    _setup(repo, pdf_factory, bad)
    with pytest.raises(split.SplitError, match=msg):
        split.split("js-m")


def test_index_then_split_short_doc(repo: Path, pdf_factory):
    _ingest(pdf_factory("c.pdf", n=4), "cofor-c", title="Checklist", version="v1")
    convert.convert("cofor-c")
    text, _ = index.build_index("cofor-c")
    (repo / "sources/cofor-c/index.md").write_text(text)
    (out,) = split.split("cofor-c")
    assert out.name == "01-contenu.md"
    assert convert.PAGE_RE.findall(out.read_text()) == ["1", "2", "3", "4"]


def test_split_web(repo: Path):
    sdir = repo / "sources/msds-site"
    (sdir / "raw").mkdir(parents=True)
    (sdir / "original").mkdir()
    (sdir / "original/guide.html").write_text("<html/>")
    data = reg.load_template()
    data.update(id="msds-site", title="Site", issuer="msds", type="web", sha256="x", pages=0,
                version="2026-10-17", web_pages=[{"url": "https://h/guide", "title": "Guide", "slug": "guide"}])
    reg.save_source(data)
    (sdir / "raw/guide.md").write_text("---\nurl: https://h/guide\nretrieved: 2026-10-17\nsha256: abc\n---\n\n# Guide\n\ntexte\n")
    text, _ = index.build_index("msds-site")
    assert "- Guide https://h/guide → 01-guide.md :" in text
    (sdir / "index.md").write_text(text)
    (out,) = split.split("msds-site")
    front = yaml.safe_load(out.read_text().split("---")[1])
    assert front == {"source": "msds-site", "version": "2026-10-17", "title": "Guide", "url": "https://h/guide", "sha256": "abc"}
    assert out.read_text().rstrip().endswith("texte")


def _edit(sid: str, **changes) -> None:
    data = reg.load_source(sid)
    data.update(changes)
    reg.save_source(data)


@pytest.mark.parametrize("version_line, msg", [
    ("version: 'v2023'", "version `v2023`, source.yaml `2024`"),
    ("", "sans `version`"),
])
def test_split_refuses_other_version(repo: Path, pdf_factory, version_line: str, msg: str):
    sdir = _setup(repo, pdf_factory, INDEX.replace("version: '2024'", version_line))
    (sdir / "01-introduction.md").write_text("découpage précédent")
    with pytest.raises(split.SplitError, match=msg):
        split.split("js-m")
    assert (sdir / "01-introduction.md").read_text() == "découpage précédent", "rien n'est écrit"


def test_split_propagates_partial_fidelity(repo: Path, pdf_factory):
    sdir = _setup(repo, pdf_factory)
    _edit("js-m", fidelity="partial", fidelity_notes="cases de niveau perdues p.8-9")
    split.split("js-m")
    for name in ("01-introduction.md", "03-objectifs.md"):
        front = yaml.safe_load((sdir / name).read_text().split("---")[1])
        assert front["fidelity"] == "partial" and front["fidelity_notes"] == "cases de niveau perdues p.8-9"
    _edit("js-m", fidelity="complete")
    split.split("js-m")
    assert "fidelity" not in (sdir / "01-introduction.md").read_text()


RECOVERED = """---
source: js-m
pages: "{pages}"
title: {title}
method: icones
---

| Module | Niveau |
|---|---|
| Sécurité | {title} |
"""


def test_split_merges_recovered_tables(repo: Path, pdf_factory, capsys):
    sdir = _setup(repo, pdf_factory)
    rec = sdir / "recovered"
    rec.mkdir()
    (rec / "a-objectifs.md").write_text(RECOVERED.format(pages="9-10", title="Grille A"))
    (rec / "b-intro.md").write_text(RECOVERED.format(pages=3, title="Grille B"))
    (rec / "c-hors.md").write_text(RECOVERED.format(pages="12-14", title="Grille C"))
    split.split("js-m")
    first = (sdir / "03-objectifs.md").read_text()
    split.split("js-m")
    objectifs = (sdir / "03-objectifs.md").read_text()
    assert objectifs == first, "rejouable : pas de double ajout"
    assert objectifs.rstrip().endswith("| Sécurité | Grille A |"), "la plus profonde des sections couvrantes"
    assert "### Tableau récupéré : Grille A" in objectifs
    assert "Grille A" not in (sdir / "02-concevoir.md").read_text()
    assert "### Tableau récupéré : Grille B" in (sdir / "01-introduction.md").read_text()
    # p.12-14 : à cheval sur 2.1 et 2.2, seul le chapitre 2 (p.6-16) couvre
    assert "### Tableau récupéré : Grille C" in (sdir / "02-concevoir.md").read_text()
    (rec / "d-nulle-part.md").write_text(RECOVERED.format(pages="16-18", title="Grille D"))
    split.split("js-m")
    assert "aucune section ne couvre p.16-18" in capsys.readouterr().err
    (rec / "e.md").write_text(RECOVERED.format(pages="2", title="X").replace("source: js-m", "source: js-autre"))
    with pytest.raises(split.SplitError, match="js-autre"):
        split.split("js-m")
    (rec / "e.md").write_text(RECOVERED.format(pages="2", title="X").replace("source: js-m", "source: js-m\nversion: '2019'"))
    with pytest.raises(split.SplitError, match="version `2019`"):
        split.split("js-m")


def test_split_applies_redactions(repo: Path, pdf_factory):
    sdir = _setup(repo, pdf_factory)
    raw = sdir / "raw.md"
    raw.write_text(raw.read_text().replace("corps page 9", "Nom d’utilisateur : expert\nMot de passe : s3cret"))
    rule = {"section": "03-objectifs", "pattern": r"Nom d.utilisateur\s*:\s*\S+\s*\n\s*Mot\sde\spasse\s*:\s*\S+",
            "replace": "[identifiants retirés]"}
    _edit("js-m", redactions=[rule])
    split.split("js-m")
    split.split("js-m")
    text = (sdir / "03-objectifs.md").read_text()
    assert "s3cret" not in text and "[identifiants retirés]" in text
    assert "s3cret" in raw.read_text(), "raw.md intact"
    _edit("js-m", redactions=[dict(rule, section="04-contenus")])
    with pytest.raises(split.SplitError, match="ne trouve rien"):
        split.split("js-m")
    _edit("js-m", redactions=[dict(rule, section="09-absente")])
    with pytest.raises(split.SplitError, match="absent d'index.md"):
        split.split("js-m")


def test_raw_redacted_by_redact_and_convert(repo: Path, pdf_factory):
    from scripts import redact

    sdir = _setup(repo, pdf_factory)
    raw = sdir / "raw.md"
    raw.write_text(raw.read_text().replace("corps page 9", "Nom d’utilisateur : expert\nMot de passe : s3cret"))
    rule = {"section": "03-objectifs", "pattern": r"Nom d.utilisateur\s*:\s*\S+\s*\n\s*Mot\sde\spasse\s*:\s*\S+",
            "replace": "[identifiants retirés]"}
    _edit("js-m", redactions=[rule])
    assert redact.redact_raw("js-m") == [raw]
    assert "s3cret" not in raw.read_text() and "[identifiants retirés]" in raw.read_text()
    assert redact.redact_raw("js-m") == [], "rejouable"
    split.split("js-m")
    assert "[identifiants retirés]" in (sdir / "03-objectifs.md").read_text()

    _edit("js-m", redactions=[dict(rule, pattern="introuvable", replace="[absent]")])
    with pytest.raises(redact.RedactError, match="ne trouve rien"):
        redact.redact_raw("js-m")
    with pytest.raises(convert.ConvertError, match="texte brut supprimé"):
        convert.convert("js-m")
    assert not raw.exists(), "aucun texte non caviardé ne reste"

    _edit("js-m", redactions=[{"section": "03-objectifs", "pattern": r"corps page 9", "replace": "[retiré]"}])
    convert.convert("js-m")
    assert "corps page 9" not in raw.read_text() and "[retiré]" in raw.read_text()

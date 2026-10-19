from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts import ingest, registry as reg


def _ingest(path: Path, sid: str, **kw) -> dict:
    e = ingest.Entry(id=sid, type=kw.pop("type", ""), path=path, **kw)
    ingest.prepare_local(e)
    return ingest.run([e])[0]


def test_ingest_pdf_moves_and_fills(repo: Path, pdf_factory):
    pdf = pdf_factory("314201fr-checklist.pdf", n=4)
    data = _ingest(pdf, "cofor-checklist-cours-base", title="Checklist", ref="314201fr")
    assert not pdf.exists(), "l'original doit être déplacé"
    assert (repo / "sources/cofor-checklist-cours-base/original/314201fr-checklist.pdf").exists()
    saved = yaml.safe_load((repo / "sources/cofor-checklist-cours-base/source.yaml").read_text())
    assert saved["pages"] == 4 and saved["type"] == "pdf"
    assert saved["status"] == "collected" and saved["extraction"] == "text"
    assert saved["sha256"] == data["sha256"] and len(saved["sha256"]) == 64
    assert saved["issuer"] == "cofor" and saved["ref"] == "314201fr"
    assert str(saved["retrieved"]) == reg.today().isoformat()
    assert "# <issuer>-<slug>" in (repo / "sources/cofor-checklist-cours-base/source.yaml").read_text()


def test_refuse_duplicate_sha_and_bad_id(repo: Path, pdf_factory):
    pdf = pdf_factory("a.pdf")
    _ingest(pdf, "cofor-a")
    dup = pdf_factory("a-copie.pdf")  # même contenu → même sha ? non : dates. On teste via copie.
    import shutil
    shutil.copy(repo / "sources/cofor-a/original/a.pdf", dup)
    with pytest.raises(ingest.IngestError, match="doublon"):
        _ingest(dup, "cofor-b")
    assert dup.exists(), "rien n'est déplacé en cas de refus"
    with pytest.raises(ingest.IngestError, match="forme attendue"):
        _ingest(dup, "Cofor_B")
    with pytest.raises(ingest.IngestError, match="déjà présent"):
        _ingest(pdf_factory("c.pdf", n=2), "cofor-a")


def test_new_version_archives_history(repo: Path, pdf_factory):
    _ingest(pdf_factory("v1.pdf", n=2), "msds-profil", version="v1")
    old_sha = reg.load_source("msds-profil")["sha256"]
    _ingest(pdf_factory("v2.pdf", n=3), "msds-profil", version="v2", new_version=True)
    data = reg.load_source("msds-profil")
    assert data["version"] == "v2" and data["pages"] == 3 and data["status"] == "collected"
    assert data["history"][0]["sha256"] == old_sha and data["history"][0]["version"] == "v1"
    assert [p.name for p in reg.original_files("msds-profil")] == ["v2.pdf"]


def test_image_dir_is_copied(repo: Path, tmp_path: Path):
    d = tmp_path / "illus"
    d.mkdir()
    (d / "a.png").write_bytes(b"\x89PNG1")
    (d / "b.png").write_bytes(b"\x89PNG2")
    data = _ingest(d, "msds-illustrations-profil", type="image")
    assert d.exists(), "un dossier d'images est copié, pas déplacé"
    assert data["extraction"] == "vision" and data["pages"] == 0
    assert (repo / "sources/msds-illustrations-profil/original/illus/a.png").exists()


def test_batch_lot_validates_all_before_writing(repo: Path, pdf_factory, tmp_path: Path):
    a, b = pdf_factory("a.pdf"), pdf_factory("b.pdf", n=2)
    lot = [
        {"file": str(a), "id": "cofor-a", "title": "A", "audience": ["formateur"], "themes": ["formation"]},
        {"file": str(b), "id": "bad id"},
    ]
    with pytest.raises(ingest.IngestError):
        ingest.run(ingest.entries_from_lot(lot, tmp_path))
    assert a.exists() and b.exists()
    lot[1]["id"] = "cofor-b"
    created = ingest.run(ingest.entries_from_lot(lot, tmp_path))
    assert [c["id"] for c in created] == ["cofor-a", "cofor-b"]
    assert reg.load_source("cofor-a")["audience"] == ["formateur"]


def test_match_manifest(repo: Path, pdf_factory):
    _ingest(pdf_factory("x.pdf"), "cofor-x")
    _ingest(pdf_factory("y.pdf", n=2), "cofor-y")
    sha_x = reg.load_source("cofor-x")["sha256"]
    manifest = {"files": [
        {"url": "https://h/x.pdf", "name": "x.pdf", "sha256": sha_x, "found_on": "https://h/page"},
        {"url": "https://h/y.pdf", "name": "y.pdf", "sha256": "0" * 64},
    ]}
    report = ingest.match_manifest(manifest)
    x, y = reg.load_source("cofor-x"), reg.load_source("cofor-y")
    assert x["file_url"] == "https://h/x.pdf" and x["url"] == "https://h/page" and x["stale"] is False
    assert y["stale"] is True
    assert any("stale" in r for r in report)


def test_page_slug_fragment():
    from scripts.ingest import _page_slug
    used: set[str] = set()
    assert _page_slug("https://cudeschin.pbs.ch/#!/article/01", used) == "article-01"
    assert _page_slug("https://cudeschin.pbs.ch/#!/article/02", used) == "article-02"
    assert _page_slug("https://hering.scout.ch/fr/abc", used) == "fr-abc"
    assert _page_slug("https://hering.scout.ch/", used) == "index"


def test_new_version_invalidates_derived(repo: Path, pdf_factory, capsys):
    _ingest(pdf_factory("v1.pdf", n=2), "msds-profil", version="v1")
    sdir = repo / "sources/msds-profil"
    for name in ("raw.md", "index.md", "01-contenu.md", "02-annexe.md"):
        (sdir / name).write_text("ancien")
    (sdir / "recovered").mkdir()
    (sdir / "recovered/t.md").write_text("ancien")
    (sdir / "notes-perso.txt").write_text("garde")
    data = reg.load_source("msds-profil")
    data.update(fidelity="partial", fidelity_notes="cases perdues", nature="prescription")
    reg.save_source(data)

    _ingest(pdf_factory("v2.pdf", n=3), "msds-profil", version="v2", new_version=True)
    left = sorted(p.name for p in sdir.iterdir())
    assert left == ["notes-perso.txt", "original", "source.yaml"]
    err = capsys.readouterr().err
    assert "raw.md" in err and "index.md" in err and "01-contenu.md" in err and "recovered/" in err
    assert "nature" in err, "les champs d'applicabilité sont signalés à revoir"
    data = reg.load_source("msds-profil")
    assert data["status"] == "collected" and data["fidelity"] is None and data["fidelity_notes"] == ""
    assert data["nature"] == "prescription"

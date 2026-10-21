from __future__ import annotations

from pathlib import Path

import yaml

from scripts import ingest, inventory, redact, referentiels as refs, registry as reg


def _ingest(path: Path, sid: str, **kw) -> dict:
    e = ingest.Entry(id=sid, type="", path=path, **kw)
    ingest.prepare_local(e)
    return ingest.run([e])[0]


def _edit(sid: str, **changes) -> None:
    data = reg.load_source(sid)
    data.update(changes)
    reg.save_source(data)


def test_valid_registry_writes_inventory(repo: Path, pdf_factory, capsys):
    _ingest(pdf_factory("a.pdf"), "cofor-a", title="A", audience=["formateur"], themes=["formation"])
    _ingest(pdf_factory("b.pdf", n=2), "js-b", title="B", audience=["expert-js"], themes=["sport", "camp"])
    _edit("js-b", extraction="vision", notes="schémas")
    assert inventory.run() == 0
    text = reg.INVENTORY.read_text()
    assert "| `collected` | 2 |" in text
    assert "### `formateur` (1)" in text and "### `sport` (1)" in text
    assert "`vision`" in text and "schémas" in text
    assert inventory.run(check_only=True) == 0


def test_errors_block_generation(repo: Path, pdf_factory, capsys):
    _ingest(pdf_factory("a.pdf"), "cofor-a", title="A", audience=["formateur"], themes=["formation"])
    _edit("cofor-a", themes=["formation", "camp", "sport", "securite"], audience=["parent"], status="bizarre")
    _ingest(pdf_factory("b.pdf", n=2), "autre-b", title="B", audience=["formateur"], themes=["formation"])
    (repo / "sources/autre-b/original/b.pdf").unlink()
    assert inventory.run() == 1
    err = capsys.readouterr().err
    assert "au plus 3 thèmes" in err
    assert "`parent`" in err
    assert "status: bizarre" in err
    assert "issuer_detail" in err
    assert "original/" in err
    assert not reg.INVENTORY.exists()


def test_folder_id_mismatch_and_duplicate_sha(repo: Path, pdf_factory, capsys):
    _ingest(pdf_factory("a.pdf"), "cofor-a", title="A", audience=["formateur"], themes=["formation"])
    (repo / "sources/cofor-a").rename(repo / "sources/cofor-z")
    assert inventory.run(check_only=True) == 1
    assert "dossier `cofor-z` ≠ id `cofor-a`" in capsys.readouterr().err


def _src(pdf_factory, sid: str = "cofor-a", n: int = 2) -> None:
    _ingest(pdf_factory(f"{sid}.pdf", n=n), sid, title="A", version="v1",
            audience=["formateur"], themes=["formation"])


def test_optional_fields_defaults_and_validation(repo: Path, pdf_factory, capsys):
    _src(pdf_factory)
    path = repo / "sources/cofor-a/source.yaml"
    data = yaml.safe_load(path.read_text())
    for key in ("fidelity", "fidelity_notes", "applies_from", "applies_until", "nature", "redactions"):
        data.pop(key, None)
    path.write_text(yaml.safe_dump(data, allow_unicode=True))
    assert inventory.run(check_only=True) == 0, "un yaml sans les champs Phase 3b reste valide"
    _edit("cofor-a", fidelity="partial", fidelity_notes="cases perdues p.2", nature="prescription",
          applies_from="2027-01-01", applies_until=None)
    assert inventory.run(check_only=True) == 0
    _edit("cofor-a", fidelity="partial", fidelity_notes="", nature="obligatoire",
          applies_from="2027-13-01", redactions=[{"section": "01-contenu", "pattern": "(", "replace": ""}])
    assert inventory.run(check_only=True) == 1
    err = capsys.readouterr().err
    assert "fidelity_notes" in err and "nature: obligatoire" in err
    assert "applies_from: 2027-13-01" in err and "regex invalide" in err
    _edit("cofor-a", fidelity="parfois", fidelity_notes="x", nature=None, redactions=[],
          applies_from="2027-01-01", applies_until="2026-01-01")
    assert inventory.run(check_only=True) == 1
    err = capsys.readouterr().err
    assert "fidelity: parfois" in err and "antérieur" in err


def test_hash_recomputed(repo: Path, pdf_factory, capsys):
    _src(pdf_factory)
    assert inventory.run(check_only=True) == 0
    (repo / "sources/cofor-a/original/cofor-a.pdf").write_bytes(b"%PDF modifie")
    assert inventory.run(check_only=True) == 1
    assert "sha256 de l'original" in capsys.readouterr().err


def test_web_hash_is_concat_of_pages(repo: Path, capsys):
    sdir = repo / "sources/msds-site"
    (sdir / "original").mkdir(parents=True)
    (sdir / "original/a.html").write_bytes(b"<a/>")
    (sdir / "original/b.html").write_bytes(b"<b/>")
    data = reg.load_template()
    data.update(id="msds-site", title="Site", issuer="msds", type="web", pages=0, version="2026-10-17",
                sha256=reg.sha256_bytes(b"<a/><b/>"), audience=["formateur"], themes=["formation"],
                web_pages=[{"url": "https://h/a", "title": "A", "slug": "a"},
                           {"url": "https://h/b", "title": "B", "slug": "b"}])
    reg.save_source(data)
    assert inventory.run(check_only=True) == 0
    (sdir / "original/b.html").write_bytes(b"<b>rendu</b>")
    assert inventory.run(check_only=True) == 1
    assert "msds-site: sha256" in capsys.readouterr().err


def test_artefacts_required_by_status(repo: Path, pdf_factory, capsys):
    from scripts import convert, index, split

    _src(pdf_factory)
    sdir = repo / "sources/cofor-a"
    _edit("cofor-a", status="converted")
    assert inventory.run(check_only=True) == 1
    assert "ni `raw.md` ni `raw/`" in capsys.readouterr().err

    convert.convert("cofor-a")
    _edit("cofor-a", status="indexed")
    assert inventory.run(check_only=True) == 1
    assert "`index.md` absent" in capsys.readouterr().err

    text, _ = index.build_index("cofor-a")
    (sdir / "index.md").write_text(text)
    assert inventory.run(check_only=True) == 1
    assert "`01-contenu.md` listée dans index.md mais absente" in capsys.readouterr().err

    split.split("cofor-a")
    assert inventory.run(check_only=True) == 0
    (sdir / "02-vieux.md").write_text("---\nversion: v1\n---\n")
    _edit("cofor-a", version="v2", fidelity="partial", fidelity_notes="tableaux p.2",
          redactions=[{"section": "01-contenu", "pattern": "corps page 1", "replace": "[retiré]"}])
    assert inventory.run(check_only=True) == 1
    err = capsys.readouterr().err
    assert "index.md porte la version `v1`" in err
    assert "`01-contenu.md` à la version `v1`" in err
    assert "sans `fidelity: partial`" in err
    assert "contient encore le texte de redactions n°1" in err
    assert "`02-vieux.md` absent d'index.md" in err

    (sdir / "02-vieux.md").unlink()
    (sdir / "index.md").write_text(text.replace("version: v1", "version: v2"))
    split.split("cofor-a")
    assert inventory.run(check_only=True) == 1, "texte brut encore en clair"
    redact.redact_raw("cofor-a")
    split.split("cofor-a")
    assert inventory.run(check_only=True) == 0

    _edit("cofor-a", status="verified", fidelity=None)
    assert inventory.run(check_only=True) == 1
    assert "`fidelity` doit être renseigné" in capsys.readouterr().err
    _edit("cofor-a", fidelity="complete")
    split.split("cofor-a")
    assert inventory.run(check_only=True) == 0


def test_catalogue_needs_only_index(repo: Path, pdf_factory, capsys):
    from scripts import index

    _src(pdf_factory, "autre-cat")
    _edit("autre-cat", issuer_detail="x", extraction="catalogue", status="indexed")
    assert inventory.run(check_only=True) == 1
    assert "`index.md` absent" in capsys.readouterr().err
    text, _ = index.build_index("autre-cat")
    (repo / "sources/autre-cat/index.md").write_text(text)
    assert inventory.run(check_only=True) == 0


def test_originals_optional_and_raw_redactions(repo: Path, pdf_factory, capsys):
    """Dépôt public : `original/` absent, sha256 non recalculé ; texte brut non caviardé refusé."""
    import shutil

    from scripts import convert

    _src(pdf_factory)
    convert.convert("cofor-a")
    sdir = repo / "sources/cofor-a"
    shutil.rmtree(sdir / "original")
    assert inventory.run(check_only=True) == 0
    assert "1 original(aux) absent(s)" in capsys.readouterr().err

    (sdir / "original").mkdir()
    assert inventory.run(check_only=True) == 1, "original/ présent mais vide : erreur"
    assert "original/" in capsys.readouterr().err
    (sdir / "original").rmdir()

    _edit("cofor-a", redactions=[{"section": "01-contenu", "pattern": "corps page 1", "replace": "[retiré]"}])
    assert inventory.run(check_only=True) == 1
    assert "`raw.md` contient encore le texte de redactions n°1 (lancer `redact cofor-a`)" in capsys.readouterr().err


def test_converted_deja_decoupe_avertit(repo: Path, pdf_factory, capsys):
    from scripts import convert

    _src(pdf_factory)
    convert.convert("cofor-a")
    _edit("cofor-a", status="converted")
    sdir = repo / "sources/cofor-a"
    (sdir / "index.md").write_text("---\nsource: cofor-a\nversion: '1'\n---\n\n- A p.1 → 01-a.md : a\n", encoding="utf-8")
    (sdir / "01-a.md").write_text("# A\n", encoding="utf-8")
    assert inventory.run(check_only=True) == 0
    assert "[converted]" in capsys.readouterr().err


def _catalogues(repo: Path, rows: str) -> None:
    for path in refs.catalogues():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rows, encoding="utf-8")


def test_catalogue_slug_inconnu(repo: Path):
    _catalogues(repo, "| `fantome` | x |\n")
    errors = refs.check_routing()
    assert any("fantome" in e and "sans referentiels/" in e for e in errors)
    assert len(errors) >= 2


def test_catalogue_referentiel_absent(repo: Path):
    (repo / "referentiels" / "toy.md").write_text("---\nslug: toy\nrelu_le: 2026-10-21\n---\n\n", encoding="utf-8")
    _catalogues(repo, "| `autre` | x |\n")
    errors = refs.check_routing()
    assert any("referentiels/toy.md absent du catalogue" in e for e in errors)


def test_relu_le_divergent(repo: Path):
    (repo / "referentiels" / "toy.md").write_text("---\nslug: toy\nrelu_le: 2026-10-21\n---\n\n", encoding="utf-8")
    _catalogues(repo, "| `toy` | x |\n")
    folder = repo / "skills-src" / "scouts" / "referentiels" / "toy"
    folder.mkdir(parents=True)
    (folder / "01-regles.md").write_text(
        "---\nslug: toy\nderive_de: {slug: toy, relu_le: 2026-01-01}\n---\n\n", encoding="utf-8"
    )
    errors = refs.check_routing()
    assert any("derive_de.relu_le `2026-01-01` ≠ relu_le `2026-10-21`" in e for e in errors)

"""`build claude-code --skill scouts-ressources` et `install` sur un dépôt jouet."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts import build, registry as reg
from tests.test_referentiels import _make_source, _write

RES = "scouts-ressources"


def _skill(repo: Path) -> None:
    ref = repo / "skills-src" / "scouts-ressources" / "references"
    ref.mkdir(parents=True)
    (repo / "skills-src" / "scouts-ressources" / "SKILL.md").write_text("---\nname: scouts-ressources\ndescription: x\n---\n# scouts-ressources\n", encoding="utf-8")
    (ref / "reglages.md").write_text("# réglages\n", encoding="utf-8")
    (repo / "GLOSSARY.md").write_text("# Glossaire\n", encoding="utf-8")
    (repo / "docs" / "concepts").mkdir()
    (repo / "docs" / "concepts" / "animation.md").write_text(
        "- [index](../../sources/autre-x-test/index.md)\n", encoding="utf-8")


def _extra(repo: Path, sid: str = "autre-y-test") -> None:
    _make_source(repo, sid)
    d = repo / "sources" / sid
    (d / "raw.md").write_text("brut", encoding="utf-8")
    (d / "original").mkdir()
    (d / "original" / "a.pdf").write_text("pdf", encoding="utf-8")
    (d / "recovered").mkdir()
    (d / "recovered" / "r.md").write_text("r", encoding="utf-8")


@pytest.fixture
def full(repo: Path) -> Path:
    _make_source(repo)
    _extra(repo)
    _skill(repo)
    _write(repo)
    return repo


def test_build_complet(full: Path):
    r = build.build_claude_code(skill=RES)
    root = full / "skills" / "scouts-ressources"
    assert r["sources"] == 2 and r["sections"] == 4 and r["referentiels"] == 1
    for rel in ("SKILL.md", "references/reglages.md", "references/glossaire.md",
                "references/concepts/animation.md", "referentiels/toy.md", "MANIFEST.md",
                "corpus/autre-x-test/index.md", "corpus/autre-y-test/01-a.md"):
        assert (root / rel).is_file(), rel
    assert "autre-y-test" in (root / "MANIFEST.md").read_text(encoding="utf-8")


def test_scope_referentiels(full: Path):
    r = build.build_claude_code("referentiels", skill=RES)
    root = full / "skills" / "scouts-ressources"
    assert r["sources"] == 1
    assert (root / "corpus" / "autre-x-test").is_dir() and not (root / "corpus" / "autre-y-test").exists()


def test_exclusions(full: Path):
    root = build.build_claude_code(skill=RES)["root"]
    names = {p.name for p in root.rglob("*")}
    assert not names & {"raw.md", "original", "recovered", "source.yaml", "a.pdf", "r.md"}


def test_refus_sans_skill_md(full: Path):
    (full / "skills-src" / "scouts-ressources" / "SKILL.md").unlink()
    with pytest.raises(build.BuildError, match="SKILL.md"):
        build.build_claude_code(skill=RES)


def test_refus_citation_absente_du_pack(full: Path):
    (full / "sources" / "autre-x-test" / "source.yaml").write_text(
        yaml.safe_dump({"id": "autre-x-test", "title": "X", "issuer": "autre", "type": "pdf", "status": "converted"}),
        encoding="utf-8")
    with pytest.raises(build.BuildError, match="autre-x-test.*absent du pack"):
        build.build_claude_code(skill=RES)


def test_refus_referentiel_invalide(full: Path):
    (full / "referentiels" / "toy.md").write_text("pas de frontmatter\n", encoding="utf-8")
    with pytest.raises(build.BuildError, match="invalides"):
        build.build_claude_code(skill=RES)


def test_liens_concepts_reecrits(full: Path):
    root = build.build_claude_code(skill=RES)["root"]
    text = (root / "references" / "concepts" / "animation.md").read_text(encoding="utf-8")
    assert "../../corpus/autre-x-test/index.md" in text and "sources/" not in text


def test_rebuild_ne_touche_que_le_pack(full: Path):
    out = full / "skills"
    build.build_claude_code(out=out, skill=RES)
    (out / "scouts-ressources" / "vieux.md").write_text("x", encoding="utf-8")
    (out / "autre.txt").write_text("x", encoding="utf-8")
    build.build_claude_code(out=out, skill=RES)
    assert not (out / "scouts-ressources" / "vieux.md").exists() and (out / "autre.txt").exists()


def test_zip(full: Path):
    import zipfile
    r = build.build_claude_code(make_zip=True, skill=RES)
    names = zipfile.ZipFile(r["zip"]).namelist()
    assert "scouts-ressources/SKILL.md" in names and all(n.startswith("scouts-ressources/") for n in names)


def test_install_cree_le_lien(full: Path, tmp_path: Path):
    build.build_claude_code(skill=RES)
    sd = tmp_path / "home" / "skills"
    assert build.install_link(skills_dir=sd, skill=RES) == "créé"
    assert (sd / "scouts-ressources").resolve() == (full / "skills" / "scouts-ressources").resolve()


def test_install_refuse_dossier_etranger(full: Path, tmp_path: Path):
    build.build_claude_code(skill=RES)
    sd = tmp_path / "home" / "skills"
    (sd / "scouts-ressources").mkdir(parents=True)
    with pytest.raises(build.BuildError, match="existe déjà"):
        build.install_link(skills_dir=sd, skill=RES)


def test_install_idempotent(full: Path, tmp_path: Path):
    build.build_claude_code(skill=RES)
    sd = tmp_path / "home" / "skills"
    build.install_link(skills_dir=sd, skill=RES)
    assert build.install_link(skills_dir=sd, skill=RES) == "déjà installé"


def test_injection_metadonnees_index(full: Path):
    sy = full / "sources" / "autre-x-test" / "source.yaml"
    data = yaml.safe_load(sy.read_text(encoding="utf-8"))
    data.update({"ref": "123fr", "nature": "prescription", "applies_from": "2026-01-01",
                 "fidelity": "partial", "extraction": "text", "url": "https://x.ch/a"})
    sy.write_text(yaml.safe_dump(data), encoding="utf-8")
    root = build.build_claude_code(skill=RES)["root"]
    text = (root / "corpus" / "autre-x-test" / "index.md").read_text(encoding="utf-8")
    front = yaml.safe_load(text.split("---\n")[1])
    assert front["version"] == "1" and front["source"] == "x"
    assert front["title"] == "X" and front["issuer"] == "autre" and front["ref"] == "123fr"
    assert front["nature"] == "prescription" and str(front["applies_from"]) == "2026-01-01"
    assert front["fidelity"] == "partial" and front["url"] == "https://x.ch/a"
    assert "applies_until" not in front and "file_url" not in front
    assert "- §1 A p.1-2 → 01-a.md" in text
    other = (root / "corpus" / "autre-y-test" / "index.md").read_text(encoding="utf-8")
    assert "fidelity: complete" in other


def test_catalogue_index_seul(full: Path):
    """Une source `extraction: catalogue` n'embarque que son index.md."""
    sid = "autre-cat-test"
    _make_source(full, sid)
    yml = full / "sources" / sid / "source.yaml"
    data = yaml.safe_load(yml.read_text(encoding="utf-8"))
    data["extraction"] = "catalogue"
    yml.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    for p in (full / "sources" / sid).glob("0*.md"):
        p.unlink()
    root = build.build_claude_code(skill=RES)["root"]
    corpus = root / "corpus" / sid
    assert (corpus / "index.md").is_file()
    assert sorted(p.name for p in corpus.iterdir()) == ["index.md"]


def test_build_deterministe_et_versionne(full: Path):
    """Deux builds identiques octet pour octet ; version du pyproject injectée, sans date."""
    r1 = build.build_claude_code(make_zip=True, skill=RES)
    assert r1["zip"] == full / "dist" / "scouts-ressources.zip"
    first = r1["zip"].read_bytes()
    skill = (r1["root"] / "SKILL.md").read_text(encoding="utf-8")
    front = yaml.safe_load(skill.split("---\n")[1])
    assert front["name"] == "scouts-ressources" and front["metadata"]["version"] == "1.2.3"
    assert front["license"].startswith("CC-BY-SA-4.0")
    assert 'version: "1.2.3" # x-release-please-version' in skill
    manifest = (r1["root"] / "MANIFEST.md").read_text(encoding="utf-8")
    assert "- version : 1.2.3 <!-- x-release-please-version -->" in manifest and "date" not in manifest
    r2 = build.build_claude_code(make_zip=True, skill=RES)
    assert r2["zip"].read_bytes() == first


def test_build_refuse_metadata_dans_la_source(full: Path):
    src = full / "skills-src" / "scouts-ressources" / "SKILL.md"
    src.write_text("---\nname: scouts-ressources\ndescription: x\nmetadata:\n  version: '9'\n---\n", encoding="utf-8")
    with pytest.raises(build.BuildError, match="injecté par `build`"):
        build.build_claude_code(skill=RES)


def test_scripts_copies_tels_quels_dans_le_pack(full: Path):
    sc = full / "skills-src" / "scouts-ressources" / "scripts"
    (sc / "sous").mkdir(parents=True)
    (sc / "ajouter.py").write_text("print('x')\n", encoding="utf-8")
    (sc / "sous" / "data.json").write_bytes(b"{}\x00")
    root = build.build_claude_code(skill=RES)["root"]
    assert (root / "scripts" / "ajouter.py").read_text(encoding="utf-8") == "print('x')\n"
    assert (root / "scripts" / "sous" / "data.json").read_bytes() == b"{}\x00"


def test_zip_exclut_scripts(full: Path):
    import zipfile
    sc = full / "skills-src" / "scouts-ressources" / "scripts"
    sc.mkdir()
    (sc / "ajouter.py").write_text("print('x')\n", encoding="utf-8")
    r = build.build_claude_code(make_zip=True, skill=RES)
    assert (r["root"] / "scripts" / "ajouter.py").is_file()
    names = zipfile.ZipFile(r["zip"]).namelist()
    assert "scouts-ressources/SKILL.md" in names
    assert not any(n.startswith("scouts-ressources/scripts") for n in names)


def test_sans_scripts_pas_de_dossier(full: Path):
    assert not (build.build_claude_code(skill=RES)["root"] / "scripts").exists()

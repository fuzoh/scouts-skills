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


def test_personnaliser_partage(full: Path):
    """`personnaliser.md` a une seule source, `skills-src/scouts/references/`, copiée dans le pack."""
    src = full / "skills-src" / "scouts" / "references"
    src.mkdir(parents=True)
    (src / "personnaliser.md").write_text("# Personnaliser\n", encoding="utf-8")
    root = build.build_claude_code(skill=RES)["root"]
    assert (root / "references" / "personnaliser.md").read_text(encoding="utf-8") == "# Personnaliser\n"
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


def test_suffixe_ressources(full: Path):
    import zipfile
    r = build.build_claude_code(make_zip=True, skill=RES, suffixe="monac")
    root = full / "skills" / "scouts-ressources-monac"
    assert r["root"] == root and not (full / "skills" / "scouts-ressources").exists()
    front = yaml.safe_load((root / "SKILL.md").read_text(encoding="utf-8").split("---\n")[1])
    assert front["name"] == "scouts-ressources-monac" and front["metadata"]["version"] == "1.2.3"
    assert "- nom : scouts-ressources-monac" in (root / "MANIFEST.md").read_text(encoding="utf-8")
    assert r["zip"] == full / "dist" / "scouts-ressources-monac.zip"
    names = zipfile.ZipFile(r["zip"]).namelist()
    assert "scouts-ressources-monac/SKILL.md" in names
    assert all(n.startswith("scouts-ressources-monac/") for n in names)


def test_sans_suffixe_pas_de_ligne_nom(full: Path):
    root = build.build_claude_code(skill=RES)["root"]
    assert "- nom :" not in (root / "MANIFEST.md").read_text(encoding="utf-8")


@pytest.mark.parametrize("bad", ["Monac", "mo_nac", "-a", "a-", "a--b", "", "é", "x" * 60])
def test_suffixe_invalide(full: Path, bad: str):
    with pytest.raises(build.BuildError, match="suffixe"):
        build.build_claude_code(skill=RES, suffixe=bad)


def test_install_suffixe(full: Path, tmp_path: Path):
    build.build_claude_code(skill=RES, suffixe="monac")
    sd = tmp_path / "home" / "skills"
    assert build.install_link(skills_dir=sd, skill=RES, suffixe="monac") == "créé"
    assert (sd / "scouts-ressources-monac").resolve() == (full / "skills" / "scouts-ressources-monac").resolve()
    assert not (sd / "scouts-ressources").exists()


# --- --perso -----------------------------------------------------------------------------------

README = """# scouts-perso

Personnalisation des skills scouts. Rester court.

## Profil
- **rôle** : responsable
- **branche** : éclaireurs

## Réglages
Clés de `references/reglages.md` du skill ; la valeur remplace celle du skill.
- **adresse** : tutoiement
- **longueur_avis** : 5 lignes

## Règles locales
Une ligne : règle — origine.
- Départ du camp avant 8 h — décision de la maîtrise

## Contacts
| rôle | nom | joignable | pour |
|---|---|---|---|
| coach | Prénom Nom | 000 | questions |

## Fiches
| dossier | sert à |
|---|---|
| groupe/statuts/ | Statuts du groupe : cotisations |
| ac/directives/ | Directives de l'association cantonale |
"""
REGLAGES = ("# réglages\n\n## Ton\n- **adresse** : vouvoiement neutre\n- **langue** : français\n\n"
            "## Longueur\n- **longueur_avis** : 8 lignes — verdict\n")


def make_perso(base: Path, readme: str = README) -> Path:
    d = base / "scouts-perso"
    (d / "groupe" / "statuts").mkdir(parents=True)
    (d / "ac" / "directives").mkdir(parents=True)
    (d / "originaux").mkdir()
    (d / "README.md").write_text(readme, encoding="utf-8")
    (d / "groupe" / "statuts" / "01-cotisations.md").write_text("# Cotisations\n\ntexte\n", encoding="utf-8")
    (d / "ac" / "directives" / "01-a.md").write_text("# A\n", encoding="utf-8")
    (d / "originaux" / "statuts.pdf").write_bytes(b"%PDF")
    return d


@pytest.fixture
def perso(full: Path, tmp_path: Path) -> Path:
    (full / "skills-src" / "scouts-ressources" / "references" / "reglages.md").write_text(REGLAGES, encoding="utf-8")
    return make_perso(tmp_path)


def test_perso_exige_suffixe(full: Path, perso: Path):
    with pytest.raises(build.BuildError, match="--suffixe"):
        build.build_claude_code(skill=RES, perso=perso)
    assert not (full / "skills").exists() and not (full / "build").exists()


def test_perso_sortie_par_defaut_build(full: Path, perso: Path):
    r = build.build_claude_code(skill=RES, perso=perso, suffixe="monac")
    assert r["root"] == full / "build" / "scouts-ressources-monac"
    assert not (full / "skills").exists()


def test_perso_reglages_remplaces(full: Path, perso: Path):
    root = build.build_claude_code(skill=RES, perso=perso, suffixe="monac")["root"]
    text = (root / "references" / "reglages.md").read_text(encoding="utf-8")
    assert "- **adresse** : tutoiement\n" in text and "vouvoiement" not in text
    assert "- **longueur_avis** : 5 lignes\n" in text and "8 lignes" not in text
    assert "- **langue** : français\n" in text


def test_perso_cle_inconnue(full: Path, perso: Path):
    (perso / "README.md").write_text(README.replace("- **adresse**", "- **inconnue**"), encoding="utf-8")
    with pytest.raises(build.BuildError, match="inconnue"):
        build.build_claude_code(skill=RES, perso=perso, suffixe="monac")


def test_perso_md_sans_reglages_et_chemins_reecrits(full: Path, perso: Path):
    root = build.build_claude_code(skill=RES, perso=perso, suffixe="monac")["root"]
    text = (root / "references" / "perso.md").read_text(encoding="utf-8")
    assert "## Réglages" not in text and "tutoiement" not in text
    for rubrique in ("## Profil", "## Règles locales", "## Contacts", "## Fiches"):
        assert rubrique in text
    assert "| perso/groupe/statuts/ | Statuts du groupe" in text
    assert "| perso/ac/directives/ |" in text and "| groupe/statuts/" not in text
    assert text.splitlines()[0] == "# scouts-perso" and "construite" in text.splitlines()[2]


def test_perso_fiches_copiees_sans_originaux(full: Path, perso: Path):
    root = build.build_claude_code(skill=RES, perso=perso, suffixe="monac")["root"]
    assert (root / "perso" / "groupe" / "statuts" / "01-cotisations.md").read_text(encoding="utf-8") == "# Cotisations\n\ntexte\n"
    assert (root / "perso" / "ac" / "directives" / "01-a.md").is_file()
    assert not any(p.name in ("originaux", "statuts.pdf") for p in root.rglob("*"))


def test_perso_a_completer_refuse(full: Path, perso: Path):
    (perso / "README.md").write_text(README.replace("Statuts du groupe : cotisations", "À COMPLÉTER"), encoding="utf-8")
    with pytest.raises(build.BuildError, match="À COMPLÉTER"):
        build.build_claude_code(skill=RES, perso=perso, suffixe="monac")


def test_perso_dossier_de_fiches_absent(full: Path, perso: Path):
    import shutil
    shutil.rmtree(perso / "ac" / "directives")
    with pytest.raises(build.BuildError, match="ac/directives"):
        build.build_claude_code(skill=RES, perso=perso, suffixe="monac")


def test_perso_sans_readme(full: Path, perso: Path):
    (perso / "README.md").unlink()
    with pytest.raises(build.BuildError, match="README.md"):
        build.build_claude_code(skill=RES, perso=perso, suffixe="monac")


def test_perso_trop_long_avertit(full: Path, perso: Path):
    (perso / "README.md").write_text(README + "- x\n" * 2000, encoding="utf-8")
    r = build.build_claude_code(skill=RES, perso=perso, suffixe="monac")
    assert any("perso.md" in w and "7000" in w for w in r["warnings"])


def test_perso_zip_suffixe_dans_dist(full: Path, perso: Path):
    import zipfile
    r = build.build_claude_code(skill=RES, perso=perso, suffixe="monac", make_zip=True)
    assert r["zip"] == full / "dist" / "scouts-ressources-monac.zip"
    names = zipfile.ZipFile(r["zip"]).namelist()
    assert "scouts-ressources-monac/references/perso.md" in names
    assert "scouts-ressources-monac/perso/groupe/statuts/01-cotisations.md" in names


def test_perso_install_trouve_build(full: Path, perso: Path, tmp_path: Path):
    build.build_claude_code(skill=RES, perso=perso, suffixe="monac")
    sd = tmp_path / "home" / "skills"
    assert build.install_link(skills_dir=sd, skill=RES, suffixe="monac") == "créé"
    assert (sd / "scouts-ressources-monac").resolve() == (full / "build" / "scouts-ressources-monac").resolve()

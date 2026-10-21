"""`light check` et `build claude-code --skill scouts` sur un squelette jouet."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

from scripts import build, light

REF = """---
slug: {slug}
derive_de: {slug}
statut: brouillon
---
# Réf

## Non-négociables
N1. [tous] Règle un (règlement de camp MSdS).
N2. [tous] Règle deux.

## Selon la date
| a | b |

## Critères de qualité
Q1. Un.

## Pièges
- Piège.

## Trame de conception
- Rubrique.
"""
SAVOIR = "---\ntitre: T\ntheme: formation\nsert_a: Répondre\nderive_de: [x]\nstatut: brouillon\n---\n## Titre\ntexte\n"
SKILL = "---\nname: scouts\ndescription: Un skill.\n---\n# scouts\n"


def make_skeleton(root: Path) -> Path:
    (root / "referentiels").mkdir(parents=True)
    (root / "savoirs").mkdir()
    (root / "references").mkdir()
    (root / "SKILL.md").write_text(SKILL, encoding="utf-8")
    (root / "referentiels" / "ua").mkdir()
    head, _, tail = REF.format(slug="ua").partition("## Selon la date")
    (root / "referentiels" / "ua" / "01-a.md").write_text(head, encoding="utf-8")
    (root / "referentiels" / "ua" / "02-b.md").write_text("## Selon la date" + tail, encoding="utf-8")
    (root / "savoirs" / "formation.md").write_text(SAVOIR, encoding="utf-8")
    (root / "references" / "reglages.md").write_text("# réglages\n", encoding="utf-8")
    return root


@pytest.fixture
def skel(tmp_path: Path) -> Path:
    return make_skeleton(tmp_path / "scouts")


def test_squelette_valide(skel: Path):
    rep = light.check(skel)
    assert rep.errors == [] and rep.files == 5


def test_trop_de_fichiers(skel: Path):
    # 100 fichiers dans le pack, dont MANIFEST.md ajouté par le build : 99 dans la source
    for i in range(94):
        (skel / "references" / f"x{i}.txt").write_text("x", encoding="utf-8")
    assert light.check(skel).errors == []
    (skel / "references" / "x.txt").write_text("x", encoding="utf-8")
    assert any("100 fichiers (max 99" in e for e in light.check(skel).errors)
    assert light.check(skel, max_files=300).errors == []


def test_budget_de_tokens(skel: Path):
    p = skel / "references" / "reglages.md"
    p.write_text("a" * 17_500, encoding="utf-8")  # 17 500 / 3,5 = 5 000
    assert light.check(skel).errors == []
    p.write_text("a" * 17_501, encoding="utf-8")
    assert any("~5001 tokens (max 5000)" in e for e in light.check(skel).errors)


def test_budget_unique_sans_exception(skel: Path):
    front = SAVOIR.split("\n---\n")[0] + "\n---\n"
    p = skel / "savoirs" / "formation-cours-base.md"
    p.write_text(front + "a" * 18_000, encoding="utf-8")
    assert any("formation-cours-base.md" in e and "(max 5000)" in e for e in light.check(skel).errors)


def test_skill_md_trop_long(skel: Path):
    (skel / "SKILL.md").write_text(SKILL + "ligne\n" * 500, encoding="utf-8")
    assert any("lignes (max 500)" in e for e in light.check(skel).errors)


def test_taille_des_fichiers(skel: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(light, "MAX_FILE_BYTES", 100)
    monkeypatch.setattr(light, "MAX_TOTAL_BYTES", 150)
    (skel / "references" / "gros.txt").write_text("x" * 101, encoding="utf-8")
    errors = "\n".join(light.check(skel).errors)
    assert "gros.txt" in errors and "au total" in errors


@pytest.mark.parametrize("ext", [".docx", ".doc", ".xlsx", ".XLS"])
def test_format_binaire_refuse(skel: Path, ext: str):
    (skel / "references" / f"modele{ext}").write_bytes(b"PK")
    assert any("refusé par Gemini" in e for e in light.check(skel).errors)


def test_un_seul_skill_md(skel: Path):
    (skel / "references" / "skill.md").write_text(SKILL, encoding="utf-8")
    assert any("un seul admis" in e for e in light.check(skel).errors)


def test_script_reseau(skel: Path):
    (skel / "scripts").mkdir()
    (skel / "scripts" / "ok.py").write_text("print(1)\n", encoding="utf-8")
    assert light.check(skel, scripts_ok=True).errors == []
    (skel / "scripts" / "web.py").write_text("import requests\n", encoding="utf-8")
    assert any("appel réseau" in e for e in light.check(skel, scripts_ok=True).errors)


def test_scripts_refuse_dans_scouts(skel: Path):
    assert not any("scripts/" in e for e in light.check(skel).errors)
    (skel / "scripts").mkdir()
    (skel / "scripts" / "ajouter.py").write_text("print(1)\n", encoding="utf-8")
    errors = light.check(skel).errors
    assert any("scripts/" in e and "scouts-ressources" in e for e in errors)



def test_build_scouts_refuse_scripts(repo: Path, tmp_path: Path):
    root = make_skeleton(repo / "skills-src" / "scouts")
    (root / "scripts").mkdir()
    (root / "scripts" / "ajouter.py").write_text("print(1)\n", encoding="utf-8")
    with pytest.raises(build.BuildError, match="scripts/"):
        build.build_claude_code(out=tmp_path / "out", skill="scouts")


@pytest.mark.parametrize("bad", ["`msds-x#03-abc`", "voir corpus/x", "voir p.12"])
def test_citation_interdite(skel: Path, bad: str):
    (skel / "references" / "reglages.md").write_text(f"# r\n{bad}\n", encoding="utf-8")
    assert any("interdit" in e for e in light.check(skel).errors)


def test_section_manquante(skel: Path):
    p = skel / "referentiels" / "ua" / "02-b.md"
    p.write_text(p.read_text(encoding="utf-8").replace("## Pièges", "## Autre"), encoding="utf-8")
    assert any("`## Pièges` manquante" in e for e in light.check(skel).errors)


def test_sections_hors_ordre_et_n_non_contigus(skel: Path):
    p = skel / "referentiels" / "ua" / "01-a.md"
    p.write_text(p.read_text(encoding="utf-8").replace("N2.", "N3."), encoding="utf-8")
    assert any("non contiguë" in e for e in light.check(skel).errors)


def test_slug_et_frontmatter(skel: Path):
    p = skel / "referentiels" / "ua" / "01-a.md"
    p.write_text(p.read_text(encoding="utf-8").replace("slug: ua", "slug: autre"), encoding="utf-8")
    (skel / "savoirs" / "formation.md").write_text("pas de front", encoding="utf-8")
    (skel / "SKILL.md").write_text("---\nname: scout-light\ndescription: x\n---\n", encoding="utf-8")
    errors = "\n".join(light.check(skel).errors)
    assert "slug" in errors and "frontmatter" in errors and "doit valoir" in errors


def test_description(skel: Path):
    (skel / "SKILL.md").write_text(f"---\nname: scouts\ndescription: {'a' * 1025}\n---\n", encoding="utf-8")
    assert any("1025 caractères" in e for e in light.check(skel).errors)
    (skel / "SKILL.md").write_text(f"---\nname: scouts\ndescription: {'a' * 1024}\n---\n", encoding="utf-8")
    rep = light.check(skel)
    assert rep.errors == [] and any("claude.ai" in w for w in rep.warnings)
    (skel / "SKILL.md").write_text(f"---\nname: scouts\ndescription: {'a' * 200}\n---\n", encoding="utf-8")
    assert light.check(skel).warnings == []


def test_referentiel_a_plat(skel: Path):
    import shutil
    shutil.rmtree(skel / "referentiels" / "ua")
    (skel / "referentiels" / "ua.md").write_text(REF.format(slug="ua"), encoding="utf-8")
    assert light.check(skel).errors == []


def test_cli(skel: Path):
    r = CliRunner().invoke(light.app, ["check", "--root", str(skel), "--table"])
    assert r.exit_code == 0 and "✓ scouts : 5 fichiers" in r.output and "tokens" in r.output
    (skel / "SKILL.md").unlink()
    assert CliRunner().invoke(light.app, ["check", "--root", str(skel)]).exit_code == 1


def test_build_light(repo: Path, tmp_path: Path):
    make_skeleton(repo / "skills-src" / "scouts")
    out = tmp_path / "out"
    r = build.build_claude_code(out=out, make_zip=True, skill="scouts")
    root = out / "scouts"
    assert r["root"] == root and (root / "SKILL.md").is_file() and (root / "savoirs" / "formation.md").is_file()
    assert not (root / "corpus").exists()
    manifest = (root / "MANIFEST.md").read_text(encoding="utf-8")
    assert "fichiers : 6" in manifest and "`ua` : derive_de `ua`" in manifest
    with zipfile.ZipFile(repo / "dist" / "scouts.zip") as z:
        assert "scouts/SKILL.md" in z.namelist()
    assert build.install_link(out, tmp_path / "sk", "scouts") == "créé"
    assert (tmp_path / "sk" / "scouts").resolve() == root.resolve()


def test_build_light_refuse_si_erreur(repo: Path, tmp_path: Path):
    root = make_skeleton(repo / "skills-src" / "scouts")
    (root / "references" / "reglages.md").write_text("`msds-x#03-abc`", encoding="utf-8")
    with pytest.raises(build.BuildError, match="scouts invalide"):
        build.build_claude_code(out=tmp_path / "out", skill="scouts")


def test_index(skel: Path):
    r = CliRunner().invoke(light.app, ["index", "--root", str(skel)])
    assert r.exit_code == 0
    readme = skel / "savoirs" / "README.md"
    assert readme.exists() and "## Formation" in readme.read_text(encoding="utf-8")
    # le README généré n'a pas de frontmatter et ne doit pas faire échouer le check
    assert light.check(skel).errors == []


def test_theme_inconnu(skel: Path):
    p = skel / "savoirs" / "formation.md"
    p.write_text(SAVOIR.replace("theme: formation", "theme: cuisine"), encoding="utf-8")
    assert any("`theme` `cuisine` inconnu" in e for e in light.check(skel).errors)


def test_theme_manquant(skel: Path):
    p = skel / "savoirs" / "formation.md"
    p.write_text(SAVOIR.replace("theme: formation\n", ""), encoding="utf-8")
    assert any("clé `theme` manquante" in e for e in light.check(skel).errors)


def test_theme_inconnu(skel: Path):
    p = skel / "savoirs" / "formation.md"
    p.write_text(SAVOIR.replace("theme: formation", "theme: cuisine"), encoding="utf-8")
    assert any("`theme` `cuisine` inconnu" in e for e in light.check(skel).errors)


def test_theme_manquant(skel: Path):
    p = skel / "savoirs" / "formation.md"
    p.write_text(SAVOIR.replace("theme: formation\n", ""), encoding="utf-8")
    assert any("clé `theme` manquante" in e for e in light.check(skel).errors)

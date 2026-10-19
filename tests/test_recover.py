"""`recover` : grilles à icônes et grilles de texte, sur les originaux du dépôt."""

from __future__ import annotations

import shutil
from pathlib import Path

import pymupdf
import pytest
import yaml

from scripts import recover, registry as reg
from tests.conftest import REAL_ROOT

MODELE = "msds-modele-de-formation"
RELATIONS = "msds-profil-tableaux-relations"


def _pdf(source_id: str) -> Path:
    found = sorted((REAL_ROOT / "sources" / source_id / "original").glob("*.pdf"))
    if not found:
        pytest.skip(f"original de {source_id} absent")
    return found[0]


def _rows(table: str) -> list[list[str]]:
    lines = [l for l in table.strip().splitlines() if l.startswith("|")]
    return [[c.strip() for c in l.strip("|").split(" | ")] for l in lines if not l.startswith("|---")]


def _cell(table: str, row: str, col: str) -> str:
    rows = _rows(table)
    header = rows[0]
    match = [r for r in rows[1:] if row in r[:2]]
    assert match, f"ligne « {row} » absente"
    return match[0][header.index(col)]


# --------------------------------------------------------------------------- #
# Texte
# --------------------------------------------------------------------------- #

def test_join_lines_recolle_phrases_cesures_et_elements() -> None:
    assert recover.join_lines(["accomplir de", "petites tâches"]) == "accomplir de petites tâches"
    assert recover.join_lines(["responsa-", "bles préparent"]) == "responsables préparent"
    assert recover.join_lines(["MSdS 1.3", "J+S 1.9"]) == "MSdS 1.3<br>J+S 1.9"
    assert recover.join_lines(["au scoutisme", "(inter-)national"]) == "au scoutisme (inter-)national"
    assert recover.join_lines(["et moniteur·trice", "J+S et réflexion"], [False, True]) == "et moniteur·trice J+S et réflexion"


def test_is_wrap_distingue_renvoi_et_nouvel_element() -> None:
    # mots : (x0, y0, x1, y1, texte) ; cellule jusqu'à x = 100
    phrase = [(0, 0, 20, 10, "un"), (22, 0, 50, 10, "deux"), (52, 0, 80, 10, "trois"), (82, 0, 96, 10, "quatre")]
    assert recover.is_wrap(phrase, [(0, 12, 15, 22, "J+S")], 100)
    assert not recover.is_wrap(phrase, [(0, 12, 30, 22, "Posture")], 100)
    court = [(0, 0, 30, 10, "MSdS"), (32, 0, 45, 10, "1.3")]
    assert not recover.is_wrap(court, [(0, 12, 15, 22, "J+S")], 50)


def test_md_table_echappe_les_barres() -> None:
    assert "a \\| b" in recover.md_table(["x"], [["a | b"]])


# --------------------------------------------------------------------------- #
# Icônes (modèle de formation p.16 : légende + premier tableau)
# --------------------------------------------------------------------------- #

def test_legende_apprise_et_icones_classees() -> None:
    doc = pymupdf.open(_pdf(MODELE))
    legend = recover.learn_legend(doc, 16, recover.LEVELS)
    assert set(legend.prints) == set(recover.LEVELS)
    # même dessin, xrefs différents d'une page à l'autre (p.16 : 208, p.17 : 225)
    assert legend.classify(doc, 208) == legend.classify(doc, 225) == "Mémoriser/comprendre"
    assert legend.classify(doc, 212) == "Évaluer/créer"


def test_tableau_a_icones_page_16() -> None:
    doc = pymupdf.open(_pdf(MODELE))
    legend = recover.learn_legend(doc, 16, recover.LEVELS)
    table = recover.recover_icons(doc, {"method": "icons", "pages": [16]}, legend)
    rows = _rows(table)
    assert rows[0][:4] == ["Rubrique", "Contenu", "Cours de resp. de patrouille", "Cours Picos"]
    assert rows[0][-1] == "Cours Top"
    assert len(rows) == 4
    assert rows[1][0] == "Fondements et méthodologie"
    assert _cell(table, "Fondements scouts", "Cours de resp. de patrouille") == "Vivre"
    assert _cell(table, "Fondements scouts", "Cours Picos") == ""
    assert _cell(table, "Fondements scouts", "Cours de base") == "Mémoriser/comprendre"
    assert _cell(table, "Fondements scouts", "Cours de RU") == "Appliquer/analyser"
    assert _cell(table, "Fondements scouts", "Cours Panorama") == "Évaluer/créer"
    assert _cell(table, "Besoins", "Cours de resp. de groupe") == ""
    assert _cell(table, "Méthodologie de branche", "Cours Top") == ""


# --------------------------------------------------------------------------- #
# Texte sans filets (tableaux des relations p.1)
# --------------------------------------------------------------------------- #

def test_grille_de_texte_relations_page_1() -> None:
    doc = pymupdf.open(_pdf(RELATIONS))
    spec = {"method": "layout", "pages": [1], "columns": ["Castors", "Louveteaux", "Éclais", "Picos", "Route"]}
    table = recover.recover_layout(doc, spec)
    rows = _rows(table)
    assert [r[0] for r in rows[1:]] == ["Tâches et responsabilités", "Opinion", "Décisions",
                                        "Conscience de soi", "Réflexion critique"]
    assert _cell(table, "Opinion", "Éclais") == "partager ses idées et les comparer avec d’autres points de vue"
    assert _cell(table, "Tâches et responsabilités", "Castors") == "accomplir de petites tâches"
    assert recover.auto_title(recover.page_lines(doc[0])) == "Relation à sa personnalité"


# --------------------------------------------------------------------------- #
# Commande : écriture, frontmatter, rejouabilité
# --------------------------------------------------------------------------- #

def _copy_source(repo: Path, source_id: str) -> Path:
    src = REAL_ROOT / "sources" / source_id
    if not (src / "original").is_dir():
        pytest.skip(f"original de {source_id} absent (originaux hors git)")
    dst = repo / "sources" / source_id
    (dst / "original").mkdir(parents=True)
    shutil.copy(src / "source.yaml", dst / "source.yaml")
    for f in (src / "original").iterdir():
        shutil.copy(f, dst / "original" / f.name)
    return dst


def test_recover_ecrit_et_rejoue_a_l_identique(repo: Path) -> None:
    dst = _copy_source(repo, MODELE)
    (dst / "recovered").mkdir()
    (dst / "recovered" / "p99-perime.md").write_text("ancien")
    written = recover.recover(MODELE)
    assert [p.name for p in written] == ["p16-niveaux-d-approfondissement-par-contenu-et-par.md"]
    assert not (dst / "recovered" / "p99-perime.md").exists()
    text = written[0].read_text(encoding="utf-8")
    front = yaml.safe_load(text.split("---\n")[1])
    assert front == {"source": MODELE, "version": reg.load_source(MODELE)["version"], "pages": "16-18",
                     "title": "Niveaux d'approfondissement par contenu et par cours", "method": "icons"}
    assert "| Sécurité et prévention | Éthique |" in text
    recover.recover(MODELE)
    assert written[0].read_text(encoding="utf-8") == text


def test_recover_refuse_une_source_sans_recette(repo: Path) -> None:
    with pytest.raises(recover.RecoverError, match="pas de recette"):
        recover.recover("js-inconnu")

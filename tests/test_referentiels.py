"""`referentiels check` : règles de docs/skills-design.md § 6, sur un dépôt jouet."""

from __future__ import annotations

from pathlib import Path

import yaml

from scripts import ingest, referentiels as refs, registry as reg

FRONT = {
    "slug": "toy", "titre": "Jouet", "signaux": ["jouet"], "role": ["responsable"],
    "verbes": ["corriger"], "parametres": [{"nom": "date", "obligatoire": True}],
    "canevas": [], "sources": ["autre-x-test"], "inclut": [], "statut": "brouillon", "relu_le": "2026-10-18",
}

NON_NEG = "## Non-négociables\n\nN1. [tous] Exigence — `autre-x-test#01-a p.3`\nN2. [tous] Autre — `autre-x-test#02-b`\n\n"
REST = (
    "## Selon la date\n\nrien\n\n## Critères de qualité\n\nQ1. Un critère — `autre-x-test#01-a`\n\n"
    "## Critères non officiels\n\n[non officiel] x (mainteneur)\n\n"
    "## Questions à poser avant de juger\n\n1. Quoi ?\n\n## Pièges\n\nrien\n\n## Trame de conception\n\nrien\n"
)


def _make_source(repo: Path, sid: str = "autre-x-test", nature: str | None = None) -> None:
    sdir = repo / "sources" / sid
    sdir.mkdir(parents=True)
    data = {"id": sid, "title": "X", "issuer": "autre", "type": "pdf", "status": "indexed"}
    if nature:
        data["nature"] = nature
    (sdir / "source.yaml").write_text(yaml.safe_dump(data), encoding="utf-8")
    (sdir / "index.md").write_text(
        "---\nsource: x\nversion: '1'\n---\n\n- §1 A p.1-2 → 01-a.md : a\n- §2 B p.3-4 → 02-b.md : b\n",
        encoding="utf-8")
    (sdir / "01-a.md").write_text("# A\n", encoding="utf-8")
    (sdir / "02-b.md").write_text("# B\n", encoding="utf-8")


def _write(repo: Path, slug: str = "toy", body: str | None = None, **front) -> refs.Referentiel:
    fm = {**FRONT, "slug": slug, **front}
    text = "---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False) + "---\n\nPérimètre.\n\n"
    text += body if body is not None else NON_NEG + REST
    path = repo / "referentiels" / f"{slug}.md"
    path.write_text(text, encoding="utf-8")
    return refs.load_referentiel(path)


def _check(repo: Path, ref: refs.Referentiel):
    return refs.validate(ref, {str(s["id"]): s for s in reg.all_sources()})


def _has(msgs: list[str], needle: str) -> bool:
    return any(needle in m for m in msgs)


def _catalogues(repo: Path, *slugs: str) -> None:
    row = "\n".join(f"| `{s}` | signaux | params | aucun |" for s in slugs)
    table = f"## 3. Catalogue\n\n| slug | signaux | paramètres | inclut |\n|---|---|---|---|\n{row}\n"
    for name in ("scouts", "scouts-ressources"):
        path = repo / "skills-src" / name / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(table, encoding="utf-8")


def _derive(repo: Path, slug: str = "toy", relu_le: str = "2026-10-18") -> None:
    folder = repo / "skills-src" / "scouts" / "referentiels" / slug
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "01-regles.md").write_text(
        f"---\nslug: {slug}\nderive_de: {{slug: {slug}, relu_le: {relu_le}}}\nstatut: brouillon\n---\n\n",
        encoding="utf-8",
    )


def test_valide(repo: Path):
    _make_source(repo)
    errors, warnings = _check(repo, _write(repo))
    assert errors == [] and warnings == []
    assert refs.run() == 0


def test_catalogue_et_relu_le(repo: Path):
    _make_source(repo)
    _write(repo)
    _catalogues(repo, "toy")
    _derive(repo)
    assert refs.run() == 0
    _catalogues(repo, "autre")
    assert refs.run() == 1
    _catalogues(repo, "toy")
    _derive(repo, relu_le="2020-01-01")
    assert refs.run() == 1


def test_citation_cassee(repo: Path):
    _make_source(repo)
    body = NON_NEG.replace("02-b", "09-zz") + REST
    errors, _ = _check(repo, _write(repo, body=body))
    assert _has(errors, "section introuvable")


def test_section_hors_index(repo: Path):
    _make_source(repo)
    (repo / "sources" / "autre-x-test" / "03-c.md").write_text("# C\n", encoding="utf-8")
    body = NON_NEG + REST.replace("`autre-x-test#01-a`", "`autre-x-test#03-c`")
    errors, _ = _check(repo, _write(repo, body=body))
    assert _has(errors, "ne figure pas dans l'index")


def test_n_sans_citation(repo: Path):
    _make_source(repo)
    body = NON_NEG.replace(" — `autre-x-test#02-b`", "") + REST
    errors, _ = _check(repo, _write(repo, body=body))
    assert _has(errors, "N2 sans citation")


def test_n_retire_sans_citation_ok(repo: Path):
    _make_source(repo)
    body = NON_NEG.replace("N2. [tous] Autre — `autre-x-test#02-b`", "N2. retiré le 2026-10-18") + REST
    errors, warnings = _check(repo, _write(repo, body=body))
    assert not _has(errors, "sans citation") and warnings == []


def test_sources_desynchronisees(repo: Path):
    _make_source(repo)
    _make_source(repo, "autre-y-test")
    errors, _ = _check(repo, _write(repo, sources=["autre-y-test"]))
    assert _has(errors, "absents du frontmatter : autre-x-test")
    assert _has(errors, "jamais cités dans le corps : autre-y-test")


def test_cycle_inclut(repo: Path):
    _make_source(repo)
    _write(repo, "a", inclut=["b"])
    ref_b = _write(repo, "b", inclut=["a"])
    errors, _ = _check(repo, ref_b)
    assert _has(errors, "cycle")


def test_inclut_inexistant(repo: Path):
    _make_source(repo)
    errors, _ = _check(repo, _write(repo, inclut=["fantome"]))
    assert _has(errors, "`fantome` inexistant")


def test_trou_de_numero_avertissement(repo: Path):
    _make_source(repo)
    body = NON_NEG.replace("N2.", "N3.") + REST
    errors, warnings = _check(repo, _write(repo, body=body))
    assert errors == [] and _has(warnings, "N2 manquant")


def test_doublon_q(repo: Path):
    _make_source(repo)
    body = NON_NEG + REST.replace("Q1. Un critère — `autre-x-test#01-a`\n",
                                  "Q1. Un — `autre-x-test#01-a`\nQ1. Deux — `autre-x-test#01-a`\n")
    _, warnings = _check(repo, _write(repo, body=body))
    assert _has(warnings, "Q1 en double")


def test_section_manquante(repo: Path):
    _make_source(repo)
    body = NON_NEG + REST.replace("## Pièges\n\nrien\n\n", "")
    errors, _ = _check(repo, _write(repo, body=body))
    assert _has(errors, "`## Pièges` absente")


def test_sections_desordonnees(repo: Path):
    _make_source(repo)
    body = NON_NEG + REST.replace("## Pièges", "## Zz").replace("## Trame de conception", "## Pièges") \
        .replace("## Zz", "## Trame de conception")
    errors, _ = _check(repo, _write(repo, body=body))
    assert _has(errors, "hors d'ordre")


def test_section_libre_et_annexe(repo: Path):
    _make_source(repo)
    body = NON_NEG + REST.replace("## Questions", "## Exemples officiels\n\nrien\n\n## Questions") + "\n## Annexe : renvois\n\nrien\n"
    errors, _ = _check(repo, _write(repo, body=body))
    assert errors == []
    bad = NON_NEG + REST + "\n## Libre\n\nrien\n"
    errors, _ = _check(repo, _write(repo, body=bad))
    assert _has(errors, "section libre")


def test_page_et_numero_seul(repo: Path):
    _make_source(repo)
    ref = _write(repo, body=NON_NEG.replace("#02-b", "#02 p.4-5") + REST)
    assert {(c.section, c.page) for c in ref.citations} >= {("01-a", "3"), ("02", "4-5")}
    errors, _ = _check(repo, ref)
    assert errors == []
    assert refs.resolve_section("autre-x-test", "02").name == "02-b.md"
    assert refs.resolve_section("autre-x-test", "07") is None


def test_numero_ambigu(repo: Path):
    _make_source(repo)
    (repo / "sources" / "autre-x-test" / "02-bis.md").write_text("#\n", encoding="utf-8")
    assert refs.resolve_section("autre-x-test", "02") is None
    errors, _ = _check(repo, _write(repo, body=NON_NEG.replace("#02-b", "#02") + REST))
    assert _has(errors, "ambigu")


def test_id_inconnu_et_non_source(repo: Path):
    _make_source(repo)
    body = NON_NEG + REST + "\nVoir `autre-fantome#01-a`, `programme-camp`, `reglages.md`.\n"
    ref = _write(repo, body=body, sources=["autre-x-test", "autre-fantome"])
    assert {c.source_id for c in ref.citations} == {"autre-x-test", "autre-fantome"}
    errors, _ = _check(repo, ref)
    assert _has(errors, "source inconnue `autre-fantome`") and len(errors) == 1


def test_trop_long(repo: Path):
    _make_source(repo)
    long = "mot " * 6_100
    errors, _ = _check(repo, _write(repo, body=NON_NEG + REST + long))
    assert _has(errors, "mots (maximum")
    _, warnings = _check(repo, _write(repo, body=NON_NEG + REST + "mot " * 4_100))
    assert _has(warnings, "mots (au-delà")


def test_frontmatter_invalide(repo: Path):
    _make_source(repo)
    errors, _ = _check(repo, _write(repo, statut="draft", verbes=["deviner"], bidule=1,
                                    parametres=[{"nom": "x"}]))
    assert _has(errors, "`statut: draft`") and _has(errors, "verbe `deviner`")
    assert _has(errors, "clé inconnue `bidule`") and _has(errors, "`parametres` n°1")
    errors, _ = _check(repo, refs.Referentiel(
        path=repo / "referentiels" / "autre.md", slug="autre", front={**FRONT}, body=""))
    assert _has(errors, "≠ nom de fichier")


def test_canevas_nature(repo: Path):
    _make_source(repo)
    _make_source(repo, "autre-ex-test", nature="exemple")
    _, warnings = _check(repo, _write(repo, canevas=["autre-x-test", "autre-ex-test"]))
    assert _has(warnings, "`autre-x-test` n'a pas `nature: exemple`")
    assert not _has(warnings, "autre-ex-test")


def test_tableau_large(repo: Path):
    _make_source(repo)
    table = "\n| a | b | c | d | e | f | g |\n|---|---|---|---|---|---|---|\n"
    _, warnings = _check(repo, _write(repo, body=NON_NEG + REST + table))
    assert _has(warnings, "7 colonnes")


def test_citing_et_run_en_erreur(repo: Path):
    _make_source(repo)
    _write(repo)
    assert refs.citing("autre-x-test") == ["toy"] and refs.citing("autre-y") == []
    _write(repo, "casse", sources=[])
    assert refs.run() == 1


def test_new_version_liste_les_referentiels(repo: Path, pdf_factory, capsys):
    e = ingest.Entry(id="autre-x-test", type="", path=pdf_factory("a.pdf"), title="X",
                     audience=["formateur"], themes=["formation"])
    ingest.prepare_local(e)
    ingest.run([e])
    _write(repo, sources=["autre-x-test"])
    e2 = ingest.Entry(id="autre-x-test", type="", path=pdf_factory("b.pdf", n=2), new_version=True)
    ingest.prepare_local(e2)
    ingest.run([e2])
    assert "référentiels à revérifier : toy" in capsys.readouterr().err

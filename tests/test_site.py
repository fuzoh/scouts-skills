"""`site` : génération du site statique sur un dépôt jouet."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit

import pytest
import yaml
from typer.testing import CliRunner

from scripts import site


def _source(repo: Path, sid: str, **fields) -> None:
    d = repo / "sources" / sid
    d.mkdir(parents=True)
    data = {"id": sid, "title": sid.upper(), "issuer": sid.split("-", 1)[0], "type": "pdf",
            "status": "indexed", "decision": "keep", **fields}
    (d / "source.yaml").write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")


def _page(repo: Path, name: str, front: str, body: str) -> None:
    d = repo / "site"
    d.mkdir(exist_ok=True)
    (d / f"{name}.md").write_text(f"---\n{front}\n---\n\n{body}\n", encoding="utf-8")


@pytest.fixture
def toy(repo: Path) -> Path:
    _source(repo, "msds-lien", title="Règlement jouet", ref="123fr", version="v2",
            url="https://exemple.ch/page", file_url="https://exemple.ch/doc.pdf")
    _source(repo, "js-sans-lien", title="Manuel jouet", published="2026-10-01",
            redactions=[{"section": "01-a", "pattern": "x", "replace": "[retiré]"}])
    _source(repo, "autre-tiers", title="Fiche tierce", issuer_detail="organisme tiers")
    _source(repo, "cofor-rejetee", title="Document rejeté", status="rejected", decision="rejected")
    _source(repo, "cudesch-brut", title="Pas encore indexé", status="converted")
    _page(repo, "index", "title: Accueil\norder: 1",
          "## Liens\n\nVoir [les sources](sources.md#droits), [l'aide](aide.md) et [ici](#liens).\n\n"
          "| a | b |\n|---|---|\n| 1 | 2 |")
    _page(repo, "aide", "title: Aide\norder: 2\nmenu: false", "## Liens\n\n## Liens\n\n[Accueil](index.md)")
    _page(repo, "sources", "title: Sources et auteurs\norder: 3", "## Droits\n\nDroits à leurs auteurs.")
    return repo


def _html(out: Path, name: str) -> str:
    return (out / f"{name}.html").read_text(encoding="utf-8")


def test_pages_et_gabarit(toy: Path, tmp_path: Path):
    out = tmp_path / "out"
    written = site.build_site(out)
    assert sorted(p.name for p in written) == ["aide.html", "index.html", "sources.html"]
    index = _html(out, "index")
    assert '<html lang="fr">' in index
    assert "<title>Accueil · " in index and "<h1>Accueil</h1>" in index
    assert "Version 1.2.3" in index                       # pyproject.toml du dépôt jouet
    assert "MIT" in index and "CC BY-SA 4.0" in index
    assert '<a href="index.html" aria-current="page" data-label="Accueil">Accueil</a>' in index
    assert 'href="aide.html">' not in index.split("</nav>")[0]   # menu: false
    assert "<table>" in index                             # tables activées
    assert 'href="sources.html#droits"' in index and 'href="aide.html"' in index
    assert '<h2 id="liens">' in index
    aide = _html(out, "aide")
    assert '<h2 id="liens">' in aide and '<h2 id="liens-2">' in aide
    assert "<script" not in index


def test_page_des_sources(toy: Path, tmp_path: Path):
    out = tmp_path / "out"
    site.build_site(out)
    page = _html(out, "sources")
    assert "Droits à leurs auteurs." in page
    assert "Règlement jouet" in page and "réf. 123fr" in page and "version v2" in page
    assert 'href="https://exemple.ch/page"' in page and 'href="https://exemple.ch/doc.pdf"' in page
    assert "Document rejeté" not in page and "cofor-rejetee" not in page
    assert "Pas encore indexé" not in page
    manuel = next(li for li in page.split("<li>") if "Manuel jouet" in li)
    assert "Pas de lien public." in manuel
    assert "Données personnelles ou d'accès retirées (caviardage)." in manuel
    assert "publié le 01.10.2026" in manuel
    reglement = next(li for li in page.split("<li>") if "Règlement jouet" in li)
    assert "caviardage" not in reglement
    # émetteurs officiels d'abord, puis les autres sous leur `issuer_detail`
    msds = page.index("Mouvement Scout de Suisse")
    js = page.index("Jeunesse+Sport")
    autres = page.index("Autres émetteurs")
    assert msds < js < autres < page.index("<h3 id=\"organisme-tiers\">Organisme tiers</h3>")
    assert "3 sources embarquées" in page


def test_liens_internes_resolus(toy: Path, tmp_path: Path):
    out = tmp_path / "out"
    site.build_site(out)
    assert site.check_links(out) == []
    names = {p.name for p in out.glob("*.html")}
    for f in out.glob("*.html"):
        for href in re.findall(r'href="([^"]*)"', f.read_text(encoding="utf-8")):
            parts = urlsplit(href)
            if parts.scheme or parts.netloc:
                continue
            assert (parts.path or f.name) in names, (f.name, href)


def test_lien_casse_detecte(toy: Path, tmp_path: Path):
    _page(toy, "aide", "title: Aide\norder: 2", "[perdu](absent.md) et [ancre](index.md#nulle-part)")
    out = tmp_path / "out"
    site.build_site(out)
    errors = site.check_links(out)
    assert any("absent.html" in e for e in errors)
    assert any("nulle-part" in e for e in errors)
    result = CliRunner().invoke(site.app, ["--out", str(tmp_path / "cli")])
    assert result.exit_code == 1


def test_sortie_deterministe(toy: Path, tmp_path: Path):
    a, b = tmp_path / "a", tmp_path / "b"
    site.build_site(a)
    site.build_site(b)
    for f in sorted(a.glob("*.html")):
        assert f.read_bytes() == (b / f.name).read_bytes(), f.name


def test_cli(toy: Path, tmp_path: Path):
    out = tmp_path / "cli"
    result = CliRunner().invoke(site.app, ["--out", str(out)])
    assert result.exit_code == 0, result.output
    assert (out / "index.html").is_file() and (out / "sources.html").is_file()


def test_frontmatter_invalide(toy: Path, tmp_path: Path):
    _page(toy, "aide", "title: Aide", "sans order")
    with pytest.raises(site.SiteError, match="order"):
        site.build_site(tmp_path / "out")


def test_page_des_versions(toy: Path, tmp_path: Path):
    _page(toy, "nouveautes", "title: Nouveautés\norder: 4", "En-tête des versions.")
    out = tmp_path / "out"
    site.build_site(out)
    assert "Aucune version publiée pour l'instant." in _html(out, "nouveautes")
    (toy / "CHANGELOG.md").write_text(
        "# Changelog\n\n## [0.3.0](https://exemple.ch/compare) (2026-11-01)\n\n"
        "### Nouveautés\n\n* **skills:** nouvelle règle\n", encoding="utf-8")
    site.build_site(out)
    page = _html(out, "nouveautes")
    assert "En-tête des versions." in page
    assert "Changelog" not in page
    assert '<a href="https://exemple.ch/compare">0.3.0</a>' in page
    assert "<strong>skills:</strong> nouvelle règle" in page


def test_version_et_date_dans_l_en_tete(toy: Path, tmp_path: Path):
    out = tmp_path / "out"
    site.build_site(out)
    assert '<span class="version" title="Version 1.2.3">v1.2.3</span>' in _html(out, "index")
    (toy / "CHANGELOG.md").write_text(
        "# Changelog\n\n## [1.2.3](https://exemple.ch/compare) (2026-11-02)\n\n"
        "## 1.2.2 (2026-10-01)\n", encoding="utf-8")
    site.build_site(out)
    index = _html(out, "index")
    assert "v1.2.3 · 02.11.2026" in index and "publiée le 02.11.2026" in index
    assert site.release_date(toy / "CHANGELOG.md", "1.2.2") == "01.10.2026"
    assert site.release_date(toy / "CHANGELOG.md", "9.9.9") == ""


def _parcours_pages(repo: Path) -> None:
    _page(repo, "web-a", "title: Installer web\norder: 10\nparcours: web", "Web A")
    _page(repo, "web-b", "title: Utiliser web\norder: 11\nparcours: web", "Web B")
    _page(repo, "web-cachee", "title: Cachée web\norder: 12\nparcours: web\nmenu: false", "Web cachée")
    _page(repo, "agent-a", "title: Installer agent\norder: 20\nparcours: agent", "Agent A")
    _page(repo, "agent-b", "title: Utiliser agent\norder: 21\nparcours: agent", "Agent B")


def _nav(page: str, label: str) -> str:
    m = re.search(rf'<nav aria-label="{label}[^"]*"[^>]*>.*?</nav>', page, re.DOTALL)
    assert m, label
    return m.group(0)


def test_parcours_inconnu(toy: Path, tmp_path: Path):
    _page(toy, "aide", "title: Aide\norder: 2\nparcours: mobile", "x")
    with pytest.raises(site.SiteError, match="parcours.*mobile"):
        site.build_site(tmp_path / "out")


def test_menu_de_premier_niveau(toy: Path, tmp_path: Path):
    _parcours_pages(toy)
    out = tmp_path / "out"
    site.build_site(out)
    main = _nav(_html(out, "index"), "Menu principal")
    labels = re.findall(r'data-label="([^"]*)"', main)
    assert labels == ["Accueil", "Dans le navigateur", "Avec un agent", "Sources et auteurs"]
    assert 'href="web-a.html"' in main and 'href="agent-a.html"' in main
    assert "web-b.html" not in main and "web-cachee" not in main and "aide.html" not in main


def test_sous_menu_du_parcours(toy: Path, tmp_path: Path):
    _parcours_pages(toy)
    out = tmp_path / "out"
    site.build_site(out)
    page = _html(out, "web-b")
    main = _nav(page, "Menu principal")
    assert 'href="web-a.html" aria-current="true"' in main      # parcours courant, pas la page d'arrivée
    assert 'href="agent-a.html" aria-current' not in main
    sub = _nav(page, "Dans le navigateur")
    assert re.findall(r'data-label="([^"]*)"', sub) == ["Installer web", "Utiliser web"]
    assert 'href="web-b.html" aria-current="page"' in sub
    assert "agent-a" not in sub and "web-cachee" not in sub
    # première page du parcours : la page est courante dans les deux menus
    first = _html(out, "web-a")
    assert 'href="web-a.html" aria-current="page"' in _nav(first, "Menu principal")
    # page hors menu d'un parcours : sous-menu présent, aucune entrée courante
    cachee = _html(out, "web-cachee")
    assert "aria-current" not in _nav(cachee, "Dans le navigateur")
    assert 'href="web-a.html" aria-current="true"' in _nav(cachee, "Menu principal")
    assert re.findall(r'data-label="([^"]*)"', _nav(_html(out, "agent-b"), "Avec un agent")) == [
        "Installer agent", "Utiliser agent"]


def test_pas_de_sous_menu_hors_parcours(toy: Path, tmp_path: Path):
    _parcours_pages(toy)
    out = tmp_path / "out"
    site.build_site(out)
    for name in ("index", "sources", "aide"):
        assert page_navs(_html(out, name)) == 1, name
    assert 'href="sources.html" aria-current="page"' in _html(out, "sources")


def page_navs(page: str) -> int:
    return page.count("<nav ")


def test_parcours_sans_page_absent_du_menu(toy: Path, tmp_path: Path):
    out = tmp_path / "out"
    site.build_site(out)
    assert "Dans le navigateur" not in _html(out, "index")


def test_parcours_pointe_vers_sa_premiere_page_de_menu(toy: Path, tmp_path: Path):
    _page(toy, "web-hors-menu", "title: Hors menu\norder: 10\nmenu: false\nparcours: web", "x")
    _page(toy, "web-installer", "title: Installer\norder: 11\nmenu: Installer\nparcours: web", "x")
    out = tmp_path / "out"
    site.build_site(out)
    main = _nav(_html(out, "index"), "Menu principal")
    assert 'href="web-installer.html"' in main and "web-hors-menu" not in main

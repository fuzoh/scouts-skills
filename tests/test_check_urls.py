"""Tests de `scripts.check_urls` : HTTP simulé par `httpx.MockTransport`, aucun réseau."""

from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

import httpx
import pytest
import yaml
from typer.testing import CliRunner

from scripts import check_urls as cu

PDF = b"%PDF-1.4 contenu de test\n"
PDF_SHA = hashlib.sha256(PDF).hexdigest()
RUNNER = CliRunner()


def make_checker(routes, max_mb: float = 50):
    """Checker sur un transport simulé ; `routes(request)` retourne une `httpx.Response`."""
    calls: list[tuple[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append((request.method, str(request.url)))
        if request.url.path == "/robots.txt":
            return httpx.Response(404)
        return routes(request)

    client = httpx.Client(transport=httpx.MockTransport(handler), follow_redirects=True)
    return cu.Checker(client, delay=0, max_mb=max_mb), calls


def file_target(url="https://ex.org/doc.pdf", sha=PDF_SHA, retrieved=date(2026, 10, 17)):
    return cu.Target("cofor-doc", "Doc", url, "file", sha, retrieved)


def page_target(url="https://ex.org/page", kind="page"):
    return cu.Target("cofor-doc", "Doc", url, kind)


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    monkeypatch.setattr(cu.time, "sleep", lambda s: None)


def test_fichier_inchange_ok():
    checker, _ = make_checker(lambda r: httpx.Response(200, content=PDF))
    res = checker.check(file_target())
    assert res.category == "ok"
    assert res.sha256_distant == PDF_SHA


def test_fichier_change_par_sha256():
    checker, _ = make_checker(lambda r: httpx.Response(200, content=PDF + b"v2"))
    res = checker.check(file_target())
    assert res.category == "change"
    assert "sha256" in res.detail


def test_fichier_trop_gros_compare_last_modified():
    def routes(request):
        return httpx.Response(
            200,
            content=PDF,
            headers={"Last-Modified": "Wed, 18 Oct 2026 08:00:00 GMT", "Content-Length": str(len(PDF))},
        )

    checker, _ = make_checker(routes, max_mb=0.000001)  # ~1 octet : tout est trop gros
    res = checker.check(file_target())
    assert res.category == "change"
    assert "non téléchargé" in res.detail

    old = make_checker(
        lambda r: httpx.Response(200, content=PDF, headers={"Last-Modified": "Mon, 01 Jan 2024 00:00:00 GMT"}),
        max_mb=0.000001,
    )[0].check(file_target())
    assert old.category == "ok"
    assert old.sha256_distant == ""


def test_redirection():
    def routes(request):
        if request.url.path == "/page":
            return httpx.Response(301, headers={"Location": "https://ex.org/nouvelle"})
        return httpx.Response(200)

    checker, _ = make_checker(routes)
    res = checker.check(page_target())
    assert res.category == "redirige"
    assert res.final_url == "https://ex.org/nouvelle"
    assert "https://ex.org/nouvelle" in res.detail


def test_redirection_vers_url_de_la_source_attendue():
    """Page de détail qui redirige vers le `file_url` de la même source : pas signalé."""
    def routes(request):
        if request.url.path == "/detail/1":
            return httpx.Response(302, headers={"Location": "https://ex.org/doc.pdf"})
        return httpx.Response(200, content=PDF)

    checker, _ = make_checker(routes)
    src = {"id": "cofor-doc", "title": "Doc", "url": "https://ex.org/detail/1",
           "file_url": "https://ex.org/doc.pdf", "sha256": PDF_SHA}
    cats = [checker.check(t).category for t in cu.targets_of(src)]
    assert cats == ["ok", "ok"]


def test_redirection_triviale_ignoree():
    """Un slash final ou un fragment ne font pas une redirection."""
    checker, _ = make_checker(lambda r: httpx.Response(200))
    assert checker.check(page_target("https://ex.org/page/#haut")).category == "ok"


def test_404_mort():
    checker, _ = make_checker(lambda r: httpx.Response(404))
    res = checker.check(page_target())
    assert res.category == "mort"
    assert res.detail == "HTTP 404"


def test_head_refuse_puis_get():
    def routes(request):
        return httpx.Response(405 if request.method == "HEAD" else 200)

    checker, calls = make_checker(routes)
    assert checker.check(page_target()).category == "ok"
    assert [m for m, u in calls if u.endswith("/page")] == ["HEAD", "GET"]


def test_erreur_reseau_deux_essais():
    attempts = []

    def routes(request):
        attempts.append(request.method)
        raise httpx.ConnectError("refusé", request=request)

    checker, _ = make_checker(routes)
    res = checker.check(page_target())
    assert res.category == "mort"
    assert "2 essais" in res.detail
    assert len(attempts) == 2 * cu.ATTEMPTS  # HEAD puis GET, deux fois


def test_5xx_puis_succes_au_second_essai():
    state = {"n": 0}

    def routes(request):
        state["n"] += 1
        return httpx.Response(503 if state["n"] <= 2 else 200)  # HEAD+GET du 1er essai échouent

    checker, _ = make_checker(routes)
    assert checker.check(page_target()).category == "ok"


def test_robots_interdit():
    def handler(request):
        if request.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nDisallow: /prive/\n")
        return httpx.Response(200)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    res = cu.Checker(client, delay=0).check(page_target("https://ex.org/prive/x"))
    assert res.category == "ignore"


def test_user_agent_identifiable():
    assert cu.USER_AGENT.startswith("scouts-skills-veille (+https://github.com/fuzoh/scouts-skills)")
    client = cu.make_client()
    assert client.headers["user-agent"] == cu.USER_AGENT
    client.close()


def test_url_non_http_morte():
    checker, calls = make_checker(lambda r: httpx.Response(200))
    assert checker.check(page_target("ftp://ex.org/x")).category == "mort"
    assert calls == []


def test_fragments_requetes_une_fois():
    """Pages d'une SPA à routes en fragment : une seule requête par URL sans fragment."""
    checker, calls = make_checker(lambda r: httpx.Response(200))
    for n in (1, 2, 3):
        checker.check(page_target(f"https://ex.org/#!/article/{n}", "web_page"))
    assert len([c for c in calls if c[1] != "https://ex.org/robots.txt"]) == 1


def test_targets_of_source_web():
    src = {
        "id": "msds-manuel",
        "title": "Manuel",
        "type": "web",
        "url": "https://ex.org/manuel",
        "file_url": "",
        "web_pages": [
            {"url": "https://ex.org/manuel", "title": "Accueil", "slug": "accueil"},
            {"url": "https://ex.org/manuel/a", "title": "A", "slug": "a"},
        ],
        "retrieved": date(2026, 10, 17),
    }
    targets = cu.targets_of(src)
    assert [(t.kind, t.url) for t in targets] == [
        ("page", "https://ex.org/manuel"),
        ("web_page", "https://ex.org/manuel/a"),
    ]
    assert all(t.sha256 == "" for t in targets)


def test_source_web_pas_comparee_au_sha256():
    """Le html d'une page web, même différent, n'est pas un changement."""
    checker, _ = make_checker(lambda r: httpx.Response(200, content=b"<html>autre</html>"))
    t = page_target("https://ex.org/manuel/a", "web_page")
    t.sha256 = PDF_SHA
    assert checker.check(t).category == "ok"


def test_rapport_md_et_json():
    results = [
        cu.Result("a-un", "Un | titre", "https://ex.org/1", "file", "change", "sha256 distant"),
        cu.Result("a-deux", "Deux", "https://ex.org/2", "page", "mort", "HTTP 404"),
        cu.Result("a-trois", "Trois", "https://ex.org/3", "page", "redirige", "redirigé vers x"),
        cu.Result("a-quatre", "Quatre", "https://ex.org/4", "page", "ok"),
    ]
    md = cu.render_md(results, without_url=7, day=date(2026, 11, 1))
    assert md.startswith("# Veille des sources")
    assert "2026-11-01" in md
    assert "Sources sans aucune URL (non vérifiables) : 7." in md
    assert "## Changés (1)" in md and "## Morts (1)" in md and "## Redirigés (1)" in md
    assert "Un \\| titre" in md  # pipe échappé
    assert "a-quatre" not in md  # `ok` : compteur seulement

    data = json.loads(cu.render_json(results, 7, date(2026, 11, 1)))
    assert data["compteurs"] == {"change": 1, "mort": 1, "redirige": 1, "ignore": 0, "ok": 1}
    assert data["sans_url"] == 7 and len(data["resultats"]) == 4


def test_rapport_md_tronque():
    results = [
        cu.Result(f"a-{i}", "Titre " * 10, f"https://ex.org/{i}", "page", "mort", "HTTP 404") for i in range(500)
    ]
    md = cu.render_md(results, 0, date(2026, 11, 1), max_chars=10_000)
    assert len(md) < 10_000
    assert "Rapport tronqué" in md
    assert "## Morts (500)" in md


# --- CLI sur un dépôt jouet ---------------------------------------------------


def write_source(repo: Path, sid: str, **fields) -> None:
    data = {
        "id": sid,
        "title": f"Titre {sid}",
        "type": "pdf",
        "url": "",
        "file_url": "",
        "web_pages": [],
        "status": "collected",
        "retrieved": date(2026, 10, 17),
        "sha256": "",
    }
    data.update(fields)
    d = repo / "sources" / sid
    d.mkdir()
    (d / "source.yaml").write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")


def tree_state(root: Path) -> dict[str, str]:
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


@pytest.fixture
def toy(repo, monkeypatch):
    write_source(repo, "cofor-stable", file_url="https://ex.org/stable.pdf", url="https://ex.org/stable", sha256=PDF_SHA)
    write_source(repo, "cofor-change", file_url="https://ex.org/change.pdf", sha256="0" * 64)
    write_source(repo, "cofor-mort", url="https://ex.org/mort")
    write_source(repo, "msds-web", type="web", url="https://ex.org/web", web_pages=[
        {"url": "https://ex.org/web", "title": "Accueil", "slug": "accueil"},
        {"url": "https://ex.org/web/p2", "title": "P2", "slug": "p2"},
    ])
    write_source(repo, "cofor-sans-url")
    write_source(repo, "cofor-rejete", url="https://ex.org/rejete", status="rejected")

    seen: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path == "/robots.txt":
            return httpx.Response(404)
        seen.append(str(request.url))
        if path == "/mort":
            return httpx.Response(404)
        if path == "/web/p2":
            return httpx.Response(301, headers={"Location": "https://ex.org/web/p2-nouveau"})
        if path.endswith(".pdf"):
            return httpx.Response(200, content=PDF)
        return httpx.Response(200)

    def client():
        return httpx.Client(transport=httpx.MockTransport(handler), follow_redirects=True)

    monkeypatch.setattr(cu, "make_client", client)
    monkeypatch.setattr(cu.time, "sleep", lambda s: None)
    return repo, seen


def test_cli_rapport_et_registre_intact(toy):
    repo, seen = toy
    before = tree_state(repo)
    out = repo / "veille.md"  # hors du registre ; ajouté après l'état initial
    result = RUNNER.invoke(cu.app, ["--delay", "0", "--out", str(out)])
    assert result.exit_code == 0, result.output  # 0 malgré changements et morts
    md = out.read_text(encoding="utf-8")
    assert "Sources sans aucune URL (non vérifiables) : 1." in md
    assert "`cofor-change`" in md and "`cofor-mort`" in md
    assert "msds-web" in md and "p2-nouveau" in md
    assert "rejete" not in md and not any("rejete" in u for u in seen)
    assert "cofor-stable" not in md  # `ok`
    out.unlink()
    assert tree_state(repo) == before  # aucun fichier du dépôt n'a bougé


def test_cli_json_only_limit(toy):
    repo, seen = toy
    result = RUNNER.invoke(cu.app, ["--delay", "0", "--format", "json", "--only", "cofor-stable"])
    assert result.exit_code == 0, result.output
    data = json.loads(result.output)
    assert data["verifiees"] == 2 and data["compteurs"]["ok"] == 2
    assert data["sans_url"] == 0

    seen.clear()
    result = RUNNER.invoke(cu.app, ["--delay", "0", "--format", "json", "--limit", "1"])
    assert json.loads(result.output)["verifiees"] == 1


def test_cli_erreurs_d_usage(toy):
    assert RUNNER.invoke(cu.app, ["--only", "inconnu"]).exit_code == 2
    assert RUNNER.invoke(cu.app, ["--format", "xml"]).exit_code == 2

"""Tests de `scripts.discover` contre un serveur HTTP local."""

import functools
import hashlib
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import pytest
import yaml

from scripts.discover import crawl, normalize_url, write_manifest

PDF_BYTES = b"%PDF-1.4 quelques octets de test\n"


class _Handler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.path.startswith("/detail/"):
            self.send_response(302)
            self.send_header("Location", "/doc.pdf")
            self.end_headers()
            return
        super().do_GET()


@pytest.fixture
def site(tmp_path, monkeypatch):
    monkeypatch.setenv("NO_PROXY", "127.0.0.1,localhost")
    monkeypatch.setenv("no_proxy", "127.0.0.1,localhost")
    (tmp_path / "private").mkdir()
    (tmp_path / "index.html").write_text(
        "<html><head><title>Accueil</title></head><body>"
        '<a href="a.html#haut">A</a> <a href="a.html">A bis</a> <a href="/a.html/">A ter</a>'
        '<a href="doc.pdf">PDF</a>'
        '<a href="https://example.org/">externe</a>'
        '<a href="/private/x.html">privé</a>'
        '<a href="mailto:x@example.org">mail</a>'
        "</body></html>",
        encoding="utf-8",
    )
    (tmp_path / "a.html").write_text(
        "<html><body><h1>Page   A</h1><a href='index.html'>retour</a>"
        "<a href='/detail/42/doc'>fiche</a></body></html>",
        encoding="utf-8",
    )
    (tmp_path / "private" / "x.html").write_text("<title>Privé</title>", encoding="utf-8")
    (tmp_path / "doc.pdf").write_bytes(PDF_BYTES)
    (tmp_path / "robots.txt").write_text("User-agent: *\nDisallow: /private/\n", encoding="utf-8")

    handler = functools.partial(_Handler, directory=str(tmp_path))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def test_crawl(site):
    root = f"{site}/index.html"
    data = crawl(root, depth=1, render=False, delay=0, max_pages=500)

    urls = [p["url"] for p in data["pages"]]
    assert urls == [root, f"{site}/a.html"]
    assert data["pages"][0]["title"] == "Accueil"
    assert data["pages"][1]["title"] == "Page A"
    assert all(p["source"] == "" for p in data["pages"])
    assert not any("/private/" in u for u in urls)

    assert len(data["files"]) == 1
    f = data["files"][0]
    assert f["url"] == f"{site}/doc.pdf"
    assert f["name"] == "doc.pdf"
    assert f["size"] == len(PDF_BYTES)
    assert f["sha256"] == hashlib.sha256(PDF_BYTES).hexdigest()
    assert f["found_on"] == root
    assert f["id"] == ""

    everything = urls + [x["url"] for x in data["files"]]
    assert all(u.startswith(site) for u in everything)


def test_redirect_to_file(site):
    """Une page de détail qui redirige (302) vers un fichier : url = fichier final, found_on = la page de détail.

    Le même fichier atteint ensuite par son lien direct (index.html) n'est pas dupliqué.
    """
    data = crawl(f"{site}/a.html", depth=1, delay=0)
    assert [f["url"] for f in data["files"]] == [f"{site}/doc.pdf"]
    assert data["files"][0]["found_on"] == f"{site}/detail/42/doc"
    assert data["files"][0]["name"] == "doc.pdf"


def test_depth_zero(site):
    data = crawl(f"{site}/index.html", depth=0, delay=0)
    assert [p["url"] for p in data["pages"]] == [f"{site}/index.html"]
    assert len(data["files"]) == 1  # fichier lié depuis la page de départ


def test_max_pages(site):
    data = crawl(f"{site}/index.html", depth=1, delay=0, max_pages=1)
    assert len(data["pages"]) == 1


def test_write_manifest(site, tmp_path):
    data = crawl(f"{site}/index.html", depth=1, delay=0)
    out = tmp_path / "manifeste.yaml"
    write_manifest(data, out)
    loaded = yaml.safe_load(out.read_text(encoding="utf-8"))
    assert list(loaded) == ["root", "retrieved", "pages", "files"]
    assert loaded == data


def test_normalize_url():
    assert normalize_url("HTTP://Exemple.org/a/#x") == "http://exemple.org/a"
    assert normalize_url("https://exemple.org") == "https://exemple.org/"
    assert normalize_url("https://exemple.org/a?q=1#f") == "https://exemple.org/a?q=1"

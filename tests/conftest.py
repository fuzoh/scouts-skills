"""Fixtures : un dépôt jouet pour isoler les tests de `sources/`."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from scripts import registry as reg

REAL_ROOT = reg.ROOT


@pytest.fixture
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Copie template et taxonomie dans tmp et redirige registry dessus."""
    sources = tmp_path / "sources"
    docs = tmp_path / "docs"
    sources.mkdir()
    (tmp_path / "referentiels").mkdir()
    docs.mkdir()
    shutil.copy(REAL_ROOT / "sources" / "_template.yaml", sources / "_template.yaml")
    shutil.copy(REAL_ROOT / "docs" / "taxonomie.md", docs / "taxonomie.md")
    monkeypatch.setattr(reg, "ROOT", tmp_path)
    monkeypatch.setattr(reg, "SOURCES", sources)
    monkeypatch.setattr(reg, "REFERENTIELS", tmp_path / "referentiels")
    monkeypatch.setattr(reg, "DOCS", docs)
    monkeypatch.setattr(reg, "SKILLS", tmp_path / "skills-src")
    monkeypatch.setattr(reg, "PACKS", tmp_path / "skills")
    monkeypatch.setattr(reg, "DIST", tmp_path / "dist")
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "x"\nversion = "1.2.3"\n')
    monkeypatch.setattr(reg, "PYPROJECT", tmp_path / "pyproject.toml")
    monkeypatch.setattr(reg, "GLOSSARY", tmp_path / "GLOSSARY.md")
    monkeypatch.setattr(reg, "CONCEPTS", docs / "concepts")
    monkeypatch.setattr(reg, "TEMPLATE", sources / "_template.yaml")
    monkeypatch.setattr(reg, "TAXONOMY", docs / "taxonomie.md")
    monkeypatch.setattr(reg, "INVENTORY", tmp_path / "INVENTORY.md")
    return tmp_path


@pytest.fixture
def pdf_factory(tmp_path: Path):
    """Crée un petit PDF avec `n` pages et des titres."""
    import pymupdf

    def make(name: str = "doc.pdf", n: int = 4, titles: list[str] | None = None, text: str = "corps") -> Path:
        doc = pymupdf.open()
        for i in range(n):
            page = doc.new_page()
            if titles and i < len(titles) and titles[i]:
                page.insert_text((72, 72), titles[i], fontsize=20)
            page.insert_text((72, 120), f"{text} page {i + 1}", fontsize=11)
            page.insert_text((290, 800), str(i + 1), fontsize=9)
        path = tmp_path / name
        doc.save(path)
        doc.close()
        return path

    return make

"""Tests de `skills-src/scouts-ressources/scripts/ajouter.py` (chargé par son chemin)."""

from __future__ import annotations

import hashlib
import importlib.util
import re
import zipfile
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "skills-src" / "scouts-ressources" / "scripts" / "ajouter.py"
spec = importlib.util.spec_from_file_location("ajouter", SCRIPT)
aj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aj)

GABARIT = """# scouts-perso

## Profil
- **rôle** :

## Règles locales
Une ligne : règle — origine.

## Fiches
| dossier | sert à |
|---|---|
"""


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def joined(parts) -> str:
    return "".join(b for _, b in parts)


@pytest.fixture
def perso(tmp_path: Path) -> Path:
    p = tmp_path / "perso" / "scouts-perso"
    p.mkdir(parents=True)
    (p / "README.md").write_text(GABARIT, encoding="utf-8")
    return p


@pytest.fixture
def work(tmp_path: Path) -> Path:
    d = tmp_path / "work"
    d.mkdir()
    return d


def run(*args) -> int:
    return aj.main([str(a) for a in args])


# --- slug -------------------------------------------------------------------

def test_slug_accents_et_ponctuation():
    assert aj.slugify("Directive cantonale : été 2027 !") == "directive-cantonale-ete-2027"


def test_slug_longueur_et_caracteres_surs():
    s = aj.slugify("a/b\\c:d*e?" + "x" * 100)
    assert len(s) <= 60 and re.fullmatch(r"[a-z0-9-]+", s)


def test_slug_vide_et_reserve_windows():
    assert aj.slugify("???") == "document"
    assert aj.slugify("CON") != "con"


# --- découpage --------------------------------------------------------------

def test_decoupe_niveau_le_plus_haut_avec_deux_parties():
    parts = aj.split_parts("# Titre\n\n## A\n\nun\n\n## B\n\ndeux\n", "Titre")
    assert [t for t, _ in parts] == ["A", "B"]


def test_decoupe_niveau_1_si_deux_titres():
    parts = aj.split_parts("# A\n\nun\n\n## sous\n\nx\n\n# B\n\ndeux\n", "Doc")
    assert [t for t, _ in parts] == ["A", "B"]
    assert "## sous" in parts[0][1]


def test_introduction_si_texte_avant_premier_titre():
    parts = aj.split_parts("Avant.\n\n# A\n\nun\n\n# B\n\ndeux\n", "Doc")
    assert [t for t, _ in parts] == ["Introduction", "A", "B"]


def test_pas_d_introduction_si_vide():
    parts = aj.split_parts("\n\n# A\n\nun\n\n# B\n\ndeux\n", "Doc")
    assert [t for t, _ in parts] == ["A", "B"]


def test_sans_titre_une_partie_au_titre_du_document():
    assert aj.split_parts("juste du texte\n\nencore\n", "Mon doc") == [("Mon doc", "juste du texte\n\nencore\n")]


def test_titre_dans_bloc_de_code_ignore():
    text = "# A\n\n```\n# pas un titre\n```\n\n# B\n\nx\n"
    assert [t for t, _ in aj.split_parts(text, "Doc")] == ["A", "B"]


def test_aucune_perte_simple():
    text = "Avant.\n\n# A\n\nun\n\n## s\n\nx\n\n# B\n\ndeux\n"
    assert joined(aj.split_parts(text, "Doc")) == text


def gros(n: int) -> str:
    return "\n\n".join(f"mot {i} " + "x" * 90 for i in range(n)) + "\n"


def test_recoupe_au_niveau_suivant():
    text = "# A\n\n" + "".join(f"## S{i}\n\n{gros(60)}\n" for i in range(3)) + "# B\n\nfin\n"
    parts = aj.split_parts(text, "Doc")
    assert all(len(b) <= 17000 for _, b in parts)
    assert any("S1" in t for t, _ in parts)
    assert norm(joined(parts)) == norm(text)


def test_recoupe_aux_paragraphes_sans_couper_un_paragraphe():
    text = "# A\n\n" + gros(400) + "\n# B\n\nfin\n"
    parts = aj.split_parts(text, "Doc")
    assert len(parts) > 3 and all(len(b) <= 17000 for _, b in parts)
    for _, b in parts:
        for para in re.split(r"\n\s*\n", b.strip()):
            assert re.fullmatch(r"(# .*|fin|mot \d+ x{90})", para.strip())
    assert norm(joined(parts)) == norm(text)


def test_document_sans_titre_trop_long_recoupe():
    text = gros(400)
    parts = aj.split_parts(text, "Doc")
    assert len(parts) > 1 and all(len(b) <= 17000 for _, b in parts)
    assert norm(joined(parts)) == norm(text)


def test_paragraphe_seul_trop_long_coupe_quand_meme():
    text = "# A\n\n" + ("mot " * 6000) + "\n\n# B\n\nx\n"
    parts = aj.split_parts(text, "Doc")
    assert all(len(b) <= 17000 for _, b in parts)
    assert norm(joined(parts)) == norm(text)


def test_titre_seul_avant_les_parties_est_porte_par_le_document():
    parts = aj.split_parts("# Doc\n\n## A\n\nun\n\n## B\n\ndeux\n", "Doc")
    assert norm(joined(parts)) == "## A un ## B deux"


# --- résolution de --perso --------------------------------------------------

def test_perso_defaut_cwd_puis_home(tmp_path, monkeypatch):
    cwd, home = tmp_path / "cwd", tmp_path / "home"
    for d in (cwd, home):
        (d / "scouts-perso").mkdir(parents=True)
        (d / "scouts-perso" / "README.md").write_text(GABARIT)
    monkeypatch.setattr(Path, "cwd", classmethod(lambda c: cwd))
    monkeypatch.setattr(Path, "home", classmethod(lambda c: home))
    assert aj.resolve_perso(None) == cwd / "scouts-perso"
    (cwd / "scouts-perso" / "README.md").unlink()
    assert aj.resolve_perso(None) == home / "scouts-perso"
    (home / "scouts-perso" / "README.md").unlink()
    with pytest.raises(aj.Refus, match="dossier perso introuvable"):
        aj.resolve_perso(None)


def test_perso_explicite_sans_readme(tmp_path):
    (tmp_path / "vide").mkdir()
    with pytest.raises(aj.Refus, match="dossier perso introuvable"):
        aj.resolve_perso(tmp_path / "vide")


# --- bout en bout .md / .txt ------------------------------------------------

def doc_md(work: Path, name="directive.md") -> Path:
    f = work / name
    f.write_text(
        "# Directive cantonale\n\nIntro.\n\n## Règle un\n\nTexte un.\n\n## Règle deux\n\nTexte deux.\n",
        encoding="utf-8",
    )
    return f


def test_md_bout_en_bout(perso, work, capsys):
    f = doc_md(work)
    assert run(f, "--dossier", "ac", "--perso", perso) == 0
    base = perso / "ac" / "directive-cantonale"
    assert sorted(p.name for p in base.glob("*.md")) == ["01-introduction.md", "02-regle-un.md", "03-regle-deux.md"]
    assert (perso / "originaux" / "directive.md").read_bytes() == f.read_bytes()
    out = capsys.readouterr().out
    assert "03-regle-deux.md" in out
    assert out.rstrip().endswith("Remplacer À COMPLÉTER dans scouts-perso/README.md par le « sert à »")
    readme = (perso / "README.md").read_text(encoding="utf-8")
    assert readme.rstrip().endswith("| ac/directive-cantonale/ | À COMPLÉTER |")


def test_frontmatter_et_titre(perso, work):
    f = doc_md(work)
    run(f, "--dossier", "groupe", "--perso", perso, "--titre", "Directive: été")
    fiche = perso / "groupe" / "directive-ete" / "02-regle-un.md"
    sha = hashlib.sha256(f.read_bytes()).hexdigest()
    text = fiche.read_text(encoding="utf-8")
    assert re.fullmatch(
        r'---\ndocument: "Directive: été"\npartie: Règle un\noriginal: originaux/directive.md\n'
        rf"sha256: {sha}\najoute_le: \d{{4}}-\d\d-\d\d\n---\n\n# Règle un\n\nTexte un\.\n",
        text,
    ), text


def test_titre_par_defaut_premier_h1_puis_nom_de_fichier():
    assert aj.document_title("x\n\n# Mon titre\n", "fichier") == "Mon titre"
    assert aj.document_title("rien", "fichier") == "fichier"


def test_txt_sans_titre(perso, work):
    f = work / "Note de camp.txt"
    f.write_bytes("Juste du texte.\r\nSur deux lignes.\r\n".encode())
    assert run(f, "--dossier", "cours", "--perso", perso) == 0
    fiches = list((perso / "cours" / "note-de-camp").glob("*.md"))
    assert [p.name for p in fiches] == ["01-note-de-camp.md"]
    body = fiches[0].read_text(encoding="utf-8")
    assert "\r" not in body and "# Note de camp\n\nJuste du texte." in body


def test_pas_de_titre_duplique(perso, work):
    f = work / "d.md"
    f.write_text("# A\n\nun\n\n# B\n\ndeux\n", encoding="utf-8")
    run(f, "--dossier", "ac", "--perso", perso, "--titre", "Doc")
    assert (perso / "ac" / "doc" / "01-a.md").read_text(encoding="utf-8").count("# A\n") == 1


# --- doublon et collisions ---------------------------------------------------

def test_doublon_refuse_sans_rien_ecrire(perso, work, capsys):
    f = doc_md(work)
    assert run(f, "--dossier", "ac", "--perso", perso) == 0
    g = work / "copie.md"
    g.write_bytes(f.read_bytes())
    avant = sorted(perso.rglob("*"))
    readme = (perso / "README.md").read_text(encoding="utf-8")
    capsys.readouterr()
    assert run(g, "--dossier", "groupe", "--perso", perso) == 1
    err = capsys.readouterr().err
    assert "déjà ajouté" in err and "directive-cantonale" in err
    assert sorted(perso.rglob("*")) == avant
    assert (perso / "README.md").read_text(encoding="utf-8") == readme


def test_meme_titre_autre_document_suffixe(perso, work):
    docs = [doc_md(work)]
    for i, txt in enumerate(["Autre contenu.", "Encore autre."]):
        g = work / f"autre{i}.md"
        g.write_text(f"# Directive cantonale\n\n{txt}\n", encoding="utf-8")
        docs.append(g)
    for x in docs:
        assert run(x, "--dossier", "ac", "--perso", perso) == 0
    assert {p.name for p in (perso / "ac").iterdir()} == {
        "directive-cantonale", "directive-cantonale-2", "directive-cantonale-3",
    }
    assert "| ac/directive-cantonale-2/ | À COMPLÉTER |" in (perso / "README.md").read_text(encoding="utf-8")


def test_nom_d_original_deja_pris(perso, work):
    (work / "a").mkdir()
    (work / "b").mkdir()
    (work / "a" / "doc.md").write_text("# Un\n\nx\n", encoding="utf-8")
    (work / "b" / "doc.md").write_text("# Deux\n\ny\n", encoding="utf-8")
    run(work / "a" / "doc.md", "--dossier", "ac", "--perso", perso)
    run(work / "b" / "doc.md", "--dossier", "ac", "--perso", perso)
    assert sorted(p.name for p in (perso / "originaux").iterdir()) == ["doc-2.md", "doc.md"]
    fiche = (perso / "ac" / "deux" / "01-deux.md").read_text(encoding="utf-8")
    assert "original: originaux/doc-2.md" in fiche


# --- index -------------------------------------------------------------------

def test_index_section_absente(perso, work):
    (perso / "README.md").write_text("# scouts-perso\n\n## Profil\n- x\n", encoding="utf-8")
    run(doc_md(work), "--dossier", "ac", "--perso", perso)
    r = (perso / "README.md").read_text(encoding="utf-8")
    assert "## Profil\n- x\n" in r
    assert r.rstrip().endswith(
        "## Fiches\n| dossier | sert à |\n|---|---|\n| ac/directive-cantonale/ | À COMPLÉTER |"
    )


def test_index_ne_casse_pas_ce_qui_suit(perso, work):
    (perso / "README.md").write_text(GABARIT + "| ac/vieux/ | sert |\n\n## Fin\ntexte\n", encoding="utf-8")
    run(doc_md(work), "--dossier", "ac", "--perso", perso)
    r = (perso / "README.md").read_text(encoding="utf-8")
    assert "| ac/vieux/ | sert |\n| ac/directive-cantonale/ | À COMPLÉTER |\n\n## Fin\ntexte\n" in r


def test_readme_trop_long_avertit(perso, work, capsys):
    (perso / "README.md").write_text(GABARIT + "\n" + "x" * 7000 + "\n", encoding="utf-8")
    assert run(doc_md(work), "--dossier", "ac", "--perso", perso) == 0
    assert "7 000" in capsys.readouterr().err


# --- refus et usage ----------------------------------------------------------

def test_format_refuse(perso, work, capsys):
    f = work / "x.exe"
    f.write_bytes(b"MZ")
    assert run(f, "--dossier", "ac", "--perso", perso) == 1
    assert "format" in capsys.readouterr().err
    assert not (perso / "originaux").exists()


def test_fichier_absent(perso, work):
    assert run(work / "nope.md", "--dossier", "ac", "--perso", perso) == 1


def test_usage(perso, work):
    with pytest.raises(SystemExit) as e:
        run(doc_md(work), "--dossier", "autre", "--perso", perso)
    assert e.value.code == 2


# --- formats binaires --------------------------------------------------------

def test_pdf_bout_en_bout(perso, pdf_factory):
    pdf = pdf_factory("Regles.pdf", n=2, titles=["Premier titre", "Second titre"], text="contenu")
    assert run(pdf, "--dossier", "ac", "--perso", perso) == 0
    texte = " ".join(p.read_text(encoding="utf-8") for p in perso.glob("ac/*/*.md"))
    assert "contenu page 1" in texte and "contenu page 2" in texte
    assert "original: originaux/Regles.pdf" in texte
    assert (perso / "originaux" / "Regles.pdf").exists()


def mini_docx(path: Path) -> Path:
    ns = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
    rel = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    rels = "http://schemas.openxmlformats.org/package/2006/relationships"

    def p(text, style=None):
        s = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
        return f"<w:p>{s}<w:r><w:t>{text}</w:t></w:r></w:p>"

    body = p("Premier", "Heading1") + p("texte un") + p("Second", "Heading1") + p("texte deux")
    wml = "application/vnd.openxmlformats-officedocument.wordprocessingml"
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(
            "[Content_Types].xml",
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            f'<Override PartName="/word/document.xml" ContentType="{wml}.document.main+xml"/>'
            f'<Override PartName="/word/styles.xml" ContentType="{wml}.styles+xml"/></Types>',
        )
        z.writestr("_rels/.rels", f'<Relationships xmlns="{rels}"><Relationship Id="rId1" Type="{rel}/officeDocument" Target="word/document.xml"/></Relationships>')
        z.writestr("word/_rels/document.xml.rels", f'<Relationships xmlns="{rels}"><Relationship Id="rId1" Type="{rel}/styles" Target="styles.xml"/></Relationships>')
        z.writestr("word/document.xml", f"<w:document {ns}><w:body>{body}</w:body></w:document>")
        z.writestr("word/styles.xml", f'<w:styles {ns}><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/></w:style></w:styles>')
    return path


def test_docx_bout_en_bout(perso, work):
    pytest.importorskip("markitdown")
    f = mini_docx(work / "cours.docx")
    assert run(f, "--dossier", "cours", "--perso", perso) == 0
    assert sorted(p.name for p in perso.glob("cours/*/*.md")) == ["01-premier.md", "02-second.md"]

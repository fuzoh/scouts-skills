"""`recover <id>` : récupère les grilles perdues à la conversion en tableaux markdown.

Écrit `sources/<id>/recovered/pNN-<slug>.md` (frontmatter {source, version,
pages, title, method} puis un tableau), que `split` ajoute en fin de la section
qui couvre ces pages. Rejouable et déterministe : `recovered/*.md` est vidé puis
réécrit depuis l'original. Ne touche ni `raw.md`, ni le yaml, ni le statut.

Deux méthodes, choisies par la recette de la source (`RECIPES`) :

- `icons` : tableau réglé (filets) dont des cellules portent une icône image
  par niveau. Les icônes sont identifiées par empreinte de pixels (grille de
  gris réduite, indépendante de la résolution et du xref), le libellé est appris
  sur la légende (icône la plus proche du texte du libellé). Squelette lignes ×
  colonnes par `find_tables`, contenu relu par position (mots et icônes dont le
  centre tombe dans la cellule). En-têtes : ligne du tableau qui porte du texte
  dans la colonne des icônes (« Niveau »), sinon texte pivoté au-dessus.
- `layout` : grille de texte sans filets (flèches, bandes de couleur). Colonnes
  = libellés d'en-tête donnés par la recette (même ligne de base), lignes =
  libellés à gauche du premier en-tête ; chaque ligne de texte va à la colonne
  dont l'en-tête est le plus proche et à la ligne dont le libellé est le plus
  proche, dans sa bande.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import typer
import yaml

from scripts import registry as reg

app = typer.Typer(add_completion=False, help=__doc__)

LEVELS = ["Vivre", "Mémoriser/comprendre", "Appliquer/analyser", "Évaluer/créer"]

# Une recette par source : légende (méthode icons) et tableaux à produire.
# `pages` = pages physiques ; `columns` (layout) = en-têtes tels qu'imprimés ;
# `parts` (layout) = moitiés d'une double page fusionnées par libellé de ligne ;
# `title` absent = plus grand texte de la page (capitales ramenées en minuscules).
RECIPES: dict[str, dict[str, Any]] = {
    "msds-modele-de-formation": {
        "legend": {"page": 16, "labels": LEVELS},
        "tables": [
            {"method": "icons", "pages": [16, 17, 18],
             "title": "Niveaux d'approfondissement par contenu et par cours"},
        ],
    },
    "cofor-checklist-cours-base": {
        "legend": {"page": 1, "labels": LEVELS},
        "tables": [
            {"method": "icons", "pages": [2, 3, 4],
             "title": "Contenus de formation, niveaux d'approfondissement et objectifs"},
        ],
    },
    "msds-profil-tableaux-relations": {
        "tables": [
            {"method": "layout", "pages": [p], "columns": ["Castors", "Louveteaux", "Éclais", "Picos", "Route"]}
            for p in range(1, 6)
        ],
    },
    "msds-profil-du-scoutisme": {
        "tables": [
            {"method": "layout", "pages": [11], "title": "Branches : âge et classe scolaire",
             "columns": ["Castors", "Louveteaux", "Éclais", "Picos", "Route"]},
            {"method": "layout", "pages": [12], "title": "Aperçu des branches",
             "newline_before": r"plusieurs ",
             "parts": [
                 {"clip": [0, 0, 595.3, 842], "columns": ["Branche Castors", "Branche Louveteaux", "Branche Éclais"]},
                 {"clip": [595.3, 0, 1191, 842], "columns": ["Branche Picos", "Branche Route", "SMT"]},
             ]},
        ] + [
            {"method": "layout", "pages": [p], "columns": ["Castors", "Louveteaux", "Éclais", "Picos", "Route"]}
            for p in range(15, 20)
        ],
    },
}

GRID = 12                 # empreinte d'icône : GRID × GRID cases de gris moyen
MATCH_MAX = 0.06          # distance moyenne maximale à l'icône de légende
MATCH_MARGIN = 0.75       # meilleure distance < MATCH_MARGIN × deuxième
WRAP_WORDS = 4            # renvoi à la ligne seulement dans une phrase, pas une liste de codes
CELL_PAD = 3              # pt : marge intérieure d'une cellule
SPACE = 2.5               # pt : largeur d'une espace
HEADER_ABOVE_MAX = 18
MARGIN = 0.06             # part de la hauteur de page où un nombre seul est un folio
GRID_BREAK = 2.0          # saut vertical (× écart médian des lignes) qui clôt une grille     # pt : rubrique = texte horizontal juste au-dessus d'un tableau
BR = "<br>"


class RecoverError(Exception):
    pass


# --------------------------------------------------------------------------- #
# Texte : lignes, jointure, rendu markdown
# --------------------------------------------------------------------------- #

@dataclass
class Line:
    text: str
    bbox: tuple[float, float, float, float]
    dir: tuple[float, float]
    size: float

    @property
    def horizontal(self) -> bool:
        return abs(self.dir[0]) > 0.9

    @property
    def cx(self) -> float:
        return (self.bbox[0] + self.bbox[2]) / 2

    @property
    def cy(self) -> float:
        return (self.bbox[1] + self.bbox[3]) / 2


def clean(text: str) -> str:
    text = text.replace(" ", " ").replace("\xa0", " ").replace("\t", " ")
    return re.sub(r"\s+", " ", text).strip()


def page_lines(page) -> list[Line]:
    """Lignes de texte non vides de la page, avec direction et taille."""
    out: list[Line] = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            text = clean("".join(s["text"] for s in line["spans"]))
            if text:
                size = max(s["size"] for s in line["spans"])
                out.append(Line(text, tuple(line["bbox"]), tuple(line["dir"]), size))
    return out


def join_lines(lines: list[str], wraps: list[bool] | None = None) -> str:
    """Recolle les lignes d'une cellule : césure = collée ; suite de phrase
    (minuscule, ou renvoi forcé `wraps[k]`) = espace ; nouvel élément
    (majuscule, chiffre, puce) = `<br>`."""
    out = ""
    for k, raw in enumerate(lines):
        line = clean(raw)
        if not line:
            continue
        if not out:
            out = line
        elif out.endswith("-") and line[:1].islower():
            out = out[:-1] + line
        elif line.lstrip("(«“\"'")[:1].islower() or (wraps and wraps[k]):
            out += " " + line
        else:
            out += BR + line
    return out


def join_label(lines: list[str]) -> str:
    """Libellé sur plusieurs lignes : une seule phrase, césure recollée."""
    out = ""
    for line in map(clean, lines):
        if out.endswith("-") and line[:1].islower():
            out = out[:-1] + line
        else:
            out = f"{out} {line}".strip()
    return out


def ordered(lines: list[Line]) -> list[str]:
    """Ordre de lecture : haut → bas ; texte pivoté vers le haut : gauche → droite."""
    def key(l: Line) -> tuple[float, float]:
        if l.horizontal:
            return (round(l.bbox[1]), l.bbox[0])
        return (l.bbox[0], 0.0) if l.dir[1] < 0 else (-l.bbox[2], 0.0)
    return [l.text for l in sorted(lines, key=key)]


def md_cell(text: str) -> str:
    return text.replace("|", "\\|")


def md_table(header: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(md_cell(h) for h in header) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(md_cell(c) for c in row) + " |" for row in rows]
    return "\n".join(out) + "\n"


def title_case(text: str) -> str:
    """« RELATION À SA PERSONNALITÉ » → « Relation à sa personnalité »."""
    return text[:1] + text[1:].lower() if text.isupper() else text


def auto_title(lines: list[Line]) -> str:
    """Plus grand texte horizontal de la page (lignes contiguës de même taille)."""
    horiz = [l for l in lines if l.horizontal]
    if not horiz:
        return ""
    size = max(l.size for l in horiz)
    top = sorted((l for l in horiz if abs(l.size - size) < 0.1), key=lambda l: (l.bbox[1], l.bbox[0]))
    return title_case(clean(" ".join(l.text for l in top)))


# --------------------------------------------------------------------------- #
# Icônes : empreinte, légende, classement
# --------------------------------------------------------------------------- #

def fingerprint(doc, xref: int) -> tuple[float, ...]:
    """Gris moyen (0 blanc, 1 noir) sur GRID × GRID cases, transparence sur blanc."""
    import pymupdf

    pix = pymupdf.Pixmap(doc, xref)
    smask = doc.xref_get_key(xref, "SMask")
    if smask[0] == "xref":
        pix = pymupdf.Pixmap(pix, pymupdf.Pixmap(doc, int(smask[1].split()[0])))
    alpha = None
    if pix.alpha:
        alpha = pymupdf.Pixmap(None, pix).samples  # canal alpha seul
        pix = pymupdf.Pixmap(pix, 0)
    if pix.colorspace is None or pix.colorspace.n != 1:
        pix = pymupdf.Pixmap(pymupdf.csGRAY, pix)
    w, h, s = pix.width, pix.height, pix.samples
    acc = [0.0] * (GRID * GRID)
    cnt = [0] * (GRID * GRID)
    for y in range(h):
        row = (y * GRID // h) * GRID
        for x in range(w):
            ink = 1 - s[y * w + x] / 255
            if alpha is not None:
                ink *= alpha[y * w + x] / 255
            k = row + x * GRID // w
            acc[k] += ink
            cnt[k] += 1
    return tuple(round(a / c, 4) if c else 0.0 for a, c in zip(acc, cnt))


def distance(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


@dataclass
class Legend:
    prints: dict[str, tuple[float, ...]]          # libellé → empreinte
    page: int = 0                                 # page de la légende
    xrefs: frozenset[int] = frozenset()           # images de la légende elle-même
    cache: dict[str, str | None] = field(default_factory=dict)

    def classify(self, doc, xref: int) -> str | None:
        """Libellé de l'icône, None si elle ne ressemble à aucune icône de légende."""
        fp = fingerprint(doc, xref)
        key = hashlib.sha1(repr(fp).encode()).hexdigest()
        if key not in self.cache:
            ranked = sorted((distance(fp, ref), label) for label, ref in self.prints.items())
            best_d, best = ranked[0]
            second = ranked[1][0] if len(ranked) > 1 else 1.0
            ok = best_d <= MATCH_MAX and best_d < MATCH_MARGIN * second
            self.cache[key] = best if ok else None
        return self.cache[key]


def learn_legend(doc, page_no: int, labels: list[str]) -> Legend:
    """Associe chaque libellé à l'image la plus proche de son texte sur la page de légende."""
    page = doc[page_no - 1]
    lines = [l for l in page_lines(page) if l.horizontal]
    images = [(i["xref"], i["bbox"]) for i in page.get_image_info(xrefs=True) if i["xref"]]
    prints: dict[str, tuple[float, ...]] = {}
    used: set[int] = set()
    for label in labels:
        hits = [l for l in lines if clean(l.text).lower() == label.lower()]
        if not hits:
            raise RecoverError(f"légende p.{page_no} : libellé « {label} » introuvable")
        line = hits[0]

        def score(img: tuple[int, tuple[float, ...]]) -> tuple[int, float]:
            x0, y0, x1, y1 = img[1]
            overlap = min(y1, line.bbox[3]) - max(y0, line.bbox[1]) > 0
            dx, dy = (x0 + x1) / 2 - line.cx, (y0 + y1) / 2 - line.cy
            return (0 if overlap else 1, (dx * dx + dy * dy) ** 0.5)

        if not images:
            raise RecoverError(f"légende p.{page_no} : aucune image")
        xref = min(images, key=score)[0]
        prints[label] = fingerprint(doc, xref)
        used.add(xref)
    if len({prints[l] for l in labels}) != len(labels):
        raise RecoverError(f"légende p.{page_no} : deux libellés ont la même icône")
    return Legend(prints, page_no, frozenset(used))


def page_icons(doc, page, legend: Legend) -> list[tuple[tuple[float, float], str]]:
    """(centre, libellé) des images de la page reconnues comme icônes de légende."""
    out = []
    for info in page.get_image_info(xrefs=True):
        if not info["xref"] or (page.number + 1 == legend.page and info["xref"] in legend.xrefs):
            continue
        label = legend.classify(doc, info["xref"])
        if label:
            x0, y0, x1, y1 = info["bbox"]
            out.append((((x0 + x1) / 2, (y0 + y1) / 2), label))
    return out


# --------------------------------------------------------------------------- #
# Méthode icons : tableaux réglés
# --------------------------------------------------------------------------- #

@dataclass
class Grid:
    """Un tableau relu : cellules texte, cellules à icône, en-têtes."""
    cols: list[tuple[float, float]]
    rows: list[list[str]]
    icon: list[list[bool]]
    names: list[str]
    rubric: str


def _inside(pt: tuple[float, float], rect: tuple[float, float, float, float]) -> bool:
    return rect[0] <= pt[0] < rect[2] and rect[1] <= pt[1] < rect[3]


def read_table(page, table, words, icons, lines: list[Line]) -> Grid:
    """Squelette `find_tables`, contenu relu par position."""
    tx0, ty0, tx1, ty1 = table.bbox
    full = max(table.rows, key=lambda r: sum(c is not None for c in r.cells))
    cols = [(c[0], c[2]) for c in full.cells if c is not None]
    starts = []
    for r in table.rows:
        cells = r.cells
        spans_all = cells[0] is not None and cells[0][2] - cells[0][0] > 0.9 * (tx1 - tx0)
        if spans_all or any(c is not None for c in cells[1:]):
            starts.append(r.bbox[1])
    bounds = list(zip(starts, starts[1:] + [ty1]))
    rows: list[list[str]] = []
    icon: list[list[bool]] = []
    for y0, y1 in bounds:
        row, flags = [], []
        for x0, x1 in cols:
            rect = (x0, y0, x1, y1)
            inside = [w for w in words if _inside(((w[0] + w[2]) / 2, (w[1] + w[3]) / 2), rect)]
            by_line: dict[tuple[int, int], list] = {}
            for w in inside:
                by_line.setdefault((w[5], w[6]), []).append(w)
            texts, wraps, prev = [], [], None
            for _, ws in sorted(by_line.items(), key=lambda kv: (round(kv[1][0][1]), kv[1][0][0])):
                ws = sorted(ws, key=lambda w: w[0])
                texts.append(" ".join(w[4] for w in ws))
                wraps.append(prev is not None and is_wrap(prev, ws, x1))
                prev = ws
            labels = [lab for pt, lab in icons if _inside(pt, rect)]
            text = ", ".join(labels) if labels else join_lines(texts, wraps)
            row.append(text)
            flags.append(bool(labels))
        rows.append(row)
        icon.append(flags)
    # Rubrique : texte horizontal juste au-dessus du tableau.
    above = [l for l in lines if l.horizontal and ty0 - HEADER_ABOVE_MAX <= l.bbox[3] <= ty0 + 1
             and tx0 <= l.cx <= tx1]
    rubric = join_lines(ordered(above))
    # Noms de colonnes pivotés au-dessus du tableau.
    names = []
    for x0, x1 in cols:
        rot = [l for l in lines if not l.horizontal and x0 <= l.cx < x1 and l.bbox[3] <= ty0 + 1]
        names.append(clean(" ".join(ordered(rot))))
    return Grid(cols, rows, icon, names, rubric)


def is_wrap(prev: list, line: list, right: float) -> bool:
    """Renvoi automatique : la ligne précédente est une phrase (≥ WRAP_WORDS mots)
    et le premier mot de la suivante n'y tenait pas (bord de cellule - marge).
    Un mot à majuscule initiale seule (« Posture ») ouvre un nouvel élément ;
    un sigle (« J+S », « MSdS ») peut continuer la phrase."""
    word = line[0][4]
    if word[:1].isupper() and word[1:].isalpha() and word[1:].islower():
        return False
    first = line[0][2] - line[0][0]
    room = right - CELL_PAD - prev[-1][2]
    return len(prev) >= WRAP_WORDS and first + SPACE > room


def recover_icons(doc, spec: dict[str, Any], legend: Legend) -> str:
    grids: list[Grid] = []
    for p in spec["pages"]:
        page = doc[p - 1]
        words = page.get_text("words")
        icons = page_icons(doc, page, legend)
        lines = page_lines(page)
        tables = sorted(page.find_tables().tables, key=lambda t: (t.bbox[1], t.bbox[0]))
        used = 0
        for t in tables:
            g = read_table(page, t, words, icons, lines)
            if any(any(f) for f in g.icon):
                grids.append(g)
                used += sum(sum(f) for f in g.icon)
        if used != len(icons):
            raise RecoverError(f"p.{p} : {len(icons)} icônes, {used} placées dans un tableau")
    if not grids:
        raise RecoverError("aucun tableau à icônes")

    ncol = len(grids[0].cols)
    if any(len(g.cols) != ncol for g in grids):
        raise RecoverError("nombre de colonnes différent d'un tableau à l'autre")
    icon_cols = sorted({j for g in grids for f in g.icon for j, v in enumerate(f) if v})

    def is_header(row: list[str], flags: list[bool]) -> bool:
        return any(row[j] and not flags[j] for j in icon_cols)

    # Colonne de contenu : la colonne sans icône la plus fournie en texte.
    data_rows = [r for g in grids for r, f in zip(g.rows, g.icon) if not is_header(r, f)]
    content = max((j for j in range(ncol) if j not in icon_cols),
                  key=lambda j: (sum(len(r[j]) for r in data_rows), -j))

    # En-têtes : ligne interne (texte dans une colonne d'icônes) ou texte pivoté au-dessus.
    names: list[str] = [""] * ncol
    out_rows: list[list[str]] = []
    form_style = False
    for g in grids:
        rubric = g.rubric
        sub = ""
        if any(g.names[j] for j in icon_cols) and not any(names):
            names = list(g.names)
        for row, flags in zip(g.rows, g.icon):
            if not any(row):
                continue
            if is_header(row, flags):                                  # ligne d'en-tête
                form_style = True
                if not any(names):
                    names = list(row)
                rubric, sub = row[content] or rubric, ""
                continue
            if form_style and not any(flags):
                filled = [j for j in range(ncol) if row[j]]
                if len(filled) == 1:                                   # sous-rubrique
                    sub = row[filled[0]]
                    continue
            out_rows.append([f"{rubric} – {sub}" if sub else rubric] + row)

    keep = list(range(ncol))
    if form_style:  # colonnes de formulaire vides (cases à cocher, n° à remplir)
        keep = [j for j in range(ncol) if any(r[1 + j] for r in out_rows)]
    keep = [content] + [j for j in keep if j != content]
    header = ["Rubrique", "Contenu"] + [names[j] or f"Col{j + 1}" for j in keep[1:]]
    body = [[r[0]] + [r[1 + j] for j in keep] for r in out_rows]
    return md_table(header, body)


# --------------------------------------------------------------------------- #
# Méthode layout : grilles de texte sans filets
# --------------------------------------------------------------------------- #

def _in_clip(l: Line, clip: tuple[float, ...] | None) -> bool:
    return clip is None or (clip[0] <= l.cx < clip[2] and clip[1] <= l.cy < clip[3])


def find_headers(lines: list[Line], columns: list[str]) -> list[Line]:
    """Les en-têtes de colonnes, tous sur une même ligne de base (la plus haute)."""
    horiz = [l for l in lines if l.horizontal]
    for first in sorted((l for l in horiz if l.text == columns[0]), key=lambda l: l.bbox[1]):
        found = [first]
        for name in columns[1:]:
            match = [l for l in horiz if l.text == name and abs(l.cy - first.cy) < 3]
            if not match:
                break
            found.append(min(match, key=lambda l: l.bbox[0]))
        if len(found) == len(columns):
            return found
    raise RecoverError(f"en-têtes {columns} introuvables sur une même ligne")


def is_folio(l: Line, height: float) -> bool:
    """Numéro de page : chiffres seuls dans la marge haute ou basse."""
    return l.text.isdigit() and not (MARGIN * height < l.cy < (1 - MARGIN) * height)


def read_layout(lines: list[Line], columns: list[str], clip=None, height: float = 842.0,
                newline_before: str = "") -> tuple[list[str], list[list[str]]]:
    """(libellés de ligne, cellules) d'une grille de texte."""
    lines = [l for l in lines if _in_clip(l, clip) and not is_folio(l, height)]
    headers = find_headers(lines, columns)
    centers = [h.cx for h in headers]
    top = max(h.bbox[3] for h in headers)
    left = min(h.bbox[0] for h in headers)
    spacing = max(b - a for a, b in zip(centers, centers[1:])) if len(centers) > 1 else 200.0

    # Libellés de ligne : texte horizontal sous les en-têtes, à gauche du premier,
    # lignes rapprochées regroupées ; la grille s'arrête au premier grand saut.
    cand = sorted((l for l in lines if l.horizontal and l.bbox[1] >= top - 1 and l.bbox[2] <= left
                   and any(c.isalpha() for c in l.text)),
                  key=lambda l: (l.bbox[1], l.bbox[0]))
    groups: list[list[Line]] = []
    for l in cand:
        prev = groups[-1][-1] if groups else None
        if prev and l.bbox[1] - prev.bbox[3] < 0.6 * (prev.bbox[3] - prev.bbox[1]) and abs(l.bbox[0] - prev.bbox[0]) < 5:
            groups[-1].append(l)
        else:
            groups.append([l])
    ys = [(g[0].bbox[1] + g[-1].bbox[3]) / 2 for g in groups]
    if not ys:
        raise RecoverError(f"aucun libellé de ligne à gauche de « {columns[0]} »")
    gaps = sorted(b - a for a, b in zip(ys, ys[1:]))
    if gaps:
        median = gaps[len(gaps) // 2]
        cut = next((i + 1 for i, (a, b) in enumerate(zip(ys, ys[1:])) if b - a > GRID_BREAK * median), len(ys))
        groups, ys = groups[:cut], ys[:cut]
    labels = [join_label([l.text for l in g]) for g in groups]
    bands = []
    for i, y in enumerate(ys):
        lo = top if i == 0 else (ys[i - 1] + y) / 2
        hi = (y + ys[i + 1]) / 2 if i + 1 < len(ys) else y + (y - lo)
        bands.append((lo, hi))

    taken = {id(l) for g in groups for l in g} | {id(h) for h in headers}
    cells: list[list[list[Line]]] = [[[] for _ in columns] for _ in ys]
    for l in lines:
        if id(l) in taken or l.cy <= top:
            continue
        i = next((k for k, (lo, hi) in enumerate(bands) if lo <= l.cy < hi), None)
        j = min(range(len(centers)), key=lambda k: abs(centers[k] - l.cx))
        if i is None or abs(centers[j] - l.cx) > spacing:
            continue
        cells[i][j].append(l)
    rx = re.compile(newline_before) if newline_before else None
    rows = []
    for row in cells:
        out = []
        for c in row:
            texts = ordered(c)
            text = join_lines(texts)
            if rx:  # élément imposé par la recette : passage à la ligne avant le motif
                text = BR.join(_split_items(texts, rx))
            out.append(text)
        rows.append(out)
    kept = [(lab, row) for lab, row in zip(labels, rows) if any(row)]
    return [k[0] for k in kept], [k[1] for k in kept]


def _split_items(texts: list[str], rx: re.Pattern) -> list[str]:
    """Regroupe les lignes en éléments, un nouvel élément à chaque ligne qui commence par `rx`."""
    items: list[list[str]] = []
    for s in texts:
        if not items or rx.match(clean(s)):
            items.append([s])
        else:
            items[-1].append(s)
    return [join_lines(i) for i in items]


def recover_layout(doc, spec: dict[str, Any]) -> str:
    if len(spec["pages"]) != 1:
        raise RecoverError("layout : une page par tableau")
    page = doc[spec["pages"][0] - 1]
    lines = page_lines(page)
    parts = spec.get("parts") or [{"columns": spec["columns"]}]
    header: list[str] = [spec.get("corner", "")]
    order: list[str] = []
    table: dict[str, list[str]] = {}
    width = 0
    for part in parts:
        labels, rows = read_layout(lines, part["columns"], part.get("clip"), page.rect.height,
                                   spec.get("newline_before", ""))
        for lab, row in zip(labels, rows):
            if lab not in table:
                order.append(lab)
                table[lab] = [""] * width
            table[lab] += row
        width += len(part["columns"])
        for lab in order:
            table[lab] += [""] * (width - len(table[lab]))
        header += part["columns"]
    return md_table(header, [[lab] + table[lab] for lab in order])


# --------------------------------------------------------------------------- #
# Commande
# --------------------------------------------------------------------------- #

def page_range(pages: list[int]) -> str:
    return f"{pages[0]}-{pages[-1]}" if pages[-1] != pages[0] else str(pages[0])


def render(source_id: str, version: str, spec: dict[str, Any], title: str, table: str) -> str:
    front = {"source": source_id, "version": version, "pages": page_range(spec["pages"]),
             "title": title, "method": spec["method"]}
    return "---\n" + yaml.safe_dump(front, sort_keys=False, allow_unicode=True) + "---\n\n" + table


def recover(source_id: str) -> list[Path]:
    """Écrit `recovered/*.md` pour la source ; rien n'est écrit si un tableau échoue."""
    import pymupdf

    if source_id not in RECIPES:
        raise RecoverError(f"pas de recette pour `{source_id}` (sources connues : {', '.join(sorted(RECIPES))})")
    recipe = RECIPES[source_id]
    data = reg.load_source(source_id)
    pdfs = [p for p in reg.original_files(source_id) if p.suffix.lower() == ".pdf"]
    if len(pdfs) != 1:
        raise RecoverError(f"{source_id}: un seul PDF attendu dans original/ ({len(pdfs)} trouvés)")
    doc = pymupdf.open(pdfs[0])
    legend = learn_legend(doc, recipe["legend"]["page"], recipe["legend"]["labels"]) if "legend" in recipe else None

    outputs: dict[str, str] = {}
    for spec in recipe["tables"]:
        try:
            if spec["method"] == "icons":
                if legend is None:
                    raise RecoverError("méthode icons sans légende dans la recette")
                table = recover_icons(doc, spec, legend)
            else:
                table = recover_layout(doc, spec)
        except RecoverError as exc:
            raise RecoverError(f"{source_id} p.{page_range(spec['pages'])} : {exc}") from exc
        title = spec.get("title") or auto_title(page_lines(doc[spec["pages"][0] - 1]))
        name = f"p{spec['pages'][0]:02d}-{reg.slugify(title, 50)}.md"
        if name in outputs:
            raise RecoverError(f"{source_id}: deux tableaux visent recovered/{name}")
        outputs[name] = render(source_id, str(data.get("version", "")), spec, title, table)

    rdir = reg.source_dir(source_id) / "recovered"
    rdir.mkdir(exist_ok=True)
    for old in rdir.glob("*.md"):
        old.unlink()
    written = []
    for name, text in outputs.items():
        (rdir / name).write_text(text, encoding="utf-8")
        written.append(rdir / name)
    return written


@app.command()
def main(
    id: str = typer.Argument(None, help="Identifiant de la source (absent avec --all)."),
    all_: bool = typer.Option(False, "--all", help="Toutes les sources qui ont une recette."),
) -> None:
    ids = sorted(RECIPES) if all_ else [id] if id else []
    if not ids:
        typer.echo("donner un identifiant ou --all", err=True)
        raise typer.Exit(1)
    for sid in ids:
        try:
            written = recover(sid)
        except (RecoverError, FileNotFoundError) as exc:
            typer.echo(f"refusé : {exc}", err=True)
            raise typer.Exit(1)
        for w in written:
            typer.echo(f"✓ {w.relative_to(reg.ROOT)}")


if __name__ == "__main__":
    app()

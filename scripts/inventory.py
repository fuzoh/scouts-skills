"""`inventory` : valide tous les `sources/*/source.yaml` et génère `INVENTORY.md`.

Validation : schéma du yaml (registry), sha256 de l'original recalculé quand
`original/` est présent (les originaux ne sont pas versionnés), et
artefacts exigés par le statut :
  converted → `raw.md` ou `raw/` (sauf `extraction: catalogue`) ;
  indexed   → idem + `index.md` à la version du registre + chaque section qu'il
              liste, à la même version (catalogue : `index.md` seul) ;
  verified  → idem + `fidelity` renseigné.
Les sections portent `fidelity: partial` si le yaml le dit, et aucune règle de
`redactions` ne doit encore trouver de texte dans les sections ni dans le texte brut.

Toute erreur : liste complète sur stderr, code 1, `INVENTORY.md` non écrit.
`--check` : validation seule.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from typing import Any

import typer

from scripts import redact
from scripts import referentiels as refs
from scripts import registry as reg
from scripts import split as sp

app = typer.Typer(add_completion=False, help=__doc__)

STATUS_ORDER = list(reg.STATUSES)


def _link(src: dict[str, Any]) -> str:
    return f"[`{src['id']}`](sources/{src['id']}/source.yaml)"


def _row(src: dict[str, Any]) -> str:
    return f"| {_link(src)} | {src.get('title', '')} | {src.get('issuer', '')} | {src.get('type', '')} | {src.get('pages', 0)} | `{src.get('status', '')}` |"


def _table(rows: list[dict[str, Any]]) -> list[str]:
    if not rows:
        return ["_aucune_", ""]
    out = ["| id | titre | émetteur | type | pages | statut |", "|---|---|---|---|---|---|"]
    out += [_row(s) for s in rows]
    out.append("")
    return out


def render_inventory(sources: list[dict[str, Any]], tax: reg.Taxonomy) -> str:
    """Markdown de l'inventaire."""
    lines = [
        "# Inventaire des sources",
        "",
        f"Généré par `just inventory` le {reg.today().isoformat()}. Ne pas éditer : le registre est dans `sources/*/source.yaml`.",
        "",
        f"**{len(sources)} sources.**",
        "",
        "## Par statut",
        "",
        "| statut | sources |",
        "|---|---|",
    ]
    by_status = Counter(s.get("status") for s in sources)
    for st in STATUS_ORDER:
        if by_status.get(st):
            lines.append(f"| `{st}` | {by_status[st]} |")
    lines.append("")

    active = [s for s in sources if s.get("status") != "rejected"]

    lines += ["## Toutes les sources", ""] + _table(sorted(sources, key=lambda s: s["id"]))

    lines += ["## Par public", ""]
    by_aud: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for s in active:
        for a in s.get("audience") or []:
            by_aud[a].append(s)
    for a in tax.audience:
        lines += [f"### `{a}` ({len(by_aud.get(a, []))})", ""] + _table(sorted(by_aud.get(a, []), key=lambda s: s["id"]))

    lines += ["## Par thème", ""]
    by_theme: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for s in active:
        for t in s.get("themes") or []:
            by_theme[t].append(s)
    for t in tax.themes:
        lines += [f"### `{t}` ({len(by_theme.get(t, []))})", ""] + _table(sorted(by_theme.get(t, []), key=lambda s: s["id"]))

    lines += ["## Extraction différée ou catalogue", ""]
    special = [s for s in active if s.get("extraction") in ("vision", "catalogue")]
    if special:
        lines += ["| id | extraction | notes |", "|---|---|---|"]
        lines += [f"| {_link(s)} | `{s.get('extraction')}` | {s.get('notes', '')} |" for s in special]
        lines.append("")
    else:
        lines += ["_aucune_", ""]

    lines += ["## Sources périmées (`stale`)", ""]
    stale = [s for s in active if s.get("stale")]
    if stale:
        lines += [f"- {_link(s)} : {s.get('file_url') or s.get('url', '')}" for s in stale]
        lines.append("")
    else:
        lines += ["_aucune_", ""]

    return "\n".join(lines)


ARTEFACT_STATUSES = ("converted", "indexed", "verified")


def has_original(data: dict[str, Any]) -> bool:
    """`original/` présent : copie locale du mainteneur (jamais dans git, absent en CI)."""
    return (reg.source_dir(str(data["id"])) / "original").is_dir()


def check_hash(data: dict[str, Any]) -> list[str]:
    """sha256 de l'original recalculé et comparé au registre, si l'original est là."""
    if data.get("status") == "rejected" or not data.get("sha256") or not has_original(data):
        return []
    try:
        actual = reg.original_sha256(data)
    except ValueError as exc:
        return [f"{data['id']}: {exc}"]
    if actual != data["sha256"]:
        return [f"{data['id']}: sha256 de l'original ({actual[:12]}…) ≠ registre ({str(data['sha256'])[:12]}…)"]
    return []


def check_artefacts(data: dict[str, Any]) -> list[str]:
    """Fichiers exigés par le statut, cohérence index / sections / registre."""
    sid = str(data.get("id") or "")
    status = data.get("status")
    if status not in ARTEFACT_STATUSES or not sid:
        return []
    sdir = reg.source_dir(sid)
    tag = f"{sid} [{status}]"
    errors: list[str] = []
    catalogue = data.get("extraction") == "catalogue"
    if not catalogue and not ((sdir / "raw.md").is_file() or any((sdir / "raw").glob("*.md"))):
        errors.append(f"{tag}: ni `raw.md` ni `raw/` (lancer `convert`)")
    redactions = data.get("redactions") or []
    for raw in redact.raw_files(sid):
        for i, r in enumerate(redactions, 1):
            if re.search(str(r["pattern"]), raw.read_text(encoding="utf-8")):
                errors.append(f"{tag}: `{raw.relative_to(sdir)}` contient encore le texte de redactions n°{i} "
                              f"(lancer `redact {sid}`)")
    if status == "verified" and not data.get("fidelity"):
        errors.append(f"{tag}: `fidelity` doit être renseigné (complete | partial)")
    if status == "converted":
        return errors

    index_path = sdir / "index.md"
    if not index_path.is_file():
        return errors + [f"{tag}: `index.md` absent"]
    try:
        front, roots = sp.parse_index(index_path.read_text(encoding="utf-8"))
    except sp.SplitError as exc:
        return errors + [f"{tag}: {exc}"]
    mismatch = sp.version_mismatch(front, data)
    if mismatch:
        errors.append(f"{tag}: {mismatch}")
    if catalogue:
        return errors

    listed = [s.file for s in sp.walk(roots)]
    on_disk = {p.name for p in sdir.iterdir() if p.is_file() and sp.SECTION_FILE_RE.match(p.name)}
    for extra in sorted(on_disk - set(listed)):
        errors.append(f"{tag}: `{extra}` absent d'index.md (rejouer `split`)")
    partial = reg.fidelity_of(data) == "partial"
    for name in listed:
        path = sdir / name
        if not path.is_file():
            errors.append(f"{tag}: section `{name}` listée dans index.md mais absente (rejouer `split`)")
            continue
        text = path.read_text(encoding="utf-8")
        sfront, body = sp.read_front(text)
        if str(sfront.get("version") or "") != str(data.get("version") or ""):
            errors.append(f"{tag}: `{name}` à la version `{sfront.get('version')}` (rejouer `split`)")
        if partial and sfront.get("fidelity") != "partial":
            errors.append(f"{tag}: `{name}` sans `fidelity: partial` (rejouer `split`)")
        for i, r in enumerate(redactions, 1):
            if sp.section_key(str(r.get("section", ""))) == name and re.search(str(r["pattern"]), body):
                errors.append(f"{tag}: `{name}` contient encore le texte de redactions n°{i} (rejouer `split`)")
    for i, r in enumerate(redactions, 1):
        if sp.section_key(str(r.get("section", ""))) not in listed:
            errors.append(f"{tag}: redactions n°{i} vise `{r.get('section')}`, absent d'index.md")
    return errors


def validate(sources: list[dict[str, Any]]) -> list[str]:
    """Hash et artefacts de sources déjà valides au sens du schéma."""
    errors: list[str] = []
    for data in sources:
        if not data.get("id") or not reg.source_path(str(data["id"])).exists():
            continue
        errors.extend(check_hash(data))
        errors.extend(check_artefacts(data))
    return errors


def run(check_only: bool = False) -> int:
    sources, errors = reg.validate_all()
    errors += validate(sources)
    ref_errors, ref_warnings = refs.check_all({str(s.get("id")): s for s in sources})
    errors += ref_errors
    for w in ref_warnings:
        typer.echo(f"avertissement : {w}", err=True)
    if errors:
        typer.echo(f"{len(errors)} erreur(s) :", err=True)
        for e in errors:
            typer.echo(f"  - {e}", err=True)
        return 1
    missing = sum(1 for s in sources if s.get("sha256") and s.get("status") != "rejected" and not has_original(s))
    if missing:
        typer.echo(f"note : {missing} original(aux) absent(s), sha256 non recalculé(s)", err=True)
    if check_only:
        typer.echo(f"✓ {len(sources)} source(s) et {len(refs.all_referentiels())} référentiel(s) valides")
        return 0
    reg.INVENTORY.write_text(render_inventory(sources, reg.load_taxonomy()), encoding="utf-8")
    typer.echo(f"✓ {len(sources)} source(s) → {reg.INVENTORY.relative_to(reg.ROOT)}")
    return 0


@app.command()
def main(check: bool = typer.Option(False, "--check", help="Valider sans écrire INVENTORY.md.")) -> None:
    """Valide le registre et écrit INVENTORY.md."""
    raise typer.Exit(run(check_only=check))


if __name__ == "__main__":
    app()

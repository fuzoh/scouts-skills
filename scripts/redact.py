"""`redact <id> | --all` : applique `redactions:` du yaml au texte brut (`raw.md`, web : `raw/*.md`).

Le caviardage est déclaré une fois dans le yaml, `redactions: [{section, pattern, replace}]`,
et appliqué partout où le texte passe : `convert` l'applique au texte brut avant
de rendre la main, `split` aux sections, `redact` rejoue l'étape brute sans
reconvertir. Rejouable : une règle sans correspondance est acceptée si son
`replace` est déjà présent (texte déjà caviardé) ; sinon refus (texte déplacé,
règle à revoir avant de la retirer).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import typer

from scripts import registry as reg

app = typer.Typer(add_completion=False, help=__doc__)


class RedactError(Exception):
    pass


def substitute(text: str, rule: dict[str, Any]) -> tuple[str, bool]:
    """Texte caviardé, et si la règle porte (motif trouvé, ou `replace` déjà présent)."""
    replace = str(rule.get("replace") or "")
    new, n = re.subn(str(rule["pattern"]), replace, text)
    return new, bool(n) or (bool(replace) and replace in text)


def raw_files(source_id: str) -> list[Path]:
    """`raw.md` et `raw/*.md` de la source, dans un ordre stable."""
    sdir = reg.source_dir(source_id)
    files = [sdir / "raw.md"] if (sdir / "raw.md").is_file() else []
    if (sdir / "raw").is_dir():
        files += sorted((sdir / "raw").glob("*.md"))
    return files


def redact_raw(source_id: str) -> list[Path]:
    """Caviarde le texte brut selon le yaml ; renvoie les fichiers réécrits. Rien n'est écrit en cas de refus."""
    data = reg.load_source(source_id)
    rules = data.get("redactions") or []
    if not rules:
        return []
    files = raw_files(source_id)
    if not files:
        raise RedactError(f"{source_id}: ni `raw.md` ni `raw/`, lancer `convert` d'abord")
    texts = {p: p.read_text(encoding="utf-8") for p in files}
    new = dict(texts)
    for i, rule in enumerate(rules, 1):
        hit = False
        for p in files:
            new[p], ok = substitute(new[p], rule)
            hit = hit or ok
        if not hit:
            raise RedactError(f"{source_id}: redactions n°{i} ne trouve rien dans le texte brut "
                              "(texte déplacé ? vérifier avant de retirer la règle)")
    changed = [p for p in files if new[p] != texts[p]]
    for p in changed:
        p.write_text(new[p], encoding="utf-8")
    return changed


@app.command()
def main(
    id: str = typer.Argument("", help="Identifiant de la source."),
    all_: bool = typer.Option(False, "--all", help="Toutes les sources qui déclarent `redactions`."),
) -> None:
    """Applique le caviardage du yaml au texte brut de la source."""
    if all_ == bool(id):
        typer.echo("refusé : donner un identifiant ou --all", err=True)
        raise typer.Exit(1)
    ids = [id] if id else [str(d["id"]) for d in reg.all_sources() if d.get("redactions")]
    failed = False
    for sid in ids:
        try:
            changed = redact_raw(sid)
        except (RedactError, FileNotFoundError) as exc:
            typer.echo(f"refusé : {exc}", err=True)
            failed = True
            continue
        for p in changed:
            typer.echo(f"✓ {p.relative_to(reg.ROOT)}")
        if not changed:
            typer.echo(f"= {sid} : texte brut déjà caviardé")
    raise typer.Exit(1 if failed else 0)


if __name__ == "__main__":
    app()

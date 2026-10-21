"""`build` : packs de distribution des skills `scouts` et `scouts-ressources`.

  build all [--zip] [--out DIR] [--dist DIR]
  build claude-code [--skill scouts|scouts-ressources] [--scope complet|referentiels] [--out DIR] [--zip] [--dist DIR]
  build install [--skill scouts|scouts-ressources] [--out DIR] [--skills-dir DIR]

Sources d'écriture dans `skills-src/<skill>/`, packs écrits dans `skills/<skill>/` (commités,
installables par `npx skills add`), zips dans `dist/<skill>.zip` (assets de release).

`--skill scouts` (défaut) : copie `skills-src/scouts/` tel quel dans `<out>/scouts/` (ni corpus,
ni référentiels de `referentiels/`, ni concepts) et ajoute un MANIFEST.md court. Refuse si
`light check` échoue.

`--skill scouts-ressources` : arborescence `<out>/scouts-ressources/` : SKILL.md, references/
(skills-src/scouts-ressources/references + glossaire + concepts), referentiels/, corpus/<id>/ (index.md
et sections ; jamais raw, original, recovered, source.yaml), MANIFEST.md. Refuse si les
référentiels ont une erreur ou citent une section absente du pack.

Déterministe : la version (`pyproject.toml`) est injectée dans le frontmatter du SKILL.md
(`metadata.version`) et dans MANIFEST.md, sans date ; zips à dates et droits fixes. Les lignes
de version portent `x-release-please-version` pour que release-please les tienne à jour.
"""

from __future__ import annotations

import re
import shutil
import zipfile
from pathlib import Path
from typing import Any

import typer
import yaml

from scripts import light
from scripts import referentiels as refs
from scripts import registry as reg
from scripts import split as sp

app = typer.Typer(add_completion=False, help=__doc__)

SCOPES = ("complet", "referentiels")
EMBEDDED_STATUSES = ("indexed", "verified")
LIMIT_MB = 30
PACK_NAME = "scouts-ressources"
LIGHT_NAME = light.SKILL_NAME
SKILLS = (LIGHT_NAME, PACK_NAME)


class BuildError(Exception):
    pass


REPO_URL = "https://github.com/fuzoh/scouts-skills"
LICENSES = {
    LIGHT_NAME: "CC-BY-SA-4.0",
    PACK_NAME: "CC-BY-SA-4.0 (corpus/ : textes officiels, droits à leurs auteurs)",
}
ZIP_DATE = (1980, 1, 1, 0, 0, 0)
SHARED_REFERENCE = "personnaliser.md"  # une seule source, dans skills-src/scouts/references/
VERSION_MARK = "x-release-please-version"


def default_out() -> Path:
    return reg.PACKS


def stamp_skill(path: Path, skill: str) -> None:
    """Ajoute `license` et `metadata` (version, source) au frontmatter du SKILL.md copié."""
    text = path.read_text(encoding="utf-8")
    m = sp.FRONT_RE.match(text)
    if not m:
        raise BuildError(f"{path} : frontmatter `---` manquant")
    front = yaml.safe_load(m.group(1)) or {}
    taken = [k for k in ("license", "metadata") if k in front]
    if taken:
        raise BuildError(f"{path} : `{'`, `'.join(taken)}` est injecté par `build`, à retirer de skills-src")
    added = (f'license: "{LICENSES[skill]}"\n'
             "metadata:\n"
             f'  version: "{reg.project_version()}" # {VERSION_MARK}\n'
             f'  source: "{REPO_URL}"')
    path.write_text(f"---\n{m.group(1)}\n{added}\n---\n{m.group(2)}", encoding="utf-8")


def manifest_head() -> list[str]:
    return ["# MANIFEST (généré par `build`, ne pas éditer)", "",
            f"- version : {reg.project_version()} <!-- {VERSION_MARK} -->",
            f"- source : {REPO_URL}"]


def select_sources(scope: str, referentiels: list[refs.Referentiel]) -> list[dict[str, Any]]:
    """Sources embarquées : indexées/vérifiées (complet) ou citées/canevas d'un référentiel."""
    ok = [s for s in reg.all_sources()
          if s.get("status") in EMBEDDED_STATUSES and s.get("decision") != "rejected"]
    if scope == "complet":
        return ok
    wanted: set[str] = set()
    for r in referentiels:
        wanted |= r.source_ids
        wanted |= {str(c) for c in (r.front.get("canevas") or [])}
    return [s for s in ok if str(s["id"]) in wanted]


def section_files(source_id: str) -> list[str]:
    idx = reg.source_dir(source_id) / "index.md"
    try:
        _, roots = sp.parse_index(idx.read_text(encoding="utf-8"))
    except (OSError, sp.SplitError) as exc:
        raise BuildError(f"`sources/{source_id}/index.md` illisible : {exc}") from exc
    return [s.file for s in sp.walk(roots)]


def check_citations(referentiels: list[refs.Referentiel], pack: dict[str, list[str]]) -> list[str]:
    errors: list[str] = []
    for r in referentiels:
        for c in r.citations:
            if c.source_id not in pack:
                errors.append(f"référentiel {r.slug} cite {c.source_id} absent du pack")
            elif c.section is not None:
                path = refs.resolve_section(c.source_id, c.section)
                if path is None or path.name not in pack[c.source_id]:
                    errors.append(f"référentiel {r.slug} cite {c.source_id}#{c.section} absent du pack")
    return sorted(set(errors))


def rewrite_concept_links(text: str) -> str:
    return text.replace("../../sources/", "../../corpus/")


INJECTED = ("title", "issuer", "ref", "nature", "applies_from", "applies_until", "fidelity",
            "extraction", "url", "file_url")


def enrich_index(text: str, data: dict[str, Any]) -> str:
    """Ajoute au frontmatter d'index.md les métadonnées de source.yaml (clés existantes conservées)."""
    m = sp.FRONT_RE.match(text)
    if not m:
        raise BuildError("index.md : frontmatter `---` manquant")
    front = yaml.safe_load(m.group(1)) or {}
    values = {k: (reg.fidelity_of(data) if k == "fidelity" else data.get(k)) for k in INJECTED}
    for k, v in values.items():
        if k not in front and v not in (None, ""):
            front[k] = v.isoformat() if hasattr(v, "isoformat") else v
    dumped = yaml.safe_dump(front, allow_unicode=True, sort_keys=False, width=1000).rstrip("\n")
    return f"---\n{dumped}\n---\n{m.group(2)}"


def _copy_tree(src: Path, dst: Path) -> int:
    n = 0
    for p in sorted(src.glob("*.md")):
        shutil.copy2(p, dst / p.name)
        n += 1
    return n


def _size_mb(root: Path) -> float:
    return sum(f.stat().st_size for f in root.rglob("*") if f.is_file()) / 1_000_000


def _write_zip(root: Path, dist: Path, name: str) -> Path:
    """Zip reproductible : ordre trié, date et droits fixes."""
    dist.mkdir(parents=True, exist_ok=True)
    zip_path = dist / f"{name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(root.rglob("*")):
            if f.is_file():
                info = zipfile.ZipInfo((Path(name) / f.relative_to(root)).as_posix(), ZIP_DATE)
                info.external_attr = 0o644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, f.read_bytes())
    return zip_path


def build_light(out: Path | None = None, make_zip: bool = False, dist: Path | None = None) -> dict[str, Any]:
    """Pack `scouts` : copie de `skills-src/scouts/` + MANIFEST.md, après `light check`."""
    out = out or default_out()
    skill_dir = reg.SKILLS / LIGHT_NAME
    if not (skill_dir / "SKILL.md").is_file():
        raise BuildError(f"{skill_dir / 'SKILL.md'} manque : rien à construire")
    rep = light.check(skill_dir)
    if rep.errors:
        raise BuildError(f"{LIGHT_NAME} invalide :\n" + "\n".join(f"  - {e}" for e in rep.errors))

    root = out / LIGHT_NAME
    if root.exists() or root.is_symlink():
        shutil.rmtree(root) if root.is_dir() and not root.is_symlink() else root.unlink()
    shutil.copytree(skill_dir, root)
    stamp_skill(root / "SKILL.md", LIGHT_NAME)

    derives: list[str] = []
    for slug, parts in light.referentiel_parts(skill_dir):
        front, _ = light.parse_front(parts[0].read_text(encoding="utf-8"))
        derives.append(f"- `{slug}` : derive_de `{(front or {}).get('derive_de')}`")
    manifest = [
        *manifest_head(),
        f"- fichiers : {rep.files + 1}",
        f"- mots : {rep.words}", "",
        "## Référentiels", "", *derives, "",
    ]
    (root / "MANIFEST.md").write_text("\n".join(manifest), encoding="utf-8")
    zip_path = _write_zip(root, dist or reg.DIST, LIGHT_NAME) if make_zip else None
    return {"root": root, "zip": zip_path, "files": rep.files + 1, "words": rep.words,
            "mb": _size_mb(root)}


def build_claude_code(scope: str = "complet", out: Path | None = None, make_zip: bool = False,
                      skill: str = LIGHT_NAME, dist: Path | None = None) -> dict[str, Any]:
    if skill not in SKILLS:
        raise BuildError(f"--skill `{skill}` inconnu ({', '.join(SKILLS)})")
    if skill == LIGHT_NAME:
        return build_light(out, make_zip, dist)
    if scope not in SCOPES:
        raise BuildError(f"--scope `{scope}` inconnu ({', '.join(SCOPES)})")
    out = out or default_out()
    skill_dir = reg.SKILLS / PACK_NAME
    if not (skill_dir / "SKILL.md").is_file():
        raise BuildError(f"{skill_dir / 'SKILL.md'} manque : rien à construire")

    known = {str(s.get("id")): s for s in reg.all_sources()}
    errors, _ = refs.check_all(known)
    if errors:
        raise BuildError("référentiels invalides :\n" + "\n".join(f"  - {e}" for e in errors))

    referentiels = refs.all_referentiels()
    sources = select_sources(scope, referentiels)
    pack = {
        str(s["id"]): [] if s.get("extraction") == "catalogue" else section_files(str(s["id"]))
        for s in sources
    }
    cite_errors = check_citations(referentiels, pack)
    if cite_errors:
        raise BuildError("\n".join(cite_errors))

    root = out / PACK_NAME
    if root.exists() or root.is_symlink():
        shutil.rmtree(root) if root.is_dir() and not root.is_symlink() else root.unlink()
    (root / "references" / "concepts").mkdir(parents=True)
    (root / "referentiels").mkdir()
    (root / "corpus").mkdir()

    shutil.copy2(skill_dir / "SKILL.md", root / "SKILL.md")
    stamp_skill(root / "SKILL.md", PACK_NAME)
    if (skill_dir / "references").is_dir():
        _copy_tree(skill_dir / "references", root / "references")
    shared = reg.SKILLS / LIGHT_NAME / "references" / SHARED_REFERENCE
    if shared.is_file():
        shutil.copy2(shared, root / "references" / SHARED_REFERENCE)
    if reg.GLOSSARY.is_file():
        shutil.copy2(reg.GLOSSARY, root / "references" / "glossaire.md")
    if reg.CONCEPTS.is_dir():
        for p in sorted(reg.CONCEPTS.glob("*.md")):
            text = rewrite_concept_links(p.read_text(encoding="utf-8"))
            (root / "references" / "concepts" / p.name).write_text(text, encoding="utf-8")
    if reg.REFERENTIELS.is_dir():
        _copy_tree(reg.REFERENTIELS, root / "referentiels")

    n_sections = 0
    for s in sources:
        sid = str(s["id"])
        dst = root / "corpus" / sid
        dst.mkdir()
        idx = (reg.source_dir(sid) / "index.md").read_text(encoding="utf-8")
        (dst / "index.md").write_text(enrich_index(idx, s), encoding="utf-8")
        for name in pack[sid]:
            src = reg.source_dir(sid) / name
            if not src.is_file():
                raise BuildError(f"section `{name}` listée par `sources/{sid}/index.md` mais absente")
            shutil.copy2(src, dst / name)
            n_sections += 1

    def label(s: dict[str, Any]) -> str:
        v = str(s.get("version") or "")
        return f"{s['id']}@{v}" if v else str(s["id"])

    manifest = [
        *manifest_head(),
        f"- scope : {scope}",
        f"- sources : {len(sources)}",
        f"- sections : {n_sections}",
        f"- référentiels : {len(referentiels)}", "",
        "## Sources embarquées", "",
        *[f"- `{label(s)}`" for s in sources], "",
    ]
    (root / "MANIFEST.md").write_text("\n".join(manifest), encoding="utf-8")

    zip_path = None
    if make_zip:
        zip_path = _write_zip(root, dist or reg.DIST, PACK_NAME)
    return {"root": root, "zip": zip_path, "sources": len(sources), "sections": n_sections,
            "referentiels": len(referentiels), "mb": _size_mb(root)}


def install_link(out: Path | None = None, skills_dir: Path | None = None, skill: str = LIGHT_NAME) -> str:
    """Lien `<skills_dir>/<skill>` → pack construit. Retourne « créé » ou « déjà installé »."""
    if skill not in SKILLS:
        raise BuildError(f"--skill `{skill}` inconnu ({', '.join(SKILLS)})")
    target = ((out or default_out()) / skill).resolve()
    if not target.is_dir():
        raise BuildError(f"{target} absent : lancer `build claude-code` d'abord")
    skills_dir = skills_dir or Path.home() / ".claude" / "skills"
    link = skills_dir / skill
    if link.is_symlink():
        if link.resolve() == target:
            return "déjà installé"
        raise BuildError(f"{link} est un lien vers {link.resolve()}, pas vers {target} : à retirer à la main")
    if link.exists():
        raise BuildError(f"{link} existe déjà et n'est pas un lien vers {target} : à retirer à la main")
    skills_dir.mkdir(parents=True, exist_ok=True)
    link.symlink_to(target, target_is_directory=True)
    return "créé"


@app.command("claude-code")
def claude_code(
    scope: str = typer.Option("complet", "--scope", help="complet | referentiels"),
    out: Path = typer.Option(None, "--out", help="Dossier parent du pack (défaut skills/)."),
    zip_: bool = typer.Option(False, "--zip", help="Produit aussi <skill>.zip (claude.ai, Gemini)."),
    skill: str = typer.Option(LIGHT_NAME, "--skill", help="scouts | scouts-ressources"),
    dist: Path = typer.Option(None, "--dist", help="Dossier des zips (défaut dist/)."),
) -> None:
    """Construit skills/<skill>/."""
    try:
        r = build_claude_code(scope, out, zip_, skill, dist)
    except BuildError as exc:
        typer.echo(f"Build refusé : {exc}", err=True)
        raise typer.Exit(1)
    _report(skill, r)


@app.command("all")
def all_(
    out: Path = typer.Option(None, "--out", help="Dossier parent des packs (défaut skills/)."),
    zip_: bool = typer.Option(False, "--zip", help="Produit aussi les zips dans --dist."),
    dist: Path = typer.Option(None, "--dist", help="Dossier des zips (défaut dist/)."),
) -> None:
    """Construit les deux packs (ce que la CI compare à skills/ commité)."""
    for skill in SKILLS:
        try:
            r = build_claude_code("complet", out, zip_, skill, dist)
        except BuildError as exc:
            typer.echo(f"Build refusé ({skill}) : {exc}", err=True)
            raise typer.Exit(1)
        _report(skill, r)


def _report(skill: str, r: dict[str, Any]) -> None:
    if skill == LIGHT_NAME:
        typer.echo(f"✓ {r['root']}\n  {r['files']} fichier(s), {r['words']} mot(s), {r['mb']:.2f} Mo")
    else:
        typer.echo(f"✓ {r['root']}\n  {r['sources']} source(s), {r['sections']} section(s), "
                   f"{r['referentiels']} référentiel(s), {r['mb']:.1f} Mo")
    if r["zip"]:
        typer.echo(f"  archive : {r['zip']}")
    if r["mb"] > LIMIT_MB:
        typer.echo(f"Avertissement : {r['mb']:.1f} Mo dépasse {LIMIT_MB} Mo (limite claude.ai).", err=True)


@app.command()
def install(
    out: Path = typer.Option(None, "--out", help="Dossier parent du pack (défaut skills/)."),
    skills_dir: Path = typer.Option(None, "--skills-dir", help="Défaut ~/.claude/skills."),
    skill: str = typer.Option(LIGHT_NAME, "--skill", help="scouts | scouts-ressources"),
) -> None:
    """Lie ~/.claude/skills/<skill> vers le pack construit."""
    try:
        res = install_link(out, skills_dir, skill)
    except BuildError as exc:
        typer.echo(f"Install refusée : {exc}", err=True)
        raise typer.Exit(1)
    typer.echo(f"✓ {res}")


if __name__ == "__main__":
    app()

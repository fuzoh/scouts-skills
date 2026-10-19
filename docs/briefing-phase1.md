# Briefing Phase 1 — outillage

Pour l'agent qui implémente la Phase 1. Tout a été décidé le 2026-10-17 avec le mainteneur ; ne pas rouvrir ces choix, les appliquer. Lire d'abord `AGENTS.md`, `METHODE.md`, `DECISIONS.md` (six entrées du 2026-10-17), `sources/_template.yaml`, `docs/taxonomie.md`.

## But

Livrer les scripts qui font passer une source de `documents/` (ou d'une URL) jusqu'à l'état `indexed`, et l'inventaire. Critère de fin : `314201fr-checklist_cours_base-v1-20260915-cofor.pdf` ingéré sous l'id `cofor-checklist-cours-base`, converti, indexé, découpé, `INVENTORY.md` généré, `just check` vert, un commit par script.

## Faits sur le corpus

- `documents/` : 123 entrées, 110 PDF (2676 pages), 4 docx, 3 xlsx, 2 pptx, 1 png, 2 dossiers de PNG allemands (illustrations profil et méthodes), 157 fichiers suivis par git (314 Mo).
- 3 doublons `(1).pdf`, 7 fichiers `T*.pdf` sans nom (à identifier en lisant la première page), 1 PDF scanné d'une page (`fr_ausbildungsmodell_fur_webseite-20231201_1.pdf`).
- 14/104 PDF ont des signets ; 2 manuels sur 14 de plus de 60 pages en ont. L'arbre des manuels viendra surtout des titres par police ou de l'agent.
- 6 PDF sont chiffrés AES (manuels J+S Bases, Coach, Trekking, experts) : `pypdf` échoue sans `cryptography`, `pymupdf` les lit.
- Outils système : `uv 0.13`, Python 3.14, `just`, `pdftotext`, `pdfinfo`, `pandoc`, `soffice`, `agent-browser`. Aucune lib Python PDF installée.
- Originaux commités tels quels, pas de LFS. `.gitignore` : `build/`, `.venv/`, `__pycache__/`.

## Forme du projet

- `pyproject.toml` à la racine, `requires-python = ">=3.14"`, package `scripts/` (ajouter `scripts/__init__.py`), CLI `typer`, un entry point par commande : `ingest`, `discover`, `convert`, `index`, `split`, `inventory`.
- Dépendances : `typer`, `pyyaml`, `pymupdf4llm` (vérifier que le mode layout `pymupdf-layout` n'est pas activé, il désactive la détection de titres), `markitdown`, `httpx`, `trafilatura`. Extra `web` : `playwright` (+ `playwright install chromium` documenté dans le justfile). `pytest` en dev.
- `justfile` : `ingest`, `convert`, `index`, `split`, `discover`, `inventory`, `check` (validation seule, sans écrire `INVENTORY.md`), `test`.
- Modèle du yaml et validation partagés dans un module `scripts/registry.py` (chargement, schéma, taxonomie depuis `docs/taxonomie.md`, règles d'id : `<issuer>-<slug>`, minuscules, tirets, sans accents, ≤ 40 caractères).
- Exécuter les scripts avec `uv run`, sans jamais lancer un interpréteur depuis `documents/`.

## Commandes

### `ingest`

- `ingest <fichier> --id <id> [--title ...] [--issuer ...]` : un fichier.
- `ingest --batch documents/lot.yaml` : liste d'entrées `{file, id, title, issuer, ref, version, published, audience, themes}` préparée par l'agent et validée par l'humain. Le fichier `lot.yaml` est supprimé après exécution (git garde la trace).
- `ingest --url <url> --id <id>` : source `type: web`, télécharge la page dans `original/` (html), `pages: 0`, `version` = date du jour.
- `ingest --batch manifeste.yaml` (sortie de `discover`) : pages regroupées par colonne `source`, fichiers téléchargés puis traités comme des fichiers locaux.
- `ingest --match manifeste.yaml` : pour chaque fichier du manifeste dont le sha256 égale celui d'une source existante, remplit `url` et `file_url` ; si seul le nom de fichier correspond, pose `stale: true` et le signale.
- Effets : calcule `sha256`, `pages` (PDF via pymupdf, pptx = diapos, sinon 0), `retrieved` (date du jour), crée `sources/<id>/source.yaml` depuis le template, **déplace** le fichier dans `sources/<id>/original/`, `status: collected`, `extraction: text`.
- Refus : sha256 déjà présent dans une source (doublon), id non conforme, id existant (sauf `--new-version` qui archive l'ancien dans `history` et repasse le statut à `collected`). Rien n'est déplacé en cas de refus.
- Type `image` : `ingest <dossier> --id ... --type image` copie le dossier entier dans `original/`, `extraction: vision`.

### `discover`

- `discover <url> --depth N [--render] [--out manifeste.yaml]`.
- Même hôte uniquement ; lit `robots.txt` et respecte `Disallow` et `Crawl-delay` ; au plus 1 requête/s ; `--render` utilise playwright pour les SPA.
- Manifeste : `pages: [{url, title, source: ""}]` et `files: [{url, name, size, sha256}]`. Les fichiers sont téléchargés en mémoire pour le hash, pas conservés.
- Ne crée jamais de source.

### `convert`

- `convert <id>` écrit `sources/<id>/raw.md`, écrase seulement ce fichier.
- PDF : `pymupdf4llm`, un marqueur `<!-- p.N -->` au début de chaque page, N = page physique 1..n.
- pptx : `markitdown`, `<!-- p.N -->` = diapo. docx : `markitdown`, pas de marqueur. xlsx : `markitdown`, un titre `#` par feuille.
- Web : `trafilatura` (ou playwright si `--render`), un `raw/<slug>.md` par page, frontmatter `{url, retrieved, sha256}` (hash du md), ancres HTML des titres conservées en `<!-- #ancre -->` juste avant le titre.
- `extraction: catalogue` ou `none` : `convert` refuse.
- Passe `status` à `converted`.

### `index`

- `index <id>` écrit un squelette `sources/<id>/index.md` sans écraser un `index.md` existant (option `--force`).
- Sources : signets PDF (`toc_source: bookmarks`), sinon titres markdown de `raw.md` (`toc_source: headings`). `toc_source: agent` est posé à la main quand l'arbre est réécrit.
- Numéro de chapitre extrait du titre quand il commence par un numéro (`3.2 Qualifier` → `§3.2`).
- `page_offset` : détecté si possible (numéro imprimé en pied de page vs page physique), sinon 0, l'agent corrige.
- Format : frontmatter `{source, version, pages, page_offset, toc_source}` puis une ligne par nœud, indentée de deux espaces par niveau : `- §3.2 Titre p.18-24 → 04-slug.md : résumé`. Résumé vide dans le squelette. Un document < 15 pages : une seule entrée `01-contenu.md`.
- Pour une source web : une ligne par page du manifeste, `→ NN-slug.md`, plages remplacées par l'url.

### `split`

- `split <id>` lit `index.md` et découpe `raw.md` en `NN-<slug>.md` selon les plages de pages (web : copie `raw/<slug>.md`). Rejouable : supprime les `NN-*.md` avant d'écrire.
- Frontmatter de section : `{source, version, chapter, pages: "18-24"}` ou `{source, version, url, sha256}`.
- Refuse si une plage chevauche ou dépasse `pages`, ou si deux lignes visent le même fichier.
- Ne change pas le statut : `indexed` est posé par l'humain après validation.

### `inventory`

- Valide tous les `sources/*/source.yaml` : champs obligatoires, valeurs de `type`, `status`, `extraction`, `audience` et `themes` contre `docs/taxonomie.md` (au plus trois thèmes), forme de l'id, cohérence dossier/id, `issuer_detail` si `issuer: autre`, présence du fichier dans `original/` sauf `rejected`.
- Toute erreur : liste complète sur stderr, code de sortie 1, `INVENTORY.md` non écrit.
- Sinon écrit `INVENTORY.md` : comptage par statut, table par audience, table par thème, liste `extraction: vision` et `catalogue`, liste `stale`.
- `inventory --check` : validation seule.

### `bench_index`

- Script jetable `scripts/bench_index.py`, pas d'entry point. PageIndex v0.4 installé dans un venv séparé (`uv venv .venv-bench`), mode `optimize="merge"` sans LLM. Compare l'arbre PageIndex et le squelette `index` sur « 01_Le cours.pdf » (67 p., sans signets), « Manuel J+S esa pour experts.pdf » (136 p., signets), « 212002fr_pfadiprofil_webb.pdf » (41 p.) contre leur table des matières imprimée. Résultat en une entrée `DECISIONS.md` ; si PageIndex gagne nettement, `index` l'appelle en option, sinon on le retire.

## Résumés et vision

- Les résumés d'`index.md` ne sont jamais écrits par `convert` ni `index`. Manuels : script `claude -p` en lot, à écrire plus tard. Documents courts : l'agent en session.
- Pas d'OCR, pas de modèle de vision en Phase 1. `extraction: vision` sert de marqueur pour plus tard.

## Ordre et commits

1. `pyproject.toml`, `scripts/__init__.py`, `scripts/registry.py`, `justfile`, `.gitignore` (+ `.venv-bench/`) — `chore(scripts): projet uv`
2. `ingest` + test — `feat(scripts): ingest`
3. `inventory` + test — `feat(scripts): inventory`
4. `convert` — `feat(scripts): convert`
5. `index` — `feat(scripts): index`
6. `split` — `feat(scripts): split`
7. `discover` — `feat(scripts): discover`
8. Test de bout en bout sur la checklist cours de base, commit de la source — `feat(sources): cofor-checklist-cours-base`
9. `bench_index` + entrée `DECISIONS.md` — `chore: benchmark index`
10. Relire `METHODE.md` contre les commandes réelles, mettre à jour `ROADMAP.md`, régénérer `INVENTORY.md`.

## Hors périmètre de cette phase

Ingestion des 123 fichiers (Phase 2, par lots d'émetteur), crawl de tool.jeunesseetsport.ch, catalogue de communagir et liberatingstructures, `check_urls`, `build`, skills.

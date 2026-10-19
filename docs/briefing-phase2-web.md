# Phase 2, partie web — livrée le 2026-10-17

Ce briefing a été exécuté ; il reste comme trace. État final et enseignements :

- 119 sources : 114 `triaged`, 1 `indexed`, 4 `rejected`. 3 sources `web` : `js-ethique-proximite-soutien` (1 page), `msds-hering-camps` (9 pages), `cudesch-cudeschin` (18 articles).
- 46 sources locales ont `url` + `file_url` pfadi.swiss retrouvées par sha256 ; `msds-modele-de-formation` (remplacé par l'export en ligne, même contenu, `--new-version`) et `msds-illustrations-profil` (zip) posées à la main ; 6 absentes du site, notées dans `notes`. Les sources J+S n'ont pas d'URL (extranet ILIAS ou jeunesseetsport.ch non crawlé).
- Manifestes dans `build/` (git-ignoré) : `pfadi.yaml` (site entier, 466 fichiers), `pfadi-catalogue.yaml` (775 entrées du Downloads avec titres et descriptions : utile pour repérer ce qui manque au corpus, ex. brochures de branche, cudesch 01-07, Ancre allemande), `hering.yaml`, `cudeschin.yaml`. Régénérer : `just discover …`, `uv run python -I scripts/catalogue_pfadi.py`.
- Les html des sources SPA dans `original/` sont des coquilles vides : `just convert <id> --render` (locale fr-CH posée dans `scripts/convert.py`).
- Détails dans `DECISIONS.md` (entrées du 2026-10-17 « Sources web » et « Triage Phase 2 ») et `METHODE.md` (Sources web).

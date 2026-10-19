# Roadmap

État du projet entre deux sessions. Mettre à jour en fin de session : cocher, noter la prochaine action, les blocages.

## Phase 0 — Méthode  ✅ 2026-10-17
- [x] Méthode de travail (`METHODE.md`)
- [x] Registre de source (`sources/_template.yaml`)
- [x] Taxonomie, glossaire initial, journal de décisions

## Phase 1 — Outillage minimal  (grill fait le 2026-10-17, voir `docs/briefing-phase1.md`)
- [x] `pyproject.toml` (uv, typer), package `scripts/`, `justfile`, `pytest` (29 tests)
- [x] `scripts/ingest.py` : fichier `--id` ou `--batch documents/lot.yaml` ; `--url` ; `--match manifeste` ; hash, pages, déplacement, refus des doublons
- [x] `scripts/inventory.py` : génère `INVENTORY.md`, valide les yaml, échoue sans générer
- [x] `scripts/convert.py` : PDF (pymupdf4llm), docx/pptx/xlsx (markitdown), web (trafilatura) → `raw.md`
- [x] `scripts/index.py` : squelette `index.md` (signets, titres par police, `page_offset`, `§chapitre`)
- [x] `scripts/split.py` : `raw.md` → `NN-slug.md` selon `index.md`
- [x] `scripts/discover.py` : manifeste d'un site (robots, 1 req/s, `--render` playwright en extra)
- [x] `scripts/bench_index.py` : PageIndex Flash (venv séparé) vs pymupdf4llm sur 3 manuels → `DECISIONS.md` ; `index --pageindex` ajouté
- [x] Test de bout en bout : `314201fr-checklist_cours_base-v1-20260915-cofor.pdf` jusqu'à `indexed`
- [x] `METHODE.md` relu après implémentation (table des commandes, format d'index, sémantique de split, manifeste)

Non testé en réel : `discover --render` et `convert --render` (playwright non installé), `ingest --batch manifeste` sur un vrai site, PDF chiffrés AES (pymupdf les ouvre, à confirmer en Phase 2).

## Phase 2 — Ingestion et triage des 121 entrées de `documents/`  (briefing : `docs/briefing-phase2.md`, suite : `docs/briefing-phase2-web.md`)
- [x] Fichiers sans nom identifiés par leur première page (table dans le briefing)
- [x] Doublons supprimés : 2 `(1).pdf`, `_Trekking.pdf` (= manuel SC/T 2026, même sha256), `Check-list Coach J+S.docx` (même contenu que le pdf) ; ancienne édition du manuel experts en `history`
- [x] Cinq lots ingérés (115 sources) : cofor 21, msds 28, js 60, cudesch 1, autre 5 ; un commit par lot
- [x] Triage validé : 112 `keep` → `triaged`, 4 `rejected` (2 italiens, communiqué Aqua Scout, dépliant Rega) ; `extraction: vision` sur 3 (scan, 2 dossiers PNG)
- [x] `documents/` vide, `just check` vert, `INVENTORY.md` régénéré (117 sources)
- [x] Article mobilesport ingéré (`js-ethique-proximite-soutien`, `collected`, à trier)
- [x] `discover` pfadi.swiss (377 pages, 466 fichiers) + catalogue Downloads paginé (`scripts/catalogue_pfadi.py`, 775 entrées) → `ingest --match` : 46 sources avec `url`/`file_url`, 2 posées à la main, 6 absentes du site (notées)
- [x] hering.scout.ch → `msds-hering-camps` (9 pages, SPA)
- [x] cudeschin.pbs.ch → `cudesch-cudeschin` (18 articles fr via locale `fr-CH`, manifeste à la main)
- [x] Triage des sources web : 114 `triaged`, 1 `indexed`, 4 `rejected`  ✅ Phase 2 close le 2026-10-17

## Phase 3 — Conversion et indexation  (briefing : `docs/briefing-phase3.md`, procédure de lot : `docs/briefing-phase3-lot.md`)
- [x] Priorité aux sources des anciens skills (trilogie formation, manuels experts et SC/T, profil, check-lists, Pano) : traitées en première vague
- [x] Conversion, index, découpage, concepts : 113 sources `indexed` (dont 2 catalogues, 3 web), 4 `vision` différées, 0 `converted` restante ; 17 commits par lot
- [x] `convert` corrigé en cours de route (texte masqué par les graphismes, jusqu'à 73 % perdu) : tout le corpus reconverti et re-découpé
- [x] Catalogues `autre-communagir-outils-animation` (78) et `autre-liberating-structures` (43)
- [x] Glossaire : ⚠ remplacés par des sources vérifiées, colonne `slug`, nouveaux termes
- [x] `just concepts` : `docs/concepts/<slug>.md` générés (index inversé source ↔ concept)
- [ ] `verified` : relecture humaine d'un index et d'une section par source (aucune encore)

## Phase 3b — Garanties et fidélité  (arbitrages du 2026-10-17, voir `DECISIONS.md`)
- [x] `_template.yaml` : `applies_from`, `applies_until`, `nature` (optionnels), `fidelity: complete | partial` + motif ; `inventory` valide
- [x] `split` propage l'avertissement de fidélité dans le frontmatter des sections ; refuse un `index.md` dont la version diffère du registre
- [x] `ingest --new-version` invalide (ou refuse) index et sections existants
- [x] `check` : artefacts requis par statut, sha256 de l'original recalculé
- [x] `convert --render` n'écrase plus `original/` (collecte et conversion séparées)
- [x] Caviardage des identifiants J+S (`redactions` dans le yaml, rejouable) : `js-intro-manuel-experts-diapos`, `msds-essentiel-msds-js-2027`, `js-manuel-sport-de-camp-trekking` ; `raw.md` intacts
- [x] `just recover` : 14 tableaux reconstitués (modèle de formation p.16-18, check-list cours de base, profil §3-4, tableaux relations) ; `msds-profil-tableaux-relations` passé de `vision` à `indexed`
- [x] (20 fiches ; six datées 2027-01-01 par déduction, à valider) `applies_*` et `nature` posés sur les sources prescriptives (modèle de formation, directives J+S, règlements)
- [x] (METHODE) `verified` redéfini : relecture ciblée des tableaux, cases et prescriptions

## Phase 4 — Design des skills
- [x] Grill Phase 4 tours 1-3 : organisation retenue (skill `scout`, `referentiels/`, trois niveaux, `[non officiel]`, packs, pilote) consignée dans DECISIONS et `docs/briefing-phase4-grill.md`
- [x] Mainteneur : canevas réels (4 vierges ingérés `autre-canevas-*`), dossiers réels de camps et d'UA déposés dans `documents/`
- [x] Analyse de terrain (`docs/briefing-terrain.md`, `scripts/terrain.py`, 6 lots en sous-agents) → `docs/terrain/` : camps, activités J+S, cours-UA, lexique, candidats pilote, notes par lot
- [x] Ingestion complémentaire : Thilo (`msds-thilo`, web), Alpha (`msds-alpha-aide-memoire-rg`), cuisine de camp J+S ; 178 sources
- [x] Mainteneur, premier tour (2026-10-17) : VC = AdA = AA gardés, CDF hors périmètre (AS), taxonomie du modèle de formation, archives jamais commitées (DECISIONS « Terrain : réponses du mainteneur »)
- [x] Terrain, second tour : `docs/terrain/securite.md` (nouveaux docs sécurité, canevas CdS cantonaux, annexes, tyroliennes), `docs/terrain/canevas-cantonaux.md` (13 canevas cantonaux vs groupe 2020 vs officiel, écart 2027) ; id `msds-retour-qualifier-accompagner` corrigé dans les docs terrain
- [x] Mainteneur (2026-10-18) : revue des critères annotée (normalisée : O 106 / G 51 / R 18 / ? 2 : QC-07, CU-18), réponses à `securite.md` §6, `canevas-cantonaux.md` §7, `cours-ua.md` §5 ; kit 2018 sans retour → proposition appliquée (I 5 / T 4 / N 61) ; `camps.md` §6 tranché par défaut (un seul référentiel pour camp d'unité et commun)
- [x] Canevas cantonaux, picasso, CdS global et annexes : **pas ingérés** (décision), règles déduites dans les référentiels comme trame non officielle
- [x] Kit 2018 : six sources ingérées en version courante et `indexed` (`msds-camps-a-l-etranger`, `msds-checklist-camps-a-l-etranger`, `js-guide-materiel-de-pret`, `autre-csaj-conge-jeunesse-fiche`, `autre-csaj-conge-jeunesse-formulaire`, `msds-assurance-tiers-conducteurs`) ; 184 sources
- [x] Premiers référentiels en **brouillon** (`referentiels/activite-js.md`, `concept-de-securite.md`, `programme-camp.md`, `ua.md`, ~120 lignes chacun, citations `id#NN-slug` toutes vérifiées ; briefing `docs/briefing-referentiels.md`) ; G et O reportés, R écartés
- [x] Relecture des quatre référentiels par le mainteneur (2026-10-18, quatre entrées DECISIONS) : `ua` N3 gardé + N4 cohérence objectifs/déroulement, GAG sourcé (J+S), IFV abandonné ; `concept-de-securite` N15 gardé, N5 allégé, N16 cellule de crise, toute randonnée a un CdS ; `programme-camp` délais 7/6 semaines confirmés par le calendrier de la Sardine en ligne, quota 2027 sourcé (`msds-essentiel-msds-js-2027`), vocabulaire (camp mixte, PF, AS ⊂ AA) ; `activite-js` N7 gardé, N14-N15 ajoutés, nuances du mainteneur étiquetées
- [x] Dépôt du mainteneur ingéré (2026-10-18, 186 sources) : `msds-essentiel-msds-js-2026` (newsletter nov. 2025 : 16+16+16, SAPC, sécurité ; identifiants caviardés p.11) et `js-structure-formation-sdct` (page BDNS « Structure de la formation » SdC/T, colonnes 2026 / 2027 reconstituées dans notes, `fidelity: partial`) ; la newsletter 2027 déposée était déjà au registre (même sha256)
- [x] QC-07 reformulé (exercice de cours) et CU-18 (« E » = R) tranchés en R : revue close, O 106 / G 51 / R 20
- [ ] **À ingérer quand ils existeront** : autorisation de camp 2027 (pas encore publiée selon le mainteneur), guide des offres OFSPO 2027 ; puis revérifier les critères fondés sur les check-lists 2026 et le quota 36 / +1 par 12. `js-structure-formation-sdct` servira au futur référentiel des cours (Cours introduction, Responsable de camp, modules 2027)
- [x] Jeu d'essai : candidats copiés en texte extrait et anonymisé dans `pilote/cas/` ; `documents/` archivé hors dépôt
- [x] Tour 4 du grill (2026-10-18, Q20-Q37) : format définitif des référentiels, `reglages.md`, grade de preuve du cudesch et affectations par référentiel, canevas = formats reconnus ; consigné dans DECISIONS et `docs/briefing-phase4-grill.md`
- [x] `docs/skills-design.md` : organisation, format des référentiels, réglages, `SKILL.md` de `scout` (plan), méthode de retour, `check`, cycle de vie, pilote
- [x] Quatre référentiels passés en `statut: relu` au format définitif (sections, portées, marques courtes, `parametres` typés, ajouts cudesch) ; `skills/scout/references/reglages.md` écrit
- [x] `SKILL.md` de `scout` (98 lignes) et squelettes `references/corriger.md`, `concevoir.md`, `chercher.md` ; `reglages.md` aligné (date du cours bloquante pour `ua`)
- [x] `check` étendu aux référentiels (`scripts/referentiels.py`, 24 tests) ; `build claude-code [--scope] [--zip]` + `just install` (`scripts/build.py`, 14 tests) ; premier pack 177 sources / 1 676 sections / 8,7 Mo, zip 4 Mo ; skill `scout` installé et détecté
- [x] Relecture agent des quatre référentiels (tous les N recoupés avec les sources) : corrections sûres appliquées (DECISIONS 2026-10-18 « `check` des référentiels… ») ; toujours `relu`
- [x] Mainteneur (2026-10-18) : `activite-js` N15 → Q17 ; `concept-de-securite` N8 constructions aligné sur `cudesch-securite#10` ; `ua` N3-N4 (brochures) gardés par décision antérieure
- [ ] Mainteneur : tests manuels du skill sur claude.ai et Gemini avec `build/claude-code/scouts-ressources.zip`, grille `pilote/tests-manuels.md`, résultats dans son tableau final
- [ ] Pilote : `scouts` + `activite-js`, `ua`, `programme-camp` ; `pilote/` (cas, attendus, rapport), 12-15 cas, contre-épreuve, comparé aux anciens prompts
- [ ] Migrer les 3 anciens prompts (correcteur UA, AC, SC ; corriger « aussi d'une AC » dans le prompt SC) vers `skills/`
- [ ] `scripts/build.py` : packs aplatis Claude Project / GPT (`camp`, `formation`) après le pilote ; `--check-limits`

## Phase 4b — `scouts` (ex `scout-light` ; 2026-10-18, DECISIONS « Second skill scout-light » et « Retours du premier test », briefing `docs/briefing-scout-light.md`)
- [x] `skills/scout-light/` : SKILL.md, references (glossaire ×2, réglages, corriger, concevoir), 4 référentiels en dossiers (activite-js 4, concept-de-securite 4, programme-camp 5, ua 3 fichiers), savoirs (camp ×2, J+S ×3, sécurité ×4, protection, formation ×3, profil / branches / pédagogie), `savoirs/README.md`
- [x] `scripts/light.py` (`just light-check` et `light index`, dans `just check`), `build claude-code --skill scout-light --zip`, `just install-light`, 15 tests ; relecture croisée par un agent : N équivalents aux quatre référentiels scout, chiffres identiques entre savoirs et référentiels, aucune correction nécessaire ; pack 40 fichiers, 0,2 Mo, `scout-light.zip` 93 Ko
- [x] Premiers retours du mainteneur (`pilote/retours-en-vrac.md`) intégrés : renommage `scouts` / `scouts-ressources`, cadrage silencieux (plus de ligne de plan), jeu 2027 par défaut, réponse univoque (dossier de camp : 4 semaines), pas de provenance entre parenthèses ni de mention du skill, « Pour aller plus loin », verbe guider (`references/guide.md`), catalogue `references/documents.md`, savoir `formation-rqa.md` (qualification comme outil pédagogique) ; les mêmes règles de posture appliquées à `scouts-ressources` ; `just zips`, `just install`, `just install-ressources`
- [x] (2026-10-18 : tout relu, 21 fichiers passés `valide`, tag `v0.1.0`) Mainteneur : second tour de tests de `scouts.zip` (grille `pilote/tests-manuels.md` mise à jour : 0.1, 0.2, 0.4, 0.5, 2.1, 2.2, 3.1, 4.4) ; relire les `brouillon` (points signalés par les agents : RG / responsable de camp, âges J+S 5-20 ans, quota 36/+12 pour 2027, délais Sardine non ingérés, facteurs kme) et le nouveau `formation-rqa.md`
- [x] Revue de contenu post-v0.1.0 intégrée (2026-10-18) : marche prudente avec/sans bagages, gilets et exception CPR, numéros d'urgence, jeux 2026/2027, délais, formation et glossaires corrigés ; points incertains arbitrés dans `DECISIONS.md`. Dérivés alignés, inventaire/index régénérés, 102 tests réussis, deux packs reconstruits. Douze cas manuels de non-régression ajoutés, pas encore exécutés.
- [x] (2026-10-19) Buts, objectifs numérotés, conditions et niveaux d'approfondissement de tous les cours du modèle de formation 2027 : `savoirs/formation-cours-{base,continue,cadres}.md` (`brouillon`), à nombre de fichiers constant (42) ; plafond 1 200 mots, 2 500 pour ces trois fichiers ; fusions camp, urgence + protection, activite-js 4 → 3 (DECISIONS « Buts et objectifs des cours »)
- [ ] Mainteneur : relire les trois `formation-cours-*.md` contre le modèle de formation et les passer `valide`
- [ ] Routine : re-dériver un dossier de `scouts/referentiels/` quand `relu_le` de son référentiel `referentiels/` change

## Phase 6 — Publication  (grill du 2026-10-19, briefing : `docs/briefing-publication.md`)
- [x] Recherche (install agents et web, release-please, CI, Pages) et grill : décisions D1-D12 consignées
- [x] Assainissement : identifiants caviardés jusque dans le texte brut (`redact`, `convert`), lieu de camp retiré d'un canevas, originaux et `pilote/cas/` hors git, `check` sans originaux ; `docs/terrain/`, `ancien skills/`, `docs/propositions/`, `idées.md`, `GOALS.md`, `pilote/retours-en-vrac.md` restés dans l'archive locale du mainteneur (seul `docs/lexique-terrain.md` publié)
- [x] Nouveau dépôt local (historique neuf), sans push ; historique réécrit en un seul commit initial, tag `v0.2.0` (2026-10-19)
- [x] `skills/` généré et commité depuis `skills-src/`, build déterministe, version injectée (`metadata.version`, MANIFEST)
- [x] Workflows : `ci.yml`, `release-please.yml` (+ upload des zips), `pages.yml` (sur tag `v*` seulement), `veille.yml` (`check-urls`) ; jactionlint propre (permissions par job, timeouts, `persist-credentials: false`, pas de cache uv pour les zips publiés)
- [x] Site (`uv run site`, 14 pages, sources générées depuis le registre, versions depuis `CHANGELOG.md`, page « Mettre à jour »)
- [x] README, LICENSE (MIT), LICENSE-CONTENT (CC BY-SA 4.0), CONTRIBUTING, formulaires d'issue, modèle de PR
- [x] Check de publication (briefing §3.7) sur un clone neuf sans originaux ; réglages post-push dans `docs/publication-reglages.md`
- [x] (2026-10-19) Dépôt `fuzoh/scouts-skills` créé, `main` et `v0.2.0` poussés, réglages appliqués (secret, Pages, PR des workflows, étiquettes), release `v0.2.0` avec zips
- [ ] Après le push : vérifier le jsonpath `uv.lock` de release-please (PR de release verte), le job `upload`, le déploiement Pages, l'issue de veille
- [x] Choix faits sans le mainteneur, validés (DECISIONS 2026-10-19 « Choix validés ») : Mistral/Copilot en mention courte, veille silencieuse, titulaire des licences `fuzoh`, sigle de l'association cantonale retiré
- [x] Tests web du mainteneur : `scouts` ok sur claude.ai et Gemini (Customize > Skills, import du zip) ; `scouts-ressources` trop lourd pour claude.ai et Gemini, ok sur ChatGPT ; site mis à jour
- [x] Site testé en ligne (agent-browser : 14 pages, mobile, mode sombre) ; débordement mobile corrigé ; mise en page 1280 px, violet MSdS, version et date dans l'en-tête
- [x] `npx skills add fuzoh/scouts-skills` (projet, `-g`, zips de release) et `npx skills update` testés depuis GitHub
- [ ] Tests « non testé » du site : `pi install git:…`, `scouts` sur ChatGPT, une vraie mise à jour d'une version à la suivante ; limite de 200 caractères de `description` annoncée par l'aide claude.ai (zips acceptés jusqu'ici)
- [ ] Veille, premier passage complet (2026-10-19) : 40 `url` `pfadi.swiss/.../downloads/detail/N/` en 404 (l'URL avec slug fonctionne, fichiers ok) à corriger dans le registre ; `msds-illustrations-profil` : zip distant changé, à réingérer en local
- [ ] Plus tard (DECISIONS « questions ouvertes tranchées ») : marketplace de plugins Claude Code ; sources web plutôt que PDF

## Phase 5 — Maintenance
- [ ] `scripts/check_urls.py` : détection `stale`
- [ ] Routine de mise à jour documentée

## Prochaine action
Relire `skills-src/scouts/savoirs/formation-cours-*.md` (numéros d'objectifs, verbes, niveaux) puis les passer `valide`. Ensuite : corriger dans le registre les 40 `url` `pfadi.swiss/.../downloads/detail/N/` en 404 (prendre l'URL avec slug) et réingérer `msds-illustrations-profil` ; tester `pi install git:github.com/fuzoh/scouts-skills` ; tests manuels 8.1–8.12.

Ancien état (2026-10-19, avant le push) : Le mainteneur relit le site (`uv run site --out build/site`, puis ouvrir `build/site/index.html`), commite l'arbre en un seul commit initial (historique réécrit, 2026-10-19) et pose le tag `v0.2.0`. Ensuite : créer `fuzoh/scouts-skills`, pousser `main` et `v0.2.0`, appliquer `docs/publication-reglages.md` (dont la release `v0.2.0`), vérifier la PR de release-please, corriger les URL de la veille. Tests manuels 8.1–8.12 toujours à faire.

Ancien état (2026-10-19, avant la réécriture de l'historique) : Le mainteneur relit le site (`uv run site --out build/site`, puis ouvrir `build/site/index.html`) et commite ses corrections. Avant le push, décider si l'historique local (17 commits) est publié tel quel : il contient encore le sigle de l'association cantonale et l'ancien titulaire de `LICENSE` ; le dépôt n'étant pas poussé, on peut le réécrire (un seul commit initial, tag `v0.1.1` reposé). Ensuite : créer `fuzoh/scouts-skills`, pousser `main` et `v0.1.1`, appliquer `docs/publication-reglages.md`, vérifier la PR de release-please, corriger les URL de la veille. Tests manuels 8.1–8.12 toujours à faire.

Ancien état (2026-10-19, avant la relecture du site) : Le mainteneur relit le dépôt local (site : `uv run site --out build/site`, puis `build/site/index.html`), crée le dépôt GitHub `fuzoh/scouts-skills`, pousse `main` et `v0.1.1`, puis applique `docs/publication-reglages.md`. Ensuite : premier PR de release-please à vérifier, corrections d'URL de la veille. Tests manuels 8.1–8.12 toujours à faire (ci-dessous).

Ancien état (2026-10-19, avant la mise en œuvre) : Phase 6 : lancer l'agent de conception sur `docs/briefing-publication.md` (commencer par §3.1, trancher les questions ouvertes §4 au fil de l'eau). Ne pas créer le dépôt GitHub ni pousser. En parallèle, tests manuels 8.1–8.12 de `v0.1.1` (ci-dessous).

Ancien état (2026-10-19, avant la Phase 6) : Tester les deux packs corrigés de `v0.1.1` (`build/claude-code/scouts.zip` et `scouts-ressources.zip`) avec les cas 8.1–8.12 de `pilote/tests-manuels.md`, puis distribuer aux collègues. Cette version corrective intègre la revue de contenu postérieure à `v0.1.0`. Recueillir les retours dans `pilote/retours-en-vrac.md` en notant la version. Toujours en attente de l'autorisation de camp 2027 et du guide des offres 2027 ; délais précis de clôture BDNS du camp et des comptes à revérifier dans le calendrier Sardine avant de les chiffrer.

Ancien état (2026-10-18, avant v0.1.0) : Le mainteneur refait un tour de tests avec `build/claude-code/scouts.zip` (principal) et `scouts-ressources.zip` sur claude.ai et Gemini, grille `pilote/tests-manuels.md` (règles communes en tête : pas de ligne de plan, jeu 2027 par défaut, une seule valeur, « Pour aller plus loin » ; reconstruire : `just zips`). Points à vérifier en priorité : la ligne de plan a bien disparu, le défaut 2027, la réponse « 4 semaines » pour le dossier de camp, le verbe guider, la qualification présentée d'abord comme outil pédagogique. Au retour : nouveaux retours dans `pilote/retours-en-vrac.md` ou ✗ / ~ dans la grille, corrections, puis décider si le pilote scripté (`docs/skills-design.md` § 8) reste utile. Toujours en attente de l'autorisation de camp 2027 et du guide des offres 2027.

Ancien état (2026-10-18 soir, avant les retours) : le mainteneur teste les deux skills (`scout.zip`, `scout-light.zip`), 45 tests.

Ancien état (2026-10-18 après-midi) : pilote scripté (attendus pour 12-15 cas de `pilote/cas/`, camps 2026 et 2027 redatés depuis P3 et P7, contre-épreuve, rapport) ; mis en pause, le mainteneur préférant tester lui-même.

Ancien état (2026-10-18 midi) : `check` étendu aux référentiels, puis `SKILL.md` de `scout`, puis `build claude-code` + `just install` ; relire les quatre référentiels avant `valide`.

Ancien état (2026-10-18 soir) : tour 4 du grill à faire (sources cudesch par référentiel, `reglages.md`, format définitif).

Ancien état (2026-10-18 matin) : le mainteneur annote les deux documents de revue et répond aux questions de `securite.md` §6 et `canevas-cantonaux.md` §7.

Ancien état (2026-10-17, premier tour terrain) : relire `docs/terrain/` et trancher les questions ouvertes ; décider du sort des dossiers réels (non commités, texte extrait dans `build/terrain/`, rejouable par `uv run python -I scripts/terrain.py`). Liste du kit administratif 2018 désormais dans `docs/revue-kit-administratif-2018.md`.

Ancien état : Grill Phase 4 : tours 1 à 3 répondus et consignés (`docs/briefing-phase4-grill.md`, section « État du grill et reprise » ; DECISIONS « Organisation des skills »). **Bloqué sur le mainteneur** : dépôt des canevas réels (vides et remplis) dans `documents/`, documents du jeu d'essai dans `documents/pilote/`, fichiers des anciens Gems s'il y en a, relecture de la liste d'ingestion Q8. Reprendre par le tour 4 (analyse des canevas, sources cudesch des référentiels, `reglages.md`), puis `docs/skills-design.md`, puis l'ordre des travaux Q19. En parallèle : agent Herdr `cudesch` (branche `cudesch`, worktree `~/.herdr/worktrees/skills-scoutisme/cudesch`) toujours en cours ; fusionner sa branche quand `docs/cudesch-rapport.md` existe, puis répondre à Q9.

## Points à arbitrer (remontés par les agents de Phase 3 ; tranchés le 2026-10-17 → Phase 3b, sauf mention)
- ✅ (caviardage sections + notes) **Identifiants en clair dans deux sources** : `js-intro-manuel-experts-diapos` (diapo 20) et `msds-essentiel-msds-js-2027` (p.4) contiennent un identifiant et un mot de passe d'accès à l'espace J+S, présents dans l'original, `raw.md` et la section. À ne jamais reprendre dans un skill ; décider s'il faut caviarder les sections (le `raw.md` n'est jamais édité à la main).
- ✅ (script de récupération des icônes) `msds-profil-tableaux-relations` reste en `vision` : la grille branche × objectif est détruite par la conversion ; `pdftotext -layout` garde l'alignement, piste pour un convertisseur « layout » optionnel. Même perte, moins grave, sur les tableaux par branche de `msds-profil-du-scoutisme` §3-4 (contenu clé du correcteur d'UA).
- ✅ (`fidelity`) Pertes résiduelles de conversion : ~17 % des pages perdent 5-15 % de leurs mots (en-têtes, pieds de page, première ligne des zones de texte sur les PDF de diapositives). Référence pour un contrôle : `page.get_text()`.
- ✅ (séparation) `convert --render` écrase `original/<slug>.html` sans mettre à jour `sha256` (sources web) : à décider avec `check_urls`.
- `version` vide dans beaucoup de fiches J+S alors que le document porte une date d'édition ; `ref` parfois différent de la référence imprimée (noté dans `notes`).
- Les `concepts` sont posés par source, pas par section ; `relations` désigne les relations du profil (retiré de `js-climat-d-apprentissage`).
- `msds-le-cours` et la trilogie sont des versions de travail (renvois « LIEN » non résolus, marques Word) : surveiller une version finale sur pfadi.swiss.

## Journal
- 2026-10-19 (formation) : buts et objectifs des cours ajoutés à `scouts` en trois savoirs rédigés par sous-agents sonnet ; fusions pour garder 42 fichiers ; plafond `light` 1 200 / 2 500 mots.
- 2026-10-19 (après push) : dépôt publié, release `v0.2.0` ; installation `npx skills` et site testés ; style du site (1280 px, violet MSdS, angles carrés, version et date en en-tête) ; nouvelle version par release-please.
- 2026-10-19 (avant push) : tour de relecture ; e-mail personnel d'un contact caviardé (`msds-assurance-tiers-conducteurs`) ; chemins locaux retirés ; page « Mettre à jour » et page « Nouveautés » générée depuis `CHANGELOG.md` ; version 0.2.0 ; historique à réécrire en un commit (laissé indexé pour le mainteneur).
- 2026-10-19 (reprise) : lien de `pilote/tests-manuels.md` corrigé ; choix faits sans le mainteneur validés ; licences au nom de `fuzoh` ; sigle de l'association cantonale retiré des fichiers versionnés ; résultats des tests web reportés sur le site (`scouts-ressources` : ChatGPT seulement). Rien de poussé.
- 2026-10-19 (publication) : dépôt public neuf préparé (assainissement, `skills-src/` → `skills/`, build déterministe, CI, release-please, Pages, veille, site, licences, formulaires) ; trois sous-agents en worktrees (workflows, veille, site) ; questions ouvertes tranchées (DECISIONS) ; check §3.7 vert sur clone neuf. Rien de poussé.
- 2026-10-19 : grill de publication (dépôt public neuf `fuzoh/scouts-skills`, originaux hors git, `skills/` généré, release-please, Pages, issues, veille mensuelle) ; recherche en deux sous-agents sonnet ; `docs/briefing-publication.md`, DECISIONS.
- 2026-10-18 (version corrective v0.1.1) : à la demande du mainteneur, corrections de la revue commitées, tag `v0.1.1` et deux packs régénérés. Tests manuels 8.1–8.12 toujours à exécuter ; pas de push.
- 2026-10-18 (revue de contenu post-v0.1.0) : revue traitée en trois blocs parallèles (sécurité, camp/J+S, formation/profil), glossaires et squelettes relus, contrôle croisé final contre le corpus. Arbitrages : bas de fourchette de marche non officiel, seuil d'annonce prudent dès trois jours, délais après-camp non confirmés retirés, règles 2026/2027 distinguées, modèle de formation et chapitres détaillés prioritaires. `uv run inventory --check`, `uv run light check`, 102 tests et builds des deux zips réussis ; `just` absent dans l'environnement, commandes `uv` équivalentes utilisées. `INVENTORY.md`, concepts et index des savoirs régénérés ; cas manuels 8.1–8.12 ajoutés, non exécutés. Aucun changement du corpus source ni nouveau tag.
- 2026-10-18 (soir) : retours du premier test de `scout-light` intégrés (DECISIONS « Retours du premier test ») : renommage `scouts` / `scouts-ressources` (dossiers, scripts, justfile, tests, docs), cadrage silencieux, jeu 2027 par défaut, univocité, posture d'assistant, « Pour aller plus loin », `references/guide.md`, `references/documents.md`, `savoirs/formation-rqa.md`, glossaires (qualification) ; grille de tests manuels mise à jour ; `just zips`.
- 2026-10-18 (après-midi, suite) : Phase 4b `scout-light` livrée en huit sous-agents sonnet (quatre référentiels en dossiers, quinze savoirs, références, outillage, relecture croisée) ; SKILL.md par le parent ; plafond relâché de 20 à 200 fichiers en cours de route ; DECISIONS, METHODE, skills-design § 10.
- 2026-10-18 (après-midi) : N15 de `activite-js` déclassé en Q17, N8 de `concept-de-securite` aligné sur le cudesch (DECISIONS) ; grille de tests manuels `pilote/tests-manuels.md` ; zip reconstruit. Pilote scripté mis en pause.
- 2026-10-18 (midi) : ordre Q19 (1)-(2) en quatre sous-agents : `scripts/referentiels.py` (check, intégré à `just check` et `ingest --new-version`), `skills/scout/SKILL.md` + trois squelettes, `scripts/build.py` (`build claude-code`, `install`), relecture des quatre référentiels avec corrections sûres appliquées ; six canevas `nature: exemple`, quatre `autre-canevas-*` en `indexed` ; 87 tests ; skill installé dans `~/.claude/skills/scout`.
- 2026-10-18 (nuit) : tour 4 du grill (Q20-Q37) en deux rounds ; `docs/skills-design.md` et `reglages.md` écrits ; quatre référentiels remis au format définitif par sous-agents sonnet (un par fichier) et passés en `relu` ; note du rapport cudesch corrigée (modèles de programme = J+S) ; METHODE § Skills, DECISIONS, briefing mis à jour.
- 2026-10-18 (soir) : relecture des quatre référentiels par le mainteneur, guidée document par document (guides de relecture de `programme-camp` et `activite-js` rédigés par sous-agents sonnet dans `build/relecture/`) ; décisions appliquées dans les référentiels, le glossaire (GAG, camp mixte, AS type d'AA), la revue (FO-11 → G), le lexique terrain (PF, IFV/GAG) et DECISIONS (quatre entrées). Sardine en ligne = `msds-hering-camps` ; son calendrier (hering.scout.ch/fr/calendar) relevé pour les délais. Commité (310f015), puis dépôt du mainteneur ingéré : deux nouvelles sources, 186 au registre.
- 2026-10-18 : retours du mainteneur intégrés (revues normalisées, questions terrain tranchées, DECISIONS « Revues tranchées ») ; canevas cantonaux non ingérés ; kit 2018 : six sources ingérées (184) ; quatre référentiels en brouillon rédigés par sous-agents sonnet ; glossaire +8 termes (CdS, matrice, PF, AA, AS, remplacement, programme général / détaillé) ; jeu d'essai anonymisé dans `pilote/cas/` ; `documents/` archivé hors dépôt.
- 2026-10-17 (terrain) : dépôt de 3 829 fichiers réels (16 camps 2009-2021, 2 cours) ; extraction `scripts/terrain.py` (2 463 textes), 6 lots analysés par sous-agents sonnet, synthèses `docs/terrain/`. Thilo, Alpha, cuisine J+S, 4 canevas vierges ingérés et indexés (178 sources). Cinq PDF isolés de `camps/` supprimés (versions périmées de formulaires déjà au registre).
- 2026-10-17 (grill tours 2-3) : réponses consignées, « canevas » réservé aux modèles officiels (terme pris dans `msds-le-cours`), référentiels nommés, vocabulaire 2027 vérifié (plus d'AC/SC dans le manuel SdC/T 2026), entrée DECISIONS « Organisation des skills », METHODE § Skills mis à jour. Attente des canevas du mainteneur.
- 2026-10-17 (Phase 3b + grill) : revue externe arbitrée (DECISIONS), Phase 3b livrée en 3 sous-agents et commitée ; grill Phase 4 tour 1 et 2, trois propositions d'organisation, contraintes plateformes, écart cudesch (numérique sur cudesch.scout.ch/fr) ; agent Herdr lancé sur branche `cudesch`.
- 2026-10-17 (suite) : Phase 3 livrée en deux vagues de sous-agents (6 lots courts/manuels prioritaires/web, puis 8 lots de manuels + catalogues + glossaire). Bug majeur de `convert` trouvé et corrigé (graphismes masquant le texte), `split` par feuille xlsx, ancres web sur ancêtre, `lang: en`, `just concepts`. 113 `indexed`.
- Revue d'ensemble (sans modification du pipeline) : 31 tests et validation des 119 registres verts. Points à arbitrer avant généralisation : pilote de skill évalué de bout en bout ; dates d'applicabilité et autorité des sources ; contrôle des pertes de conversion (notamment cases de niveau de la check-list) ; validation des artefacts et des hashes selon le statut ; invalidation des index/sections lors d'un changement de version. Reproduit en environnement temporaire : `split` accepte un index v1 avec un registre v2 ; `check` accepte `verified` sans artefacts et sans vérifier le hash de l'original. Recommandations, pas décisions actées.
- 2026-10-17 (nuit) : Phase 2 close. URL pfadi.swiss par sha256, hering et cudeschin ingérés, `discover` corrigé (redirections), rendu en locale fr-CH, `scripts/catalogue_pfadi.py`.
- 2026-10-17 (soir) : Phase 2 locale livrée : 115 sources ingérées en 5 lots, triées, `documents/` vide. Article mobilesport ingéré. `discover` pfadi.swiss et `install-web` lancés en fin de session.
- 2026-10-17 : Phase 0 et Phase 1 livrées (10 commits). Benchmark PageIndex → `index --pageindex`. Première source `cofor-checklist-cours-base` à `indexed`.

## Blocages
Aucun.

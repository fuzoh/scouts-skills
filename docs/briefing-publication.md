# Briefing Phase 6 — Publication (dépôt public, CI, releases, site)

Grill du 2026-10-19 avec le mainteneur. Ce document fixe les décisions et la liste des tâches pour l'agent de conception. Les faits techniques ont été vérifiés le 2026-10-19 sur les sources primaires (URL en fin de document) ; ce qui reste incertain est marqué **à tester**.

## 1. Décisions prises

| # | Sujet | Décision |
|---|---|---|
| D1 | Dépôt | **Un seul dépôt public** `fuzoh/scouts-skills`, **créé de zéro** (nouvel historique propre). Le dépôt actuel reste archivé en local comme référence. **Ne pas créer le dépôt GitHub ni pousser** : tout se prépare en local, le mainteneur poussera lui-même. |
| D2 | Originaux | Tous les `sources/*/original/` **hors git** (dossier ignoré, gardé en local + archive Sync). `url` / `file_url` et `sha256` restent au registre. Piste : préférer une variante web quand le PDF est en ligne. |
| D3 | Identifiants J+S | Caviardés **aussi dans `raw.md`** (4 sources, cf. §3.1). Mentionner sur la page des sources qu'un caviardage a eu lieu. |
| D4 | Droits | Tous les documents utilisés sont publics et redistribuables (selon les infos du mainteneur). Une page du site liste chaque source : titre, auteur/émetteur, lien vers l'original. |
| D5 | Données réelles | `pilote/cas/` **retiré** du dépôt public (local seulement). `docs/terrain/` gardé après relecture d'anonymisation (groupes, lieux, années identifiantes) ; question ouverte : utilité réelle pour les skills, éventuelle extraction plus abstraite (Q-ouverte 1). |
| D6 | Skills publiés | **Les deux** : `scouts` (principal) et `scouts-ressources` (formateur·ices, approfondissement). |
| D7 | `skills/` | `skills/` contient désormais les **packs générés et commités** (`skills/scouts/`, `skills/scouts-ressources/` corpus inclus), pour `npx skills add fuzoh/scouts-skills`. Les sources d'écriture actuelles de `skills/` déménagent (nom proposé : `skills-src/`). La CI échoue si `skills/` n'est pas à jour. |
| D8 | Distribution | Zips en **assets de release** (publics, permanents) ; artefacts d'action en plus sur la CI (inspection, 7 j). Lien stable `releases/latest/download/<skill>.zip` ⇒ **pas de `"prerelease": true`**. |
| D9 | Releases | release-please, config calquée sur celle du mainteneur (cf. §4.2), token PAT en secret. |
| D10 | Retours | **Issues GitHub avec formulaires** (pas de Discussions, pas de formulaire externe). |
| D11 | Veille | Workflow **mensuel** qui vérifie les `url` / `file_url` du registre et **ouvre ou met à jour une issue récapitulative** (pas de PR : la ré-ingestion reste locale). |
| D12 | Licences | Code (`scripts/`, workflows) **MIT** ; contenu propre (skills, référentiels, savoirs, site, docs) **CC BY-SA 4.0** ; textes officiels : droits à leurs auteurs, listés sur la page des sources. |

## 2. État constaté (audit du 2026-10-19)

- Pas de README racine, pas de LICENSE, pas de CHANGELOG, pas de `.github/`. `origin` = chemin local.
- `.git` = 320 Mo, 600 fichiers sous `original/` (PDF, html, docx, pptx, xlsx, png).
- Identifiants J+S en clair dans `raw.md` de : `js-manuel-sport-de-camp-trekking` (l.257-258, **sans `redactions` dans le yaml, à ajouter**), `js-intro-manuel-experts-diapos`, `msds-essentiel-msds-js-2027`, `msds-essentiel-msds-js-2026`. Sections et packs déjà propres.
- `pilote/cas/` : 40+ dossiers réels anonymisés à la main ; `pilote/README.md` exige une relecture humaine avant diffusion. `pilote/cas/S1` contient des numéros du mova (officiels, OK).
- Autres dossiers à statuer pour le public : `ancien skills/` (anciens prompts), `docs/propositions/`, `build/` (ignoré), `documents/` (vide, ignoré ?), `idées.md`, `GOALS.md`.
- `pyproject.toml` : `name = "skills-scoutisme"`, `version = "0.1.0"` alors que le tag courant est `v0.1.1`.
- `scripts/build.py` écrit `date.today()` dans `MANIFEST.md` : **build non déterministe**, incompatible avec un `skills/` commité vérifié par la CI.
- `scripts/inventory.py` recalcule le sha256 de l'original : échouera en CI sans les originaux.
- Descriptions des `SKILL.md` : ~700 et ~820 caractères. L'aide claude.ai annonce 200 caractères max pour `description`, alors que les zips ont déjà été chargés avec succès en test : **à vérifier**, ne pas raccourcir à l'aveugle.
- Le build de `scouts-ressources` lit `sources/<id>/index.md` et les sections, jamais `original/` ni `raw.md` : il tourne sans les originaux.

## 3. Tâches

### 3.1 Assainissement et nouveau dépôt (bloquant, en premier)
1. Ajouter `redactions` à `js-manuel-sport-de-camp-trekking` ; étendre le caviardage à `raw.md` (script rejouable, pas d'édition à la main ; amender la règle METHODE « raw jamais édité »). Vérifier par `rg -i "mot de passe|utilisateur\s*:"` sur tout le dépôt, et chercher d'autres secrets (IBAN, e-mails privés, téléphones hors numéros officiels).
2. `.gitignore` : `sources/*/original/`, `pilote/cas/`, `documents/`.
3. `check` / `inventory` : sha256 de l'original vérifié **seulement si l'original est présent** (local) ; en CI, vérifier le reste. Tests à adapter.
4. Relire `docs/terrain/` : retirer noms de groupes, lieux, années identifiantes ; statuer sur sa place (cf. Q-ouverte 1).
5. Statuer sur `ancien skills/`, `docs/propositions/`, `idées.md`, `GOALS.md` (Q-ouverte 2).
6. Créer le nouveau dépôt local : copie de l'arbre assaini, premier commit `chore: dépôt public initial`, puis tag `v0.1.1` sur ce commit pour amorcer release-please. Vérifier avec `git count-objects -vH` et un `rg` final qu'aucun original ni secret n'est passé. **Ne pas créer le repo GitHub, ne pas pousser.**

### 3.2 Build et `skills/` commité
1. Déplacer les sources des skills vers `skills-src/` ; `build` écrit dans `skills/<nom>/` (plus `build/claude-code/` pour les dossiers ; zips dans `build/` ou `dist/`, ignoré). Mettre à jour `justfile`, METHODE, `docs/skills-design.md`, tests.
2. Build **déterministe** : retirer la date du MANIFEST (ou la remplacer par la version du `pyproject`), tri stable, zips reproductibles (dates de fichier fixes dans le zip).
3. Version dans les packs : `metadata.version` dans le frontmatter des `SKILL.md` ou ligne du MANIFEST, mise à jour par release-please (`extra-files` + `x-release-please-version`), à trancher (Q-ouverte 3).
4. `just build-skills` (ou équivalent) = les deux packs + zips ; contrôle `git diff --exit-code skills/` en CI.
5. Vérifier que `npx skills add ./` sur le nouveau dépôt découvre bien `skills/scouts` et `skills/scouts-ressources` (le dépôt `vercel-labs/agent-skills` utilise la même disposition) et que `npx skills add <url du zip>` de `scouts-ressources` passe avec `SKILLS_EXTRACT_MAX_FILES=2000` (**à tester** : limite par défaut 1 000 fichiers par archive).

### 3.3 GitHub Actions
Versions vérifiées le 2026-10-19 : `actions/checkout@v7`, `astral-sh/setup-uv@v10.3.0` (**pas de tag flottant `@v10`**), `actions/upload-artifact@v7`, `googleapis/release-please-action@v5` (v5.0.0, épinglée par SHA chez le mainteneur), `actions/upload-pages-artifact@v5`, `actions/deploy-pages@v5`, `actions/configure-pages@v6`. Épingler par SHA comme le mainteneur.

1. **`ci.yml`** (push `main` + PR) : setup-uv (`python-version: "3.14"`, cache), `uv run pytest`, `uv run inventory --check`, `uv run light check`, build des deux packs, `git diff --exit-code skills/`, upload des zips en artefacts (`retention-days: 7`). Checkout par défaut (`fetch-depth: 1`) : les originaux n'étant plus versionnés, pas besoin de sparse-checkout.
2. **`release-please.yml`** (push `main`) : modèle du mainteneur. Avec un PAT (`token: secrets.…`), le tag poussé par release-please **déclenche** d'autres workflows (avec `GITHUB_TOKEN`, non : doc GitHub). Deux options valides : job `upload` dans le même workflow conditionné par `release_created`, ou `release.yml` séparé `on: push: tags: v*`. Recommandé : même workflow (un seul endroit, pas de dépendance au PAT pour l'upload). Le job build au tag, puis `gh release upload "$TAG" scouts.zip scouts-ressources.zip --clobber`. **Noms de zip sans version** (lien `latest` stable).
3. **`pages.yml`** (push `main` sur `site/**`, `workflow_dispatch`) : génération, `upload-pages-artifact`, `deploy-pages`, permissions `pages: write`, `id-token: write`, `concurrency: pages`. Réglage repo : Pages > Source = GitHub Actions (à faire par le mainteneur après le push).
4. **`veille.yml`** (cron mensuel + `workflow_dispatch`) : script `scripts/check_urls.py` (Phase 5 de la ROADMAP) : HEAD/GET poli (1 req/s) sur `url` / `file_url`, compare ETag / Last-Modified / taille / sha256 au registre, liste changés, morts (4xx/5xx), redirigés ; crée ou met à jour **une** issue (label `veille`) via `gh issue`. Permission `issues: write`. Pas de modification du dépôt.
5. Réglages repo à documenter pour le mainteneur (pas faisables en local) : secret PAT release-please, « Allow GitHub Actions to create and approve pull requests », Pages, labels.

### 3.4 release-please
- `release-please-config.json` : le modèle du mainteneur, avec ces écarts proposés :
  - `"release-type": "python"` (met à jour `pyproject.toml` ; `simple` ne le fait pas) + `"package-name": "scouts-skills"` ; **`uv.lock` n'est pas mis à jour** : prévoir `uv lock` dans la PR de release ou ne pas utiliser `--locked` en CI.
  - `"prerelease": false` (D8).
  - `"bump-patch-for-minor-pre-major": false` pour que `feat` donne une mineure (0.2.0) ; avec `true` (modèle actuel), un `feat` ne donne qu'un patch avant 1.0 (Q-ouverte 4).
  - Sections du changelog en français (titres libres) : Fonctionnalités, Corrections, Contenu ?, Documentation…, `style` caché. Les scopes (`feat(skills):`) apparaissent en gras.
  - `extra-files` : fichiers portant la version (README, `skills-src/*/SKILL.md` si version dans le frontmatter, pages du site qui affichent la version).
- `.release-please-manifest.json` : `{".": "0.1.1"}` ; `bootstrap-sha` = commit initial du nouveau dépôt (puis retirable).
- Convention de commit à documenter dans CONTRIBUTING (déjà pratiquée : `feat(skills):`, `fix(referentiels):`, `docs:`). Proposer un type ou scope pour les changements de contenu qui doivent produire une release (ex. `fix(contenu):`), sinon un changement de savoir en `docs:` ne déclenche aucune version.

### 3.5 Site GitHub Pages
Sobre : **sans logo, sans couleurs**, HTML sémantique, CSS minimal (largeur de lecture, police système) ou aucun. Générateur recommandé : **script Python `scripts/site.py`** (`markdown` ou `markdown-it-py`, via `uv`) qui convertit `site/*.md` en HTML avec un gabarit unique et un menu. Écartés : MkDocs (thème imposé), Jekyll (toolchain Ruby), Zensical (pré-1.0, thémé). Tout en français.

Pages :
1. **Accueil** : ce que sont ces skills, pour qui (responsables, formateur·ices, coachs, experts J+S), différence `scouts` / `scouts-ressources`, limites (pas un document officiel, toujours vérifier, jeu 2027 par défaut), liens.
2. **Installer avec un agent** (Claude Code, Codex, Pi, autres via `npx skills`) :
   - Universel : `npx skills add fuzoh/scouts-skills --skill scouts -g` (`-a claude-code|codex|pi`), `npx skills use …` sans installer.
   - Claude Code : `npx skills` ou copie dans `~/.claude/skills/` ; option marketplace de plugins (`.claude-plugin/marketplace.json`, `/plugin marketplace add fuzoh/scouts-skills`, sources `./skills/scouts` et `./skills/scouts-ressources`) (Q-ouverte 5). Skills préfixés `/plugin:skill` dans ce cas.
   - Codex : `~/.agents/skills/` (utilisateur) ou `.agents/skills/` (projet) ; `~/.codex/skills` non documenté, ne pas l'écrire.
   - Pi : `pi install git:github.com/fuzoh/scouts-skills` (installe tout le dépôt, **à tester** : découverte des deux skills sans bruit des autres dossiers) ou `~/.agents/skills/`.
   - Mise à jour (`npx skills update`, `pi update`, nouveau zip).
3. **Installer sur une plateforme web** :
   - claude.ai : Customize > Skills > + > Upload a skill (zip), code execution et création de fichiers activés ; plans Free à Enterprise ; Team/Enterprise : activation par un owner. `scouts` testé ; `scouts-ressources` (1 700 fichiers) **à tester**.
   - ChatGPT : Skills > Create > Upload ; plans et limites non confirmés (API : 500 fichiers / 50 Mo par skill) ⇒ `scouts` probable, `scouts-ressources` probablement non. **À tester.**
   - Gemini : pas de skills ; Gem avec fichiers ou zip en conversation (10 fichiers / 100 Mo). Reprendre ce qui a marché lors des tests du mainteneur sur Gemini. Variante aplatie (quelques gros fichiers) = tâche ROADMAP « packs aplatis » existante.
   - Mistral Le Chat, Copilot : pas de skills, bibliothèque de documents seulement ; mentionner ou omettre (Q-ouverte 6).
4. **Utiliser le skill** (plusieurs pages, contenu tiré de `references/guide.md`, `pilote/tests-manuels.md`, `docs/skills-design.md`) : poser une question de règle ou de délai ; corriger une activité J+S, une UA, un programme de camp, un concept de sécurité ; concevoir un document ; débuter (guider) ; quand prendre `scouts-ressources` (citations exactes). Exemples de prompts concrets, sans données réelles.
5. **Sources et auteurs** : générée depuis le registre (`sources/*/source.yaml`, sources `indexed`/`verified` embarquées) : titre, émetteur (MSdS, OFSPO/J+S, BPA, cudesch, autres), édition/version, lien `url`/`file_url`, mention de caviardage le cas échéant, mention des droits. Génération par script, pas à la main.
6. **Signaler une erreur, suggérer une modification, commenter** : pour non-techniciens. Création d'un compte GitHub, lien direct vers chaque formulaire d'issue, ce qu'il faut joindre (prompt, réponse, version du skill, plateforme), commentaire sur une issue existante.
7. **Contribuer** : pour qui veut aller plus loin : structure du dépôt, pipeline (renvoi à METHODE), modifier un savoir ou un référentiel, ajouter une source (originaux hors git), conventional commits, PR, `just check` / tests, build. Peut reprendre `CONTRIBUTING.md`.

### 3.6 Fichiers du dépôt public
- `README.md` (court : quoi, installer, lien site, licences), `LICENSE` (MIT), `LICENSE-CONTENT` ou section dédiée (CC BY-SA 4.0), `CONTRIBUTING.md`, `CHANGELOG.md` (créé par release-please).
- `.github/ISSUE_TEMPLATE/` (formulaires YAML) : erreur de contenu (règle fausse, chiffre, délai), suggestion d'amélioration, problème d'installation ; `config.yml` avec lien vers le site ; `pull_request_template.md`.
- Labels : `contenu`, `installation`, `suggestion`, `veille`.
- `AGENTS.md` du dépôt public : adapter (plus de `documents/` comme boîte d'entrée publique ? originaux hors git).
- `pyproject.toml` : `name = "scouts-skills"`, version `0.1.1`, `license`, `readme`.

### 3.7 Check de publication (à refaire sur le nouveau dépôt, avant push)
- [ ] Aucun fichier sous `original/`, aucun `pilote/cas/`, aucun binaire inattendu (`git ls-files | rg -v '\.(md|yaml|yml|py|toml|json|lock)$'`).
- [ ] Aucun identifiant, mot de passe, IBAN, e-mail ou téléphone privé (`rg` ciblés ; numéros officiels tolérés).
- [ ] `docs/terrain/` relu, mainteneur OK.
- [ ] `uv sync`, `uv run pytest`, `inventory --check`, `light check`, build des deux packs, `git diff --exit-code skills/` : verts sans les originaux.
- [ ] Taille du dépôt raisonnable (`git count-objects -vH`).
- [ ] README, LICENSE, CONTRIBUTING, templates d'issue, workflows présents ; `actionlint` sur `.github/workflows/`.
- [ ] Site généré en local et relu (liens internes, commandes d'install avec `fuzoh/scouts-skills`).
- [ ] Liens absolus vers l'ancien chemin ou des fichiers retirés (`pilote/cas`, `original/`) corrigés dans docs, skills et référentiels.
- [ ] Liste des actions manuelles post-push pour le mainteneur (secret PAT, Pages, réglage PR, labels, création de la release `v0.1.1` si voulue).

## 4. Questions ouvertes (à trancher avec le mainteneur pendant la conception)
1. `docs/terrain/` : utile aux skills tel quel, ou à remplacer par une extraction plus abstraite (patrons, erreurs fréquentes, sans aucun cas) ? Sinon le garder hors du dépôt public.
2. `ancien skills/`, `docs/propositions/`, `idées.md`, `GOALS.md`, `pilote/retours-en-vrac.md` (retours d'amis) : publics ou locaux ?
3. Où porter la version visible par l'utilisateur : frontmatter `metadata.version` du `SKILL.md`, MANIFEST, ou les deux ?
4. `bump-patch-for-minor-pre-major` : garder `true` (modèle du mainteneur, `feat` → patch) ou `false` (`feat` → mineure) ?
5. Ajouter une marketplace de plugins Claude Code en plus de `npx skills` ? (Coût : un `marketplace.json` ; préfixe `scouts:` dans les noms de skill.)
6. Page web : documenter Mistral / Copilot (pas de skills) ou se limiter à claude.ai, ChatGPT, Gemini ?
7. Sources web vs PDF (D2) : convertir en priorité vers la variante web quand le PDF est en ligne. Chantier séparé, après publication ?

## 5. Sources (consultées le 2026-10-19)
- Claude Code skills : https://code.claude.com/docs/en/skills ; plugins/marketplace : https://code.claude.com/docs/en/plugin-marketplaces, https://code.claude.com/docs/en/plugins/marketplace-reference
- Codex skills : https://learn.chatgpt.com/docs/build-skills
- Pi : https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md, `…/docs/packages.md`
- `npx skills` : https://github.com/vercel-labs/skills (limites d'archive : 10 MiB / 25 MiB / 1 000 fichiers, surchargeables)
- claude.ai : https://support.claude.com/en/articles/12512180-use-skills-in-claude, https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- ChatGPT : https://help.openai.com/en/articles/20001066-skills-in-chatgpt (403 en direct, seconde main) ; API : https://developers.openai.com/cookbook/examples/skills_in_api
- Gemini : https://support.google.com/gemini/answer/14903178, https://support.google.com/gemini/answer/15146780
- release-please : https://github.com/googleapis/release-please-action, https://github.com/googleapis/release-please/blob/main/docs/manifest-releaser.md, https://github.com/googleapis/release-please/blob/main/docs/customizing.md
- GITHUB_TOKEN ne déclenche pas de workflows : https://docs.github.com/en/actions/concepts/security/github_token
- Pages : https://docs.github.com/en/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site
- setup-uv : https://github.com/astral-sh/setup-uv ; checkout : https://github.com/actions/checkout

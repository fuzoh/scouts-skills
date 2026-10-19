# Méthode de travail

Ce dépôt est la **fabrique** des skills scoutisme suisse : il collecte les ressources officielles, les convertit en markdown exploitable, les indexe, puis construit des skills distribuables. Ce fichier décrit la méthode. L'état du travail vit dans les fichiers listés en fin de document, jamais dans la tête d'une session.

## Principes

1. **Une source = un identifiant stable.** Le document officiel change de version, l'identifiant ne change pas. Les skills citent l'identifiant, le registre dit quelle version est courante.
2. **Le registre est la vérité.** Chaque source a un `source.yaml` ; tout ce qui est dérivé (inventaire, index de concepts, listes dans les skills) est régénéré, jamais édité à la main.
3. **Scripts pour l'extraction, agent pour le sens.** Conversion PDF/web → md, hashes, inventaire, vérification d'URL : scripts `uv` reproductibles. Découpage sémantique, résumés, concepts, glossaire : agent, validé par un humain.
4. **Progressive disclosure partout.** Un skill charge un index court, puis seulement la section nécessaire. Aucun fichier chargé d'entrée de jeu ne dépasse ~200 lignes.
5. **Citation obligatoire.** Toute section convertie porte sa source, sa version et ses pages d'origine. Un skill qui affirme quelque chose doit pouvoir pointer `id@version p.X`.
6. **Une seule source de vérité par format.** `SKILL.md` (spec agentskills.io) est le format maître ; les packs pour apps web (Claude Project, GPT, Gemini) sont construits depuis les skills, jamais maintenus à part.
7. **Français uniquement.** Une source DE n'est retenue que si aucun équivalent FR n'existe ; elle est alors marquée `lang: de` et traduite dans les sections converties.

## Pipeline d'une source

Chaque source passe par ces états, enregistrés dans `status:` du `source.yaml`. Un état n'est atteint que si son critère est rempli.

| Statut | Critère de sortie |
|---|---|
| `collected` | Fichier original dans `sources/<id>/original/` (local, jamais versionné), `source.yaml` créé avec `url`, `sha256`, `retrieved`. |
| `triaged` | Humain a validé : `id`, `title`, `issuer`, `audience`, `themes`, et décidé `keep` ou `rejected`. Les doublons sont supprimés ici. |
| `converted` | `raw.md` écrit par `convert` (texte complet, marqueurs de page physiques `<!-- p.N -->`, ancres web `<!-- #ancre -->`). Sources web : un `raw/<slug>.md` par page. |
| `indexed` | `index.md` validé (arbre des sections : chapitre, pages, résumé d'une ligne, fichier) ; `split` a découpé `raw.md` en `NN-<slug>.md` ; `concepts:` rempli dans le yaml. Si `extraction: catalogue`, seul `index.md` existe et l'état `converted` est sauté. |
| `verified` | Un humain a relu l'index et les tableaux, cases et prescriptions contre l'original ; `fidelity` renseigné. |
| `superseded` | Une version plus récente est `collected` sous le même `id` ; l'ancienne reste dans `history:`. |
| `rejected` | Hors périmètre ou doublon. Le yaml reste (trace), l'original est supprimé. |

Toute transition est un commit distinct ou groupé par lot homogène (`feat(sources): triage lot cofor`). `just check` exige les artefacts du statut : `converted` → `raw.md` ou `raw/` ; `indexed` → en plus `index.md` à la version du registre et chaque section qu'il liste, à la même version, sans `NN-*.md` orphelin (catalogue : `index.md` seul) ; `verified` → en plus `fidelity`. Il recalcule aussi le sha256 de l'original quand `original/` est présent (web : concaténation des `original/<slug>.html` dans l'ordre de `web_pages`) ; sans `original/` (clone public, CI), le hash n'est pas recalculé et `check` le signale.

## Arborescence

```
sources/<id>/
  source.yaml          registre : métadonnées, statut, versions, concepts
  original/<fichier>   fichier officiel tel que téléchargé (une seule version courante) ; git-ignoré, copie locale du mainteneur
  raw.md               texte complet converti puis caviardé par script, jamais édité à la main (web : raw/<slug>.md par page)
  index.md             arbre des sections : chapitre, pages, résumé, fichier ; pilote le découpage
  recovered/<nom>.md   tableau récupéré par script (grille à icônes), frontmatter {source, pages, title, method[, version]}
  NN-<slug>.md         une section par fichier, frontmatter {source, version, title, chapter, pages | url, sha256[, fidelity, fidelity_notes]}
referentiels/<slug>.md un référentiel par livrable (non-négociables cités id#NN-slug, critères de qualité, [non officiel], pièges, trame) ; brouillons tant que `check` ne les valide pas
skills-src/<nom>/      sources d'écriture d'un skill au format agentskills.io, format maître : `scouts` (sans corpus, savoirs) et `scouts-ressources` (le pack ajoute referentiels/ et corpus/)
  SKILL.md
  references/          méthode par verbe (corriger, concevoir, chercher, guide), reglages.md, documents.md
skills/<nom>/          packs générés par `just skills` et commités (installables par `npx skills add`) ; jamais édités à la main, la CI refuse un écart avec le build
pilote/                grille de tests manuels ; jeu d'essai sur dossiers réels anonymisés dans pilote/cas/<code>/, local, jamais versionné ; jamais une source
scripts/               package uv (CLI typer) : ingest, discover, convert, index, split, recover, inventory, concepts, referentiels, build
build/, dist/          sorties locales et zips des packs (git-ignorés ; zips publiés en assets de release)
docs/                  documentation longue du dépôt ; docs/lexique-terrain.md = vocabulaire déduit de dossiers réels, [non officiel], jamais une source (les notes de terrain restent hors dépôt)
documents/             INBOX locale, git-ignorée : fichiers bruts pas encore ingérés. Vide quand tout est traité. Dossiers réels (camps, UA) : analysés par scripts/terrain.py → build/terrain/, jamais ingérés ni versionnés
```

Granularité adaptative : un document court (< 15 pages) reste en un seul fichier `01-contenu.md` avec un `index.md` à une entrée. Un manuel est découpé par chapitre, puis par sous-section si un chapitre dépasse ~300 lignes.

### Commandes

Toutes via `just` (qui appelle `uv run <commande>`). `just` seul liste les recettes.

| Commande | Effet | Statut posé |
|---|---|---|
| `just ingest <fichier> --id <id> [--title --ref --version --published --audience --themes --type]` | sha256, pages, déplace l'original dans `sources/<id>/original/`, crée `source.yaml` | `collected` |
| `just ingest --batch documents/lot.yaml` | lot `[{file, id, title, issuer, ref, version, published, audience, themes}]`, tout validé avant d'écrire, `lot.yaml` supprimé ensuite | `collected` |
| `just ingest --batch manifeste.yaml` | manifeste de `discover` : pages regroupées par colonne `source` → sources web ; fichiers avec `id` → téléchargés puis traités en local | `collected` |
| `just ingest --url <url> --id <id>` | une page web, html dans `original/`, `version` = date du jour | `collected` |
| `just ingest --match manifeste.yaml` | remplit `url`/`file_url` des sources dont le sha256 est dans le manifeste ; même nom mais hash différent → `stale: true` | — |
| `just ingest <dossier> --id <id> --type image` | copie le dossier dans `original/`, `extraction: vision` | `collected` |
| `just ingest ... --new-version` | remplace l'original d'une source existante, ancienne version dans `history` ; supprime `raw.md`, `raw/`, `index.md`, `NN-*.md`, `recovered/` (liste affichée, récupérables par git), vide `fidelity`, signale `applies_*`, `nature`, `redactions` à revoir | `collected` |
| `just convert <id> [--render]` | `raw.md` (web : `raw/<slug>.md`) ; refuse `extraction: catalogue \| none` ; `--render` ne touche pas `original/`, page rendue dans `build/render/<id>/` | `converted` |
| `just index <id> [--force] [--pageindex]` | squelette `index.md`, jamais écrasé sans `--force` ; `--pageindex` = arbre PageIndex Flash pour un PDF sans signets (`just install-pageindex`) | — |
| `just recover <id>` / `--all` | reconstitue dans `recovered/` les grilles perdues à la conversion (icônes de niveau, tableaux à colonnes alignées) selon une recette par source dans `scripts/recover.py` ; rejouable, à lancer avant `split` | — |
| `just redact <id>` / `--all` | applique `redactions` du yaml au texte brut (`raw.md`, `raw/`), rejouable ; `convert` le fait déjà | — |
| `just split <id>` | `NN-<slug>.md` depuis `index.md`, rejouable ; fusionne `recovered/`, applique `redactions`, propage `fidelity: partial` | — |
| `just discover <url> --depth N [--render] [--out manifeste.yaml]` | manifeste yaml, ne crée rien dans `sources/` | — |
| `just check-urls [--only <id>] [--limit N] [--format md\|json] [--out veille.md]` | compare le registre aux URL publiées : changées (sha256), mortes, redirigées ; rapport md ou json ; ne modifie rien | — |
| `just inventory` / `just check` | valide tous les yaml, les artefacts du statut et le sha256 des originaux présents, puis écrit `INVENTORY.md` / valide seulement | — |
| `just referentiels check` / `--citing <id>` | valide `referentiels/*.md` (frontmatter, citations `id#NN-slug` existantes et listées dans `index.md`, N cités, `sources` = ids cités, `inclut` sans cycle, `canevas` = sources `nature: exemple`, ordre des sections, taille) ; inclus dans `just check` / `--citing` : référentiels qui citent une source | — |
| `just build claude-code [--skill scouts\|scouts-ressources] [--scope complet\|referentiels] [--zip] [--out dir] [--dist dir]` | `scouts` (défaut) : copie de `skills-src/scouts/` après `light check`, dans `skills/scouts/` ; `scouts-ressources` : `SKILL.md`, `references/` (+ `glossaire.md`, `concepts/`), `referentiels/`, `corpus/<id>/` (`index.md` enrichi des métadonnées du registre + sections), refuse un référentiel invalide ou une citation absente du pack ; jamais `raw.md`, `original/`, `recovered/`, `source.yaml`. Les deux : `license` et `metadata.version` (du `pyproject.toml`) injectés dans le frontmatter, MANIFEST sans date, zips reproductibles dans `dist/` | — |
| `just skills` (alias `just zips`) | `light index` puis `build all --zip` : `skills/scouts/`, `skills/scouts-ressources/`, `dist/scouts.zip`, `dist/scouts-ressources.zip`. À lancer et commiter après toute modification de `skills-src/`, `referentiels/`, des sections ou du glossaire | — |
| `just install` / `just install-ressources` | build puis lien `~/.claude/skills/scouts` (resp. `scouts-ressources`) vers `skills/<nom>/` (refuse un dossier étranger) | — |
| `just concepts` | génère `docs/concepts/<slug>.md` (index inversé des `concepts:`, définition reprise de la colonne `slug` de `GLOSSARY.md`) et `docs/concepts/README.md` | — |
| `just test` | pytest | — |

Refus d'`ingest` (rien n'est déplacé) : sha256 déjà connu, id non conforme, id existant sans `--new-version`. `indexed` et `verified` sont posés à la main.

### Flux de conversion

1. `convert <id>` → `raw.md`. Rejouable, écrase seulement `raw.md`. PDF : pymupdf4llm page par page ; une page qui rend moins de 85 % des mots du PDF (graphismes vectoriels qui masquent le texte) est reprise sans graphismes ni images, au prix des tableaux de cette page.
2. `index <id>` → squelette `index.md` depuis les signets du PDF, l'arbre PageIndex (`--pageindex`, recommandé pour un manuel sans signets) ou les titres détectés par police (`toc_source: bookmarks | pageindex | headings | agent`), avec `page_offset` si la pagination imprimée diffère de la page physique. Quand les titres portent un numéro (`2.1 …`), le niveau vient du numéro, plus fiable que la police. Le titre de couverture et la table des matières restent souvent dans le squelette : l'agent les retire.
3. Agent et humain corrigent `index.md` : titres, plages, numéros de chapitre, résumés. Résumés en lot par `claude -p` pour les manuels, par l'agent en session pour les documents courts.
4. `split <id>` → `NN-<slug>.md` selon les plages d'`index.md`. Rejouable ; `index.md` est la seule vérité du découpage. Refuse un `index.md` dont la `version` diffère de `source.yaml` (index d'une autre version : `index --force`), et n'écrit rien en cas de refus. Un nœud reçoit ses pages moins celles de ses descendants : le chapitre garde son introduction, les sous-sections leurs pages. `split` refuse deux frères qui se chevauchent, un enfant qui sort de son parent, une plage au-delà de `pages`, un même fichier visé deux fois. Les sections changent souvent en milieu de page : arrondir à la page et regrouper deux sections qui partagent une page dans un nœud (« §2.2.7 … ; 2.2.8 … »). Un parent dont toutes les pages sont dans ses enfants reçoit un fichier sans texte (avertissement) : lui donner un résumé de renvoi. Sans plage (xlsx), une entrée reçoit le bloc `# <titre>` de `raw.md` (une feuille), sinon tout `raw.md`.
5. Tableaux récupérés : chaque `recovered/<nom>.md` (écrit par `scripts/recover.py`) est ajouté sous `### Tableau récupéré : <title>` à la fin de la section la plus profonde dont la plage couvre ses `pages` (la première à égalité) ; aucune → avertissement, tableau non fusionné. Ne jamais coller un tableau à la main dans une section : `split` l'effacerait.

Format d'`index.md` : frontmatter `{source, version, pages, page_offset, toc_source}` puis une ligne par nœud, indentée de deux espaces par niveau :

```
- §3 Le retour p.12-24 → 03-le-retour.md : principes du feedback en cours
  - §3.2 Qualifier p.18-24 → 04-qualifier.md : critères et déroulement
```

`page_offset` = page physique − page imprimée (0 si inconnu). Sans pagination (docx, xlsx) la plage est omise : `- Titre → 01-contenu.md : résumé`. Web : `- Titre <url> → NN-slug.md : résumé`.

### Fidélité, applicabilité, caviardage

- `fidelity: complete | partial` (vide = `complete` non évalué, obligatoire à `verified`). `partial` exige un motif dans `fidelity_notes` (« cases de niveau perdues p.2-4 ») ; `split` recopie les deux champs dans le frontmatter de chaque section, le build les transmet aux packs.
- `applies_from`, `applies_until` (AAAA-MM-JJ), `nature: prescription | recommandation | exemple` : sources prescriptives seulement (règlements, directives, modèles de formation), vides ailleurs. Un skill qui évalue un cours choisit la référence selon la date.
- Caviardage (identifiants en clair) : une règle du yaml, jamais une édition à la main, `redactions: [{section: NN-slug, pattern: regex, replace: "[identifiants retirés]"}]`. `convert` l'applique au texte brut (`raw.md`, `raw/`) avant de rendre la main, `redact <id>` la rejoue sans reconvertir, `split` l'applique à la section visée. Rejouable : une règle qui ne trouve ni son motif ni son `replace` fait refuser `convert` (texte brut supprimé), `redact` et `split` ; `check` refuse un texte brut ou une section qui contient encore le motif. `replace` non vide. Le motif ne doit pas recopier le secret (viser le libellé : `Nom d.utilisateur\s*:\s*\S+…`). Le même texte est retiré à la main de `notes`.

### Citation

- PDF : `id@version §3.2 p.14`. `p.N` est la page physique (1..n) ; `§` est le numéro imprimé, extrait du titre ou posé par l'agent.
- pptx : `p.N` = numéro de diapo. docx, xlsx : pas de page, citation par section (`id@version §titre`) ; xlsx = une section par feuille.
- Web : `id <url>#ancre`. Les ancres HTML des titres sont conservées dans le md sous forme `<!-- #ancre -->`. Sans ancre (SPA à slugs aléatoires), `url` + titre en clair. `version` = date `retrieved` ; `sha256` par page dans le frontmatter.

### Sources web

Pas de crawler qui crée des sources. `discover <url> --depth N [--render]` parcourt le même hôte (robots.txt respecté, 1 requête/s, `--render` = playwright pour les SPA, `just install-web`) et écrit un manifeste yaml : `pages: [{url, title, source}]` et `files: [{url, name, size, sha256, found_on, id}]`. L'humain regroupe les pages en sources en remplissant la colonne `source` avec un id (un manuel en ligne = une source, sections = pages ; une page peut devenir un document à part) et pose un `id` sur les fichiers à ingérer, puis `ingest --batch manifeste.yaml`. Les fichiers téléchargés suivent le même chemin que les fichiers locaux (`url` = `found_on`, `file_url` = url du fichier). Une source web garde la liste de ses pages dans `web_pages: [{url, title, slug}]` du yaml ; chaque page est enregistrée en `original/<slug>.html`, jamais réécrite ensuite (collecte et conversion séparées : `convert --render` garde la page rendue dans `build/render/<id>/<slug>.html`, git-ignoré, et ne convertit que vers `raw/`). `ingest --match manifeste.yaml` remplit `url` et `file_url` des sources locales dont le sha256 correspond. Le rendu (`--render`) se fait en locale `fr-CH`. Un lien qui redirige vers un fichier (page de détail d'un catalogue) donne `url` = fichier final et `found_on` = la page de détail. Pour un catalogue paginé côté serveur (espace Downloads de pfadi.swiss), `scripts/catalogue_pfadi.py` écrit `build/pfadi-catalogue.yaml` (entrées, fichiers hachés seulement s'ils correspondent à un original local sans `file_url`). Une SPA à routes en fragment (`#!/article/NN`) ne se crawle pas : manifeste écrit à la main, slug de page dérivé du fragment.

### Extraction

`extraction:` dans le yaml, posé au triage : `text` (défaut), `vision` (texte insuffisant : scanné, schémas, PNG ; traitement différé, pas d'OCR pour l'instant), `catalogue` (seulement un `index.md` listant les pages avec une ligne chacune, pour suggérer une ressource sans l'embarquer), `none`.

## Identifiants

Forme : `<issuer>-<slug>`, minuscules, tirets, sans accents, ≤ 40 caractères.

| issuer | Émetteur |
|---|---|
| `msds` | Mouvement Scout de Suisse (brochures, profil, modèle de formation) |
| `cofor` | Commission formation MSdS (checklists, approfondissements, dossiers de cours) |
| `js` | Jeunesse+Sport / OFSPO (manuels, bases, modules) |
| `cudesch` | Collection cudesch |
| `autre` | Tout le reste, précisé dans `issuer_detail` |

Exemples : `cofor-checklist-cours-base`, `js-manuel-sport-de-camp`, `msds-profil-scoutisme`. Le numéro officiel (ex. `314201fr`) va dans `ref:`, pas dans l'id.

## Tri : pas de hiérarchie de dossiers

Un document sert souvent plusieurs publics et plusieurs thèmes. Les sources sont donc à plat dans `sources/`, et le classement est porté par trois champs du yaml, tous multi-valués :

- `audience` : `responsable`, `formateur`, `expert-js`, `coach-js`, `cadre-cantonal`
- `themes` : vocabulaire contrôlé dans `docs/taxonomie.md` (formation, programme, sécurité, camp, administration, prévention, inclusion, sport…)
- `concepts` : termes du glossaire touchés par la source (UA, AC, SC, feedback…)

Les vues par public ou par thème sont générées dans `INVENTORY.md`.

## Glossaire et index de concepts : séparés

- `GLOSSARY.md` : court, chargé par tous les skills. Terme, sigle, définition en une ligne, source canonique. Cible : < 150 lignes.
- `docs/concepts/<concept>.md` : un fichier par concept, généré par `just concepts` depuis les `concepts:` des yaml. Définition (colonne `slug` du glossaire), sources qui portent le concept (`id@version`, nombre de sections, lien vers leur `index.md`), concepts liés par co-occurrence. C'est l'index inversé et le graphe de navigation ; chargé à la demande seulement. Les concepts sont posés au niveau de la source, pas de la section : l'`index.md` de la source fait le dernier pas.

Le glossaire pointe vers `docs/concepts/` quand un terme y a une fiche. Le glossaire ne contient jamais la liste des sources d'un concept : c'est le rôle de la fiche.

## Versions et mise à jour

- Une mise à jour officielle = `ingest --new-version` : nouveau fichier dans `original/`, ancien supprimé, entrée ajoutée dans `history:` du yaml, `raw`, `index.md`, sections et `recovered/` de l'ancienne version supprimés, `status: collected` ; puis reconversion, index, découpage.
- Veille : `just check-urls [--only <id>] [--limit N] [--format md|json] [--out fichier]` (`scripts/check_urls.py`) vérifie poliment (robots.txt, 1 requête/s par hôte, user-agent `scouts-skills-veille`) chaque `file_url`, `url` et `web_pages[].url` des sources ni `rejected` ni `superseded`. Classement : `change` (sha256 du fichier distant ≠ `sha256` du registre ; fichier trop gros : `Last-Modified` postérieur à `retrieved`), `redirige` (URL finale différente, sauf vers une autre URL de la même source), `mort` (4xx/5xx, erreur réseau après 2 essais), `ok`. Les pages web ne sont pas comparées au sha256 (html instable) : seulement mortes ou redirigées. Le script ne modifie jamais le registre ni aucun fichier versionné, et sort en 0 même avec des changements.
- Le workflow mensuel `.github/workflows/veille.yml` (cron le 1er du mois, `workflow_dispatch` possible) lance `check-urls` puis ouvre ou met à jour **une** issue au label `veille` (corps = rapport, commentaire de synthèse) ; jamais de PR ni de fermeture automatique. `stale: true` reste posé à la main par l'humain, après lecture de l'issue et ré-ingestion locale (`ingest --new-version`) : les originaux ne sont pas dans le dépôt public.
- Les skills référencent `id` sans version : à la construction, le build injecte la version courante dans les citations.

## Skills

Deux skills, même méthode (`DECISIONS.md` ; spécification dans `docs/skills-design.md`) :
- **`scouts`** (`skills-src/scouts/`), le skill principal : sans corpus, règles et savoirs encodés en fichiers courts, provenance en clair ; décrit plus bas.
- **`scouts-ressources`** (`skills-src/scouts-ressources/`) : même méthode avec le corpus embarqué et les citations `id#NN-slug` ; pour qui veut le texte officiel.
- Quatre verbes (chercher, expliquer, corriger, concevoir ; `scouts` ajoute guider), sans point d'entrée par public : le livrable nommé ou joint commande le routage.
- **Référentiels** `referentiels/<slug>.md` : un par livrable, non-négociables cités par `id#section`, critères de qualité, critères `[non officiel]`, validés par `check` ; format, cycle de vie (`brouillon` → `relu` → `valide`) et règles de `check` dans `docs/skills-design.md` § 2, 6, 7. Le mot « canevas » désigne les modèles vierges ingérés (sources `nature: exemple`), formats reconnus et jamais exigés ; la trame de conception du référentiel est la structure de sortie de *concevoir*.
- **Réglages** `skills-src/<nom>/references/reglages.md` : ce que le mainteneur change sans toucher à la méthode (niveau, longueurs, ton, posture, jeu de date par défaut, univocité, hors corpus, critères globaux). Priorité : conversation > réglages > `SKILL.md`.
- Un skill dédié n'apparaît qu'après échec de l'échelle référentiel → référentiel avec procédure → non-négociables dans `SKILL.md` → dédié.

- **Posture commune** (`DECISIONS.md`) : assistant qui discute, pas de ligne de plan ni de compte rendu de lecture, cadrage silencieux ; jeu de date 2027 par défaut (2026 seulement si le camp ou le cours est explicitement antérieur au 01.01.2027) ; une seule valeur par réponse (la plus prudente) ; pas de provenance entre parenthèses dans la prose ; jamais de mention du skill ; « Pour aller plus loin » en fin de réponse.
- **`SKILL.md` de `scouts-ressources`** (≤ 150 lignes) : quatre verbes, chargement en quatre pas (glossaire → référentiel entier → sections citées → réglages), catalogue des référentiels, cadrage silencieux, niveaux, citation, hors corpus, situations sans livrable. Squelettes par verbe dans `references/corriger.md`, `concevoir.md`, `chercher.md`.
- **Pack `scouts-ressources`** (`just build claude-code --skill scouts-ressources`, `just install-ressources`) : `scouts-ressources/{SKILL.md, references/, referentiels/, corpus/<id>/}` ; dans le pack, une citation `id#NN-slug` se lit dans `corpus/<id>/NN-slug.md` ; `corpus/<id>/index.md` porte le titre, `nature`, `applies_*`, `fidelity` de la source.

- **`scouts`** (`skills-src/scouts/`, `DECISIONS.md`) : même méthode sans corpus ni citation `id#section` ; référentiels en dossiers `referentiels/<slug>/NN-*.md` dérivés de `referentiels/<slug>.md` (`derive_de`), savoirs par thème dans `savoirs/` (index généré par `light index`), `references/guide.md` (parcours pour qui débute), `references/documents.md` (catalogue des documents officiels à recommander). Limites des applis web (100 fichiers dans le pack, 50 Mo, 25 Mo par fichier, pas de format bureautique binaire, `description` ≤ 1 024 car.) et budget de 5 000 tokens estimés par fichier (`docs/contraintes-plateformes.md`) : `just light-check` (dans `just check`), `just build claude-code --skill scouts --zip`, `just install`. Produit dérivé : reporter dans le dossier de `scouts` toute modification d'un référentiel de `referentiels/`.

Règle : un skill n'embarque jamais une copie d'une section de source. Il référence `sources/<id>/NN-slug.md` et le build copie ce qu'il faut dans le pack de distribution.

## Fichiers d'état

| Fichier | Rôle | Édité par |
|---|---|---|
| `sources/*/source.yaml` | statut et métadonnées de chaque source | script (création, hash, `collected` → `converted`) puis humain/agent (tri, concepts, `indexed`, `verified`) |
| `INVENTORY.md` | vue d'ensemble : comptage par statut, tables par public et thème | **généré** par `scripts/inventory` |
| `ROADMAP.md` | phases du projet, prochaine action, blocages | humain, en fin de session |
| `DECISIONS.md` | décisions structurantes en vigueur | réécrire la ligne quand la décision change |
| `GLOSSARY.md` | termes partagés | agent propose, humain valide |
| `docs/taxonomie.md` | vocabulaire contrôlé `themes` et `audience` | humain |

Fin de session type : mettre à jour `ROADMAP.md` (fait / prochaine action), régénérer `INVENTORY.md`, commit.

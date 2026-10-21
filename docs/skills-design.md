# Design des skills

Référence de conception issue du grill Phase 4 (`docs/briefing-phase4-grill.md` ; choix encore en vigueur dans `DECISIONS.md`). Ce document fait foi pour le format des référentiels, le contenu de `reglages.md` et les règles de `check`. METHODE § Skills en donne le résumé.

## 1. Organisation

- **Deux skills de même méthode** : `scouts` (principal, sans corpus, § 10) et `scouts-ressources` (corpus embarqué, citations). Verbes : chercher, expliquer, corriger, concevoir. `scouts` ajoute guider. Les deux ont personnaliser. Pas de point d'entrée par public : le livrable nommé ou joint commande le routage ; sans livrable, recherche dans le corpus ou les savoirs. Jusqu'au 2026-10-18 les skills s'appelaient `scout` et `scout-light`.
- **Référentiels** `referentiels/<slug>.md`, un par livrable, données de premier rang, lus par le skill : `activite-js`, `concept-de-securite`, `programme-camp`, `qualification`, `ua`.
- **Priorité** : conversation > `scouts-perso/` > `reglages.md` > `SKILL.md`. Une règle locale durcit ; elle n'assouplit pas un non-négociable ni une règle de sécurité.
- **Échelle de bascule** avant tout skill dédié : référentiel → référentiel avec procédure → non-négociables recopiés dans `SKILL.md` → skill dédié. Repli si le pilote échoue : découpage par livrable (proposition A), référentiels conservés.
- **Canevas** : le mot désigne les modèles vierges ingérés (`nature: exemple`), jamais les référentiels.
- **Packs** : zip agentskills.io avec corpus pour Claude Code, claude.ai, Gemini, ChatGPT. Pack aplati par domaine `camp` / `formation` pour Claude Project et custom GPT : seulement si un retour bêta le demande. Le build n'embarque jamais `raw.md` ni les originaux.

## 2. Format d'un référentiel

### 2.1 Frontmatter

```yaml
slug: activite-js                # = nom du fichier
titre: Activité J+S (…)
signaux: [mots ou rubriques qui trahissent ce livrable dans une demande]
role: [responsable, coach-js, formateur, expert-js]
verbes: [corriger, concevoir, expliquer]
parametres:
  - {nom: date du camp, obligatoire: true}
  - {nom: branche, obligatoire: false}
canevas: [ids de sources nature: exemple]   # formats reconnus en entrée, jamais exigés
sources: [ids]                   # = exactement l'ensemble des ids mentionnés dans le corps (`id#NN-slug` ou `id` seul entre accents graves)
inclut: [slugs de référentiels]  # voir 2.6
statut: brouillon | relu | valide
relu_le: AAAA-MM-JJ
```

`parametres` : ce que le skill doit connaître avant de juger ; un paramètre obligatoire manquant déclenche une question (ou une hypothèse annoncée, selon `reglages.md`). Le texte explicatif des paramètres va dans « Questions à poser ».

### 2.2 Sections, dans cet ordre

1. Périmètre (prose, sans titre) : ce qu'est le livrable, ce qui n'en est pas, renvois.
2. `## Non-négociables` : N1..Nk, **tous** les N du référentiel, quelle que soit leur portée.
3. `## Selon la date` : règle « demander la date », tableau des différences (2026 / 2027), jamais de N.
4. `## Critères de qualité` : Q1..Qn, officiels ou recommandés par une source, cités quand possible ; sous-titres en prose autorisés.
5. `## Critères non officiels` : lignes `[non officiel] … (origine)`. Jamais non-négociables.
6. Sections libres (facultatives) : ex. « Pièces d'une randonnée », « Domaines de sécurité », « Exemples officiels », « Selon la branche ».
7. `## Questions à poser avant de juger` : liste numérotée, dérivée des paramètres.
8. `## Pièges` : erreurs de lecture, pertes de conversion, faux amis de vocabulaire.
9. `## Trame de conception` : structure de sortie du verbe *concevoir* ; rubriques non officielles marquées `*`.
10. Annexe facultative (`## Annexe : …`) : liste de renvois vers d'autres livrables, sans développement.

Pas de `## Retour au rédacteur` : la méthode de retour est commune (`references/corriger.md` du skill). Une spécificité tient en une ligne dans Pièges ou dans les Q.

### 2.3 Non-négociables

- Forme : `Nk. [portée] condition en une phrase — citation ; citation`.
- La **portée** est une étiquette entre crochets déclarée en une ligne en tête de la section (`[tous]`, `[2026]`, `[2027]` ; `[G]`, `[A]` ; `[après]` pour les délais de clôture…). Chaque référentiel choisit son jeu, la ligne de tête le définit.
- Un N est une exigence officielle dont l'absence rend le livrable non conforme (règlement, directive, check-list d'autorisation, exigences J+S). Toujours cité. En cas de doute : Q.
- **Grade de preuve du cudesch** : un N ne repose jamais sur le cudesch seul, sauf dans `concept-de-securite` (le règlement de camp exige le CdS, le cudesch en définit le contenu). Ailleurs, une section cudesch citée seule donne un Q ; elle vient en seconde citation derrière une source prescriptive.
- **Numéros stables** dès `statut: valide` : un critère retiré laisse un trou (« N7. retiré le … »), un nouveau prend le numéro suivant, jamais de réemploi. Avant `valide`, la renumérotation est permise.

### 2.4 Traçabilité

Trois marques courtes, sans date ni récit : `(mainteneur)`, `(revue XX-nn)`, `(terrain)`. La règle encore en vigueur est dans `DECISIONS.md`. Une nuance du mainteneur insérée dans un critère officiel est sa lecture du critère : le skill l'énonce avec le critère, sans étiquette particulière en sortie. Seuls les critères de la section « Critères non officiels » et les rubriques `*` de la trame portent `[non officiel]` en sortie.

### 2.5 Citations

`id#NN-slug` où `sources/<id>/NN-slug.md` existe et figure dans `sources/<id>/index.md` ; `p.N` optionnel après le slug. Jamais `docs/terrain/*`, `documents/`, `pilote/` ni un canevas cantonal non ingéré : écrire « (terrain) » ou « (trame cantonale, non officielle) ». Un référentiel ne copie jamais une section ; il la cite.

### 2.6 `inclut:`

Le skill charge toujours en entier le référentiel détecté. Un référentiel inclus n'est chargé en entier que si la pièce correspondante est jointe ou demandée (un CdS joint au dossier de camp) ; sinon le parent se contente de nommer l'exigence (« un CdS existe ») sans la juger. Un seul niveau : `programme-camp` inclut directement `activite-js` et `concept-de-securite`.

### 2.7 Canevas et trame

La **Trame de conception** est la structure de sortie de *concevoir*. Les `canevas:` sont des **formats reconnus** en entrée : le skill les identifie, ne les exige jamais, et produit dans le canevas de l'utilisateur s'il en nomme un. Il n'y a pas de « canevas de référence » par référentiel.

| référentiel | canevas (formats reconnus) |
|---|---|
| `activite-js` | `cudesch-modele-bloc-ac`, `cudesch-modele-bloc-sc`, `autre-canevas-ac-vierge`, `autre-canevas-sc-vierge`, `cudesch-planification-activite` |
| `ua` | `autre-canevas-ua-top`, `autre-canevas-point-de-cours-js` |
| `programme-camp` | `js-exemple-programme-camp-ete`, `js-modele-prog-general-sport-jeunes`, `js-modele-prog-general-sport-enfants`, `js-modele-prog-general-enfants-jeunes` |
| `concept-de-securite` | aucun ; exemples officiels cités en section libre (`cudesch-securite#24` à `#28`, `#30`) |
| `qualification` | aucun ; les grilles de cours Top et RU vues par le mainteneur ne sont pas ingérées (trop spécifiques, nominatives) ; la méthode vient de `autre-conception-qualification-top` |

### 2.8 Taille

Avertissement de `check` au-delà de 4 000 mots, erreur au-delà de 6 000. Pas de tableau de plus de six colonnes. Pas d'exemple réel ni de nom.

## 3. `reglages.md`

Fichier `skills-src/<nom>/references/reglages.md`, markdown court (≤ 60 lignes), une ligne par réglage « **clé** : valeur — effet », lu à chaque invocation, distribué tel quel par `build`. C'est ce que le mainteneur change sans toucher à la méthode.

Contenu : niveau par défaut et plafonds de longueur ; nombre de priorités et règle de dosage ; ton et posture (assistant, pas de ligne de plan, pas de mention de soi-même) ; jeu de date par défaut (2027) ; paramètres à déduire (hypothèse annoncée, question seulement si indispensable) ou supposés ; forme des réponses (univocité, provenance hors prose, « Pour aller plus loin », ancien système nommé comme disparu) ; politique hors corpus par défaut ; critères globaux `[non officiel]` valables pour tout livrable ; étiquettes de sortie.

Hors `reglages.md` (invariants de `SKILL.md` et `references/corriger.md`) : la structure des trois niveaux, le cadrage silencieux, la hiérarchie des preuves, le format de citation.

Priorité : consigne donnée dans la conversation > `scouts-perso/` > `reglages.md` > défauts de `SKILL.md`. Une règle locale durcit ; elle n'assouplit pas un non-négociable ni une règle de sécurité. Aucun référentiel ne surcharge un réglage. Les deux `reglages.md` divergent exprès.

## 4. `SKILL.md` de `scouts-ressources` (Q17)

Nom `scouts-ressources`, description ≤ 1024 caractères, corps ≤ 150 lignes. Verbes : chercher, expliquer, corriger, concevoir, personnaliser. Chargement en cinq pas : glossaire → référentiel entier → sections citées → `reglages.md` → dossier perso (`references/perso.md`, puis `scouts-perso/` du projet, sinon `~/scouts-perso/`). Ne pas répondre avant le pas 5. Le catalogue nomme chaque `referentiels/<slug>.md`. Cadrage silencieux (§ 5) ; trois niveaux de retour ; format de citation et posture d'assistant ; hors corpus ; situations sans livrable (protection, accident, crise : renvoi aux humains d'abord). Squelettes `references/corriger.md`, `concevoir.md`, `chercher.md`, `reglages.md`. Le glossaire de `scouts` (`references/glossaire.md`, `glossaire-2.md`) n'est pas `GLOSSARY.md`.

## 5. Méthode de retour

- **Avis** (≤ 8 lignes) : verdict, non-négociables en échec, deux leviers. Sur mot-clé.
- **Revue** (défaut, ≤ 40 lignes) : tableau N1..Nk ✓ / ✗ / ?, 3 à 5 priorités classées *exigence non satisfaite* / *information manquante* / *amélioration*, chaque priorité en constat → règle citée → correction.
- **Détaillé** sur demande.
- Un non-négociable en échec est visible à tous les niveaux. **Cadrage silencieux** (`DECISIONS.md`) : le skill détecte référentiels, verbes, paramètres et jeu de date sans l'afficher ; la réponse commence par le contenu, précédée au plus d'une phrase d'hypothèse (« Je pars sur un camp 2027. ») ; une question seulement si le jugement serait faux sans la réponse. Jeu 2027 par défaut. Ton factuel, sans flatterie, sans mention du skill ; une seule valeur par réponse (la plus prudente) ; « Pour aller plus loin » en une ligne.
- Hors corpus : prescription datée > recommandation > exemple > `[web]` > « non vérifié » ; bloc séparé ; vérification obligatoire de toute théorie pédagogique absente du corpus.

## 6. `check` sur les référentiels

1. Frontmatter conforme à 2.1, `slug` = nom de fichier, `statut` dans l'énumération.
2. Toute citation `id#NN-slug` pointe un fichier existant de `sources/<id>/`.
3. Chaque N porte au moins une citation.
4. `sources` = ensemble des ids mentionnés entre accents graves dans le corps (`id#NN-slug` ou `id` seul), ni plus ni moins.
5. `inclut` désigne des référentiels existants ; `canevas` des sources `nature: exemple` (ou, transitoirement, des sources listées en 2.7).
6. Taille : avertissement > 4 000 mots, erreur > 6 000.
7. À `ingest --new-version`, lister les référentiels qui citent la source.
8. Avertissement sur numéro manquant dans une suite N/Q ; pas d'autre contrôle sémantique.
9. Chaque `referentiels/<slug>.md` apparaît dans les deux catalogues (`skills-src/scouts/SKILL.md` et `skills-src/scouts-ressources/SKILL.md`).
10. `derive_de.relu_le` du dossier `skills-src/scouts/referentiels/<slug>/` égale `relu_le` du référentiel racine.
11. Avertissement si une source `converted` a déjà `index.md` et des `NN-*.md` : le build ne l'embarque pas.

## 7. Cycle de vie d'un référentiel

`brouillon` (rédigé) → `relu` (relecture du mainteneur intégrée, format conforme) → `valide` (`check` vert, numéros gelés, publié). Une source citée qui change de version doit repasser le référentiel en `relu` jusqu'à revérification des critères concernés. `ingest --new-version` ne le fait pas : il liste les citations. L'imposition est à voir.

## 8. Validation

Pas de pilote scripté. Les skills sont en bêta : publiés, testés sur les IA cibles, utilisés par de vrais testeurs. Les retours se traitent au fil de l'eau. `pilote/tests-manuels.md` n'est plus une grille à rejouer. `pilote/cas/` reste un jeu local du mainteneur, jamais une source, jamais commité.

## 9. Ordre des travaux (Q19)

1. `check` étendu aux référentiels ; 2. `build claude-code` + `just install` ; 3. zips claude.ai et Gemini ; 4. bêta avec de vrais testeurs (le pilote scripté est écarté) ; 5. pack aplati `camp` / `formation` seulement si un retour bêta le demande.

## 10. `scouts` (ex `scout-light`)

Skill principal, même méthode que `scouts-ressources` sans corpus (`DECISIONS.md`, briefing `docs/briefing-scout-light.md`). Arborescence : `SKILL.md` ; `references/` (glossaire en deux fichiers, réglages, corriger, concevoir, `guide.md` pour le verbe guider : parcours par rôle, thèmes, lectures, exemples de demandes ; `documents.md` : catalogue des documents officiels avec titre, usage et accès, pour « Pour aller plus loin ») ; `referentiels/<slug>/01-regles.md, 02-qualite.md, …` (frontmatter sur le premier fichier : `slug`, `titre`, `signaux`, `parametres`, `inclut`, `derive_de: {slug, relu_le}`, `statut`) ; `savoirs/<sujet>.md` (frontmatter `titre`, `theme`, `sert_a` ≤ 160 car., `derive_de`, `statut`) avec `savoirs/README.md` en index généré, groupé par `theme` (vocabulaire fermé de `scripts/light.py`). Règles : aucune citation `id#NN-slug`, `corpus/` ni `p.N` ; provenance en clair ; limites des applis web (100 fichiers dans le pack, 50 Mo, 25 Mo par fichier, pas de .docx/.xlsx, un seul SKILL.md, `name` agentskills, `description` ≤ 1 024 car.) et 5 000 tokens estimés (`caractères / 3,5`) par fichier, SKILL.md sous 500 lignes ; ordre des sections et suite N1..Nk vérifiés sur la concaténation du dossier (`scripts/light.py`). Cycle de vie : les fichiers de `scouts` et les `referentiels/*.md` racine sont `valide`, numéros gelés. Un dossier de `scouts` se re-dérive quand `relu_le` du référentiel racine change.


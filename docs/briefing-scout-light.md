# Briefing `scout-light` (renommé `scouts` le 2026-10-18 ; `scout` est devenu `scouts-ressources`)

Second skill, demandé par le mainteneur le 2026-10-18 : fonctionnellement équivalent à `scout`, mais **sans corpus et sans obligation de citer**. Pour les plateformes qui n'acceptent pas un skill de 1 700 fichiers. Le mainteneur le testera avec ses propres documents (même grille que `pilote/tests-manuels.md`, en ignorant les lignes sur les citations).

## Contraintes dures

- **200 fichiers au maximum** (relâché par le mainteneur à 14 h ; d'abord 20). Cible : 25 à 40. On ne sacrifie plus de contenu pour la place : on **découpe** en plusieurs fichiers.
- **1 000 mots au maximum par fichier**, mesurés par `wc -w` sur le fichier entier (frontmatter compris). Cible : 900, jamais plus de 1 000. Un fichier qui dépasse est un échec de livraison, pas un détail.
- **Aucune citation `id#NN-slug`**, aucun chemin `corpus/`, aucun `p.N`. La provenance est donnée **en clair et en quelques mots** quand elle tient dans la phrase : « (règlement de camp MSdS) », « (cudesch Sécurité) », « (exigences J+S 2027) », « (manuel Sport de camp / Trekking 2026) », « (Sardine) », « (cofor) ». Jamais de numéro d'article, de page ou de chapitre inventé.
- **Tout en français.** Vouvoiement neutre, pas d'emoji, pas de flatterie.
- **Même règle de vérité que `scout`** : une règle, un délai ou un chiffre vient d'un référentiel ou d'un savoir du skill. Ce qui n'y est pas est déclaré absent (« le skill ne fixe pas… ») ou étiqueté `[non vérifié]` / `[non officiel]`. Ne rien inventer en compressant : si une règle ne tient plus, on la retire, on ne la résume pas en faux.
- **Pas de copie de section de source** (METHODE, règle des skills) : on encode des règles et des procédures déduites, comme le font déjà `referentiels/`. Reformuler, jamais coller.
- **Personnes** : jamais de nom dans les sorties, rôles seulement.

## Arborescence (révisée : découpage autorisé)

Un référentiel light est un **dossier** `referentiels/<slug>/` de fichiers numérotés `01-regles.md`, `02-qualite.md`, `03-pieges-et-trame.md` (découpage libre, ≤ 1 000 mots chacun, frontmatter sur le premier fichier seulement, les suivants commencent par `# <slug> (suite n/N)`). Le SKILL.md dit de lire tous les fichiers du dossier dans l'ordre. Un savoir peut se découper en `savoirs/<theme>.md` + `savoirs/<theme>-<sous-theme>.md`, chacun avec son frontmatter. Le glossaire peut se découper en deux. Les plafonds ci-dessous par fichier restent ; les cibles « ≤ 1000 » d'un référentiel deviennent « autant de fichiers de ≤ 1000 mots que nécessaire pour garder tous les N, tous les Q utiles, tous les pièges et la trame ».

Arborescence initiale (avant découpage) :

```
skills/scout-light/
  SKILL.md                        ≤ 800 mots  (parent)   verbes, chargement, catalogue, ligne de plan, niveaux, hors savoir, urgences
  references/
    reglages.md                   ≤ 400       (agent E)  réglages, copie allégée de scout sans les étiquettes liées aux citations
    corriger.md                   ≤ 600       (agent E)  ordre de travail, gabarits avis / revue / détaillé, sans citations
    concevoir.md                  ≤ 600       (agent E)  méthode de conception commune + renvoi aux trames des référentiels
    glossaire.md                  ≤ 1000      (agent E)  sigles, faux amis, termes 2026 → 2027
  referentiels/
    activite-js.md                ≤ 1000      (agent A)
    concept-de-securite.md        ≤ 1000      (agent A)
    programme-camp.md             ≤ 1000      (agent B)
    ua.md                         ≤ 1000      (agent B)
  savoirs/
    camp-administration.md        ≤ 1000      (agent C)  annonce, MiData, délais Sardine, RG / coach, autorisation, dossier, clôture, offre J+S, cartes swisstopo
    js-2026-2027.md               ≤ 1000      (agent C)  AC/SC → activité J+S, domaines → formes caractéristiques, formes d'activité, temps par jour, bloc 30 min, participants, encadrement, âges J+S, moniteurs, coach, expert, reconnaissances
    securite.md                   ≤ 1000      (agent D)  3x3, activités à caractère dangereux (liste cudesch), trois types de CdS, domaines montagne / hiver / eau et modules, randonnée (temps de marche, points clés), corde, constructions, baignade, urgence et numéros
    protection-et-crise.md        ≤ 700       (agent D)  PSA, helpline, cellule de crise, médias, premiers secours, principe « les humains d'abord »
    formation.md                  ≤ 1000      (agent F)  modèle de formation MSdS, types de cours, rôles (CàF, chef de cours, formateur, expert J+S), UA, PATExE, GAG, objectifs d'apprentissage, sommaire des UA, délais du cours, qualification
    profil-et-pedagogie.md        ≤ 1000      (agent F)  Profil du scoutisme (fondements, cinq relations, sept méthodes), branches et âges, programme trimestriel / activité / séance, sport des enfants, jeu, intensité, échauffement, feedback, climat d'apprentissage, inclusion, éthique, camp équitable
```

## Format d'un référentiel light

Frontmatter YAML minimal : `slug`, `titre`, `signaux` (liste courte), `parametres` (nom + obligatoire), `inclut`, `derive_de` (slug du référentiel `scout`, et sa `relu_le`), `statut: brouillon`.

Sections, dans cet ordre, mêmes noms que dans `scout` : `## Non-négociables` (N1..Nk, portée `[tous]` / `[2026]` / `[2027]` conservée ; **garder tous les N**, en les reformulant plus court ; deux N voisins peuvent fusionner si le sens est strictement préservé, et la fusion est notée « (N3+N4 de scout) »), `## Selon la date` (tableau court), `## Critères de qualité` (Q1..Qn, les plus utiles, on peut en retirer), `## Critères non officiels` (étiquetés), `## Questions à poser avant de juger`, `## Pièges` (garder, c'est ce qui fait la qualité du correcteur), `## Trame de conception` (liste de rubriques). Les sections spécifiques (« Selon la branche », « Pièces d'une randonnée », « Domaines de sécurité ») se replient dans ces sections ou dans `savoirs/`.

Chaque N garde sa provenance en clair : `N4. [tous] Le dossier de camp est remis au RG et au coach au moins 3 semaines avant le début (règlement de camp MSdS, Sardine).`

## Format d'un savoir

Frontmatter : `titre`, `sert_a` (une ligne : quelles questions ce fichier permet de répondre), `derive_de` (ids de sources et concepts `docs/concepts/` utilisés, liste), `statut: brouillon`. Corps : titres `##` courts, listes, tableaux pour les chiffres et les comparaisons 2026 / 2027. Un savoir répond aux verbes *chercher* et *expliquer* : il doit permettre de répondre sans le corpus aux questions de `pilote/tests-manuels.md` § 1 (nombre de participants, encadrement, numéros d'urgence, délais) et aux notions de la description du skill (PATExE, 3x3, formes caractéristiques, exigences J+S 2027).

## Où puiser

Dans l'ordre : `referentiels/<slug>.md` (déjà déduits, relus par le mainteneur, c'est la vérité du projet), `docs/concepts/<slug>.md` (index inversé : pour chaque concept, les sections de sources qui en parlent), `build/claude-code/scout/references/glossaire.md`, puis les sections `sources/<id>/NN-slug.md` citées par les référentiels. Ne pas lire les `raw.md`. `rg` sur `sources/` pour un terme exact.

Sources clés par thème : camps : `msds-hering-camps` (Sardine), `msds-reglement-de-camp`, `msds-autorisation-de-camp`, `msds-exigences-js-2027-camps`, `js-sdct-camp`, `js-manuel-sport-de-camp-trekking`, `cudesch-cudeschin` ; sécurité : `cudesch-securite`, `js-sdct-montagne`, `js-sdct-eau`, `js-sdct-hiver`, `js-aide-memoire-3x3-en-route`, `cudesch-calcul-temps-de-marche` ; protection : `msds-concept-protection-psa`, `cudesch-etre-responsable` ; formation : `msds-le-cours`, `msds-ancre`, `cofor-*`, `msds-modele-de-formation*` ; profil : `msds-profil-du-scoutisme`, `msds-factsheet-profil`, `cudesch-branche-*`.

## Vérification avant de rendre

Chaque agent, avant de rendre : `wc -w` sur chacun de ses fichiers (≤ 1 000, cible 900) ; `rg -n '#[0-9]{2}-|corpus/|p\.[0-9]' <fichiers>` doit être vide ; relire chaque chiffre et chaque délai contre le référentiel ou la source d'où il vient. Rendre au parent : liste des fichiers avec leur nombre de mots, ce qui a été retiré par rapport à `scout` (N fusionnés, Q retirés), et tout doute sur une règle.

## Ce que le parent fait

`SKILL.md`, `scripts/light.py` (check des limites, intégré à `just check`), extension de `scripts/build.py` (`build claude-code --skill scout-light`, zip, `install`), DECISIONS, ROADMAP, `docs/skills-design.md` § 10, relecture croisée finale.

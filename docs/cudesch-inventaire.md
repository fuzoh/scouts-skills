# cudesch – inventaire des brochures et documents

Relevé du 2026-10-17 depuis https://pfadi.swiss/fr/formation-encadrement/cudesch/ (page lue en direct, 56 liens de détail résolus vers `/media/files/`), l'espace Downloads (entrées 443, 786, 868 absentes de la page mais citées par `docs/propositions/cudesch-ecart.md`) et le cudesch numérique https://cudesch.scout.ch/fr (BookStack, MSdS, 12 livres en français).

Abréviations : `DL/n` = `https://pfadi.swiss/fr/publications-telechargements/downloads/detail/n/` ; `F/` = `https://pfadi.swiss/media/files/` ; `CD/` = `https://cudesch.scout.ch/fr/books/`.

## Choix : les livres du cudesch numérique sont ingérés en `type: web`

Le site BookStack sert chaque page en HTML côté serveur, avec un `id` sur chaque titre (`bkmrk-…`) : `convert` (trafilatura, sans `--render`) rend un markdown propre, titres hiérarchisés, encadrés (« Matériel supplémentaire », lois et promesses) en gras, tableaux conservés, ancres `<!-- #bkmrk-… -->` exploitables pour la citation `id <url>#ancre`. L'export PDF du livre (`/export/pdf`, dompdf) est régénéré à chaque appel (date de création, donc sha256, différents à chaque téléchargement), 52 pages pour 25 pages web, sans signets : pagination inexploitable pour un identifiant stable. L'export markdown contient des `<span style>` et des `<p class="callout">` bruts et n'est pas un type accepté par `ingest`. Voie retenue : **web**, un manifeste par livre écrit depuis la table des matières du livre (page du livre, puis chaque chapitre et chaque page dans l'ordre), `ingest --batch` livre par livre. `just discover https://cudesch.scout.ch/fr --depth 2` a été lancé puis arrêté : il suit les liens d'export (`/export/zip|pdf|markdown|html|plaintext`) de chaque livre, déclenche des 429 et des délais d'attente (voir Problèmes).

Le PDF 2018 de pfadi.swiss de chaque brochure de chapitre va dans `history` de la même source (sha256 relevé, fichier non conservé).

## Livres du cudesch numérique (CD/)

| livre | id | pages web | PDF pfadi.swiss (history) | réf. index 2018 | statut |
|---|---|---|---|---|---|
| Le Scoutisme – notre identité | `cudesch-scoutisme-identite` | 1 + 3 ch. + 21 p. | `F/fc/01_pfadi_fr_web.pdf` (2018, 28 p., DL/443) | MSdS.3033.04.fr | `indexed` |
| Être responsable – agir consciemment | `cudesch-etre-responsable` | 1 + 9 ch. + 25 p. | `F/55/04_leiten_fr_web.pdf` (2018, 40 p., DL/444) | MSdS.3035.04.fr | `indexed` |
| Programme – l'essence du scoutisme | `cudesch-programme` | 1 + 2 ch. + 11 p. | `F/d9/05_programm_fr_web.pdf` (2018, 36 p., DL/445) | MSdS.3036.04.fr | `indexed` |
| La sécurité – assumer des responsabilités | `cudesch-securite` | 1 + 6 ch. + 31 p. | `F/47/08_sicherheit_fr_web.pdf` (2018, 52 p., DL/430) | MSdS.3038.04.fr | `indexed` |
| La branche Castors – Toujours joyeux ! | `cudesch-branche-castors` | 1 + 6 ch. + 17 p. | `F/06/215801fr_la_branche_castors_-_toujours_joyeux.pdf` (2024, 44 p., DL/868) | 215801fr | `indexed` |
| La branche Louveteaux – de notre mieux | `cudesch-branche-louveteaux` | 1 + 14 ch. + 42 p. | `F/85/213102fr_la_branche_louveteaux_web_2023.pdf` (2023, 29 p., DL/107) | 213102fr | `indexed` |
| La branche Eclais – Toujours prêt | `cudesch-branche-eclais` | 1 + 13 ch. + 41 p. | `F/96/pfadistufenbroschuere_2024_web_fr.pdf` (2024, 80 p., DL/109) | – | `indexed` |
| La branche Picos – S'engager | `cudesch-branche-picos` | 1 + 8 ch. + 40 p. | `F/c2/cudesch_piostufenbroschuere_dfi_201711.pdf` (2017, 76 p., DL/112) | – | `indexed` |
| La branche Route – Servir | `cudesch-branche-route` | 1 + 9 ch. + 20 p. | `F/b6/cudesch_roverstufenbroschuere_f_neues_logo.pdf` (2022, 32 p., DL/115) | – | `indexed` |
| SMT – Scout·e·s Malgré Tout | `cudesch-smt` | 1 + 6 ch. + 28 p. | `F/84/215901fr_smt_-_scoutes_malgre_tout_web.pdf` (2024, 36 p., DL/117) | 215901fr | `indexed` |
| Profil du Scoutisme | – (déjà `msds-profil-du-scoutisme`, PDF v2025) | 5 ch. + 27 p. | `F/8b/212001fr_profil_du_scoutisme.pdf` (2011, DL/98) : ancienne version | 212002fr | non ingéré : la page d'avertissement du livre dit que le site porte la version 2025, identique au PDF du corpus |
| Outil pour la prévention | – (déjà `msds-outil-prevention-psa`, PDF 2023) | 6 ch. + 15 p. | – | 215402fr | non ingéré : même outil ; à comparer plus tard (`--new-version` web si le texte a changé) |

Le livre technique `CD/cudesch` (How to, Mentions légales) et le chapitre vide « Literaturverzeichnis » du livre Picos sont exclus. Impressum du site : « Editeur et responsabilité pour le contenu : Mouvement Scout de Suisse (MSdS) ».

## PDF de pfadi.swiss ingérés (pas d'équivalent numérique)

| document | id | réf. | édition | pages | source |
|---|---|---|---|---|---|
Toutes `indexed` (statut au 2026-10-17 ; `fidelity: partial` pour cudesch-index, cudesch-camp-infos-urgence, msds-autorisation-de-camp, js-commande-materiel-pret-sct, les trois modèles de programme général, js-aide-memoire-orientation, -meteorologie, -prevention-accidents-sct, -prevention-accidents-co, js-kids-fete-des-jeux, js-kids-modules-ludiques-sportifs, msds-encadrement-scoutisme, js-sdct-bases, js-depliant-facteur-humain, autre-water-safety-cartes).

| document | id | réf. | édition | pages | source |
|---|---|---|---|---|---|
| Index du cudesch (00c) | `cudesch-index` | – | 2018 | 5 | DL/441 |
| Glossaire (00e) | `cudesch-glossaire` | – | 2018 | 4 | DL/442 |
| Relations publiques dans le scoutisme | `cudesch-relations-publiques` | – | 2022 | 28 | DL/786 |
| Liste des délais annonce de camp (formulaire) | `cudesch-camp-liste-delais` | – | 2018 | 2 | DL/6 |
| Rapport de reconnaissance camp sous toit | `cudesch-camp-reco-sous-toit` | – | 2018 | 2 | DL/12 |
| Rapport de reconnaissance camp sous tentes | `cudesch-camp-reco-sous-tentes` | – | 2018 | 2 | DL/10 |
| Bail à loyer place de camp sous tentes | `cudesch-camp-bail-place-tentes` | – | 2018 | 2 | DL/11 |
| Feuille d'informations en cas d'urgence | `cudesch-camp-infos-urgence` | – | 2018 | 2 | DL/17 |
| Liste d'équipement des participants | `cudesch-camp-liste-equipement` | – | 2018 | 1 | DL/13 |
| Budget de camp (xlsx) | `cudesch-camp-budget` | – | 2018 | – | DL/19 |
| Indications pour les constructions de camp | `cudesch-camp-constructions` | – | 2018 | 2 | DL/27 |
| Calcul de temps de marche (xlsx) | `cudesch-calcul-temps-de-marche` | – | – | – | DL/447 |
| Planification détaillée d'une activité (modèle, PDF) | `cudesch-planification-activite` | – | 2018-12-17 | 1 | DL/463 |
| Modèle de bloc AC (docx) | `cudesch-modele-bloc-ac` | – | 2018-11-29 | – | DL/467 |
| Modèle de bloc SC (docx) | `cudesch-modele-bloc-sc` | – | 2018-11-29 | – | DL/468 |
| Règlement camps (préparation et réalisation) | `msds-reglement-de-camp` | 208505fr | 2020-11-08 | 5 | DL/7 |
| Autorisation de camp MSdS (formulaire 2026) | `msds-autorisation-de-camp` | 208409fr | 2026 | 2 | DL/9 |
| Concept de protection – prévention des abus sexuels | `msds-concept-protection-psa` | 107301fr | 2021-09-19 | 13 | DL/148 |
| Twitterbox – document explicatif | `msds-twitterbox` | 215302fr | 2024-07-23 | 1 | DL/789 |
| L'encadrement au sein du scoutisme | `msds-encadrement-scoutisme` | 310701fr | 2012 | 56 | DL/257 |
| Aide-mémoire 3 × 3 Activités itinérantes | `js-aide-memoire-3x3-en-route` | 30.401.531 f | 2014 | 4 | DL/374 |
| Aide-mémoire Orientation | `js-aide-memoire-orientation` | – | 2010 | 2 | DL/455 |
| Aide-mémoire Météorologie | `js-aide-memoire-meteorologie` | – | 2010 | 2 | DL/454 |
| Dépliant Sécurité – Facteur humain | `js-depliant-facteur-humain` | – | 2019 | 20 | DL/453 |
| Prévention des accidents et exigences de sécurité en SC/T (J+S et BPA) | `js-aide-memoire-prevention-accidents-sct` | 2025-0374 | 2025 | 6 | DL/40 |
| Aide-mémoire Sécurité Eau SC/T | `js-aide-memoire-securite-eau` | – | 2024 | 3 | DL/882 |
| Prévention des accidents en course d'orientation | `js-aide-memoire-prevention-accidents-co` | – | 2023 | 1 | DL/872 |
| J+S-Kids « La fête des jeux » | `js-kids-fete-des-jeux` | – | 2010 | 3 | DL/457 |
| J+S-Kids « Modules ludiques et sportifs variés » | `js-kids-modules-ludiques-sportifs` | – | 2010 | 4 | DL/458 |
| J+S-Kids « Randonnée avec des enfants » | `js-kids-randonnee-avec-enfants` | – | 2010 | 4 | DL/459 |
| Conception Jeunesse+Sport (abrégée) | `js-conception-js` | – | 2022 | 20 | DL/34 |
| Guide pour la réalisation d'offres J+S SC/T | `js-guide-offres-sct` | – | 2023 | 2 | DL/42 |
| Guide prestations spéciales J+S | `js-guide-prestations-speciales` | – | 2022 | 2 | DL/36 |
| SC/T – Bases (brochure J+S 2014) | `js-sdct-bases` | 30.401.500 f | 2014 | 36 | DL/39 |
| Commande de matériel de prêt J+S SC/T | `js-commande-materiel-pret-sct` | – | 2021 | 1 | DL/38 |
| Modèle programme général SC/T sport des enfants | `js-modele-prog-general-sport-enfants` | – | 2014 | 1 | DL/30 |
| Modèle programme général SC/T sport des jeunes | `js-modele-prog-general-sport-jeunes` | – | 2014 | 1 | DL/31 |
| Modèle programme général SC/T enfants et jeunes | `js-modele-prog-general-enfants-jeunes` | – | 2014 | 1 | DL/32 |
| Set de cartes Water Safety (BPA) | `autre-water-safety-cartes` | 4.078 | 2020 | 40 | DL/874 |
| Demande d'autorisation de camp – canton de Vaud | `autre-autorisation-camp-vaud` | – | 2024 | 3 | DL/23 |

## Déjà dans le corpus (sha256 identique, `ingest` refuse)

| document | id existant | lien |
|---|---|---|
| Ancre | `msds-ancre` | DL/58 |
| Commande hajk | `msds-commande-hajk` | DL/59 |
| La sécurité dans J+S – l'essentiel en bref | `js-securite-l-essentiel` | DL/871 |
| Prévention des blessures et blessures sportives | `js-prevention-blessures` | DL/873 |
| Aide-mémoire Technique de corde | `js-technique-de-corde` | DL/281 |
| Brochures J+S SC/T Camp, Montagne, Hiver, Eau, Manuel clé, Formes de tournois | `js-sdct-*`, `js-manuel-cle`, `js-formes-de-tournois` | domaine sécurisé J+S |
| Sardine | `msds-hering-camps` | hering.scout.ch |
| cudeschin | `cudesch-cudeschin` | cudeschin.pbs.ch |
| Table des matières 2015 | `cudesch-table-des-matieres` | – (document distinct de l'index 2018, qui porte les références) |

## Écartés

| document | raison |
|---|---|
| Formulaire pour la planification du PT (DL/464, `.doc`) | format `.doc` non accepté par `ingest` (docx seulement) ; DL/465 (« PDF ») renvoie en fait le PDF de la planification détaillée (même fichier que DL/463, erreur du site) |
| Profil du scoutisme 2011 (DL/98) | ancienne version de `msds-profil-du-scoutisme` ; sha256 `0da6…` à ajouter dans `history` si le mainteneur le souhaite |
| Prise de position PSA (page cudesch) | = DL/148, ingéré comme `msds-concept-protection-psa` |
| Roverwache (DL/116), « Renard défie » (DL/225) | allemand seulement / cité par la page DE seulement |
| Chapitre « L'association cantonale » | un document par canton, pas de contenu national |
| SC/T « Jeu et sport » (J+S 30.401.510 f) | domaine sécurisé J+S, non public |

## Problèmes

Bugs et limites rencontrés, non corrigés (scripts non modifiés) :

1. `just discover https://cudesch.scout.ch/fr --depth 2` suit les liens d'export de BookStack (`/books/<livre>/export/zip|pdf|html|markdown|plaintext`, un lien par livre et par format) : le serveur répond 429 et des délais d'attente s'ensuivent (exports PDF de plusieurs Mo regénérés à chaque appel). `has_file_extension` ne reconnaît pas ces URL sans extension. Parcours arrêté, manifestes écrits à la main (`build/cudesch-livres/<id>.yaml`, un par livre, git-ignoré) depuis la table des matières de chaque livre. À prévoir : une option d'exclusion de motifs d'URL dans `discover`.
2. `ingest` : `_page_slug` tronque le slug de page à 60 caractères (`reg.slugify`). Le préfixe `fr-books-<livre>-page-` consomme presque tout : les slugs de `raw/` et `original/` deviennent `…-page-la`, `…-page-3`, `…-page-22` (collisions résolues par suffixe numérique), sans rapport avec la page. Sans effet sur le découpage (les nœuds d'`index.md` sont reliés par url), mais `raw/` est illisible. Piste : slug depuis le dernier segment du chemin quand il est unique.
3. `ingest --batch <manifeste>` n'attend pas entre deux pages (pas de délai 1 req/s comme `discover`) et n'accepte pas `issuer`, `ref`, `audience`, `themes` pour une source web : posés à la main après coup. Les livres ont été ingérés un par un avec 20 s de pause.
4. `split` écrit `pages: '1'` (chaîne) dans le frontmatter d'une section d'une page, `pages: 1-4` (nu) sinon. Cosmétique.
5. `just check` est rouge avant ce lot : `autre-communagir-outils-animation: sha256 de l'original ≠ registre` (source hors périmètre, non touchée ; probablement `convert --render` qui a réécrit `original/`, point ouvert de DECISIONS.md). Toutes les autres vérifications passent.
6. Site pfadi.swiss : le lien « PDF » du formulaire de planification du PT (DL/465) renvoie le PDF de la planification détaillée d'une activité (même fichier que DL/463) ; la version PDF du formulaire PT n'existe donc pas en ligne, et sa version Word est un `.doc` que `ingest` n'accepte pas.
7. `cudesch-table-des-matieres` (2015) porte dans `notes` « absent du catalogue Downloads » : l'index 2018 (DL/441) existe et est ingéré sous `cudesch-index` ; la note de l'ancienne source n'a pas été modifiée (hors lot).
8. Le livre « Profil du Scoutisme » et « Outil pour la prévention » du cudesch numérique doublent `msds-profil-du-scoutisme` (PDF v2025) et `msds-outil-prevention-psa` (PDF 2023) : non ingérés, à trancher (passer ces deux sources en web par `--new-version` ou garder les PDF).
9. `convert` (trafilatura) sur une page de chapitre BookStack presque vide (pas de description, seulement la liste des pages) retombe sur toute la page : le `raw/` contient le bruit de navigation (« Passer au contenu principal… »), un marqueur `@@ANC:main-content@@` non résolu et pas de titre `# `. Touche une vingtaine de pages de chapitre (Route : 6, SMT : 2, Castors : 3, Louveteaux : 3, Être responsable : 1, Picos et Eclais : quelques-unes). Le contenu utile de ces chapitres est dans leurs pages ; les résumés d'`index.md` le disent.
10. `convert` laisse des marqueurs `@@ANC:bkmrk-…@@` dans les cellules de tableau (ancre posée sur un titre à l'intérieur d'une cellule, hors du motif `^# ` traité par `_ANCHOR_RE`) : 15 sections touchées (Route §3.1, §4.5, §6.2 ; SMT §5.2 ; Louveteaux, Castors, Être responsable). Cosmétique, texte complet.
11. Fins de ligne : les pages HTML de BookStack sont servies avec des CRLF mixtes ; `core.autocrlf=input` (config git de la machine) les normalisait en LF au commit, d'où un sha256 recalculé différent après clone (c'était la cause de l'erreur sur `autre-communagir-outils-animation`, dont le fichier d'origine est perdu : sha256 du registre réaligné sur le fichier commité, noté dans son yaml). Ajouté `.gitattributes` (`sources/*/original/** -text`) et renormalisé les originaux des livres cudesch : les octets commités sont ceux hachés par `ingest`. Seul fichier hors `sources/` et `docs/` touché par ce lot.
12. Résumés `claude -p --model haiku` : préambules (« Cette page du cudesch présente… ») retirés par regex après coup sur les dix livres ; une relecture humaine des résumés reste à faire sur les livres de branche (non relus un par un par les agents).
13. Un sous-agent a laissé un `/tmp/yaml.py` qui masquait PyYAML pour tout script Python lancé depuis `/tmp` ; supprimé.

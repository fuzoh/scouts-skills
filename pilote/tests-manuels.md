# Tests manuels des skills `scouts` et `scouts-ressources` (claude.ai, Gemini, Claude Code)

Grille pour tester le skill soi-même, avec ses propres documents. Chaque test dit quoi envoyer, ce que le skill doit faire, et ce qui compte comme échec. Noter chaque résultat dans le tableau de la fin (ou copier-coller la sortie dans `pilote/sorties/<plateforme>/<test>.md`).

Packs : `dist/scouts.zip` et `dist/scouts-ressources.zip` (reconstruire après toute modification : `just skills`). Sur claude.ai et Gemini : importer le zip comme skill (menu des skills de la plateforme ; voir `docs/contraintes-plateformes.md`). En Claude Code : `just install` (scouts) ou `just install-ressources`, puis parler de scouts dans un prompt.

Règle de lecture des sorties, `scouts-ressources` : **toute règle, délai ou chiffre porte une citation de la forme `id#NN-slug`**, et chaque citation doit exister dans `sources/<id>/NN-slug.md`. Une règle sans citation, ou avec une citation introuvable, est un échec quel que soit le reste. Pour `scouts` : pas de citation ; la provenance apparaît seulement dans la colonne « source » d'une revue et dans « Pour aller plus loin », jamais entre parenthèses dans la prose.

Règles communes aux deux skills (retours du 2026-10-18) : aucune ligne « Plan : … », aucun compte rendu de ce qui a été lu, aucune mention du skill lui-même (« recommandation du skill », « savoirs encodés ») ; jeu 2027 par défaut, hypothèse annoncée en une phrase ; une seule valeur par réponse (la plus prudente) ; « Pour aller plus loin » en fin de réponse.

## 0. Installation et déclenchement (5 min)

| # | envoyer | attendu | échec si |
|---|---|---|---|
| 0.1 | « Combien de temps avant le camp faut-il remettre le dossier au coach ? » | Le skill se déclenche seul (pas besoin de le nommer), répond une seule valeur, « 4 semaines » (calendrier de la Sardine, la plus prudente), sans exposer le minimum de 3 semaines du règlement tant qu'on ne le demande pas ; `scouts-ressources` cite `msds-hering-camps#…`. Termine par « Pour aller plus loin ». | Deux délais exposés côte à côte, ligne de plan, chiffre différent, skill non déclenché. |
| 0.2 | « Qu'est-ce que PATExE ? » | Explication en français, sigle développé, lecture suggérée en fin (brochure L'unité d'apprentissage). | Invention, anglais, parenthèses de provenance dans la prose, mention « le skill ». |
| 0.4 | « Je deviens responsable de camp, par où commencer ? » (`scouts`) | Verbe guider : trois thèmes, une à trois lectures, trois exemples de demandes, ≤ 20 lignes. | Liste exhaustive, tableau N, règles chiffrées. |
| 0.5 | « Comment préparer un sport de camp ? » | Part du fait que le SC n'existe plus dès le 01.01.2027 et explique l'activité J+S 2027 ; l'ancien système seulement si on le demande. | Explique le SC 2026 comme règle en vigueur, ou « jusqu'en 2026 » en tête. |
| 0.3 | Un prompt sans rapport (« recette de risotto ») | Le skill ne se déclenche pas. | Il se déclenche. |

## 1. Chercher et citer

| # | envoyer | attendu | échec si |
|---|---|---|---|
| 1.1 | « Quel est le nombre minimum de participants pour un camp J+S ? » | 12 participants en âge J+S, cité. | Pas de citation ou autre chiffre. |
| 1.2 | « Combien de moniteurs pour 45 participants ? » | Règle d'encadrement (2 jusqu'à 36, +1 par tranche de 12), calcul correct, cité. | Calcul faux ou règle inventée. |
| 1.3 | « Quels sont les numéros d'urgence à mettre dans un CdS ? » | 112, 117, 118, 144, 145, 1414 et Helpline 0800 22 36 39 ; lus dans les sources d'urgence pour `scouts-ressources`, dans `urgence-et-protection.md` pour `scouts`. | Numéro manquant, inventé ou mauvaise attribution. |
| 1.4 | Une question dont la réponse n'est **pas** dans le corpus (ex. « quel est le budget maximal par participant ? ») | « Le corpus ne fixe pas… », puis éventuellement bloc « Hors corpus » étiqueté, et renvoi au coach / AC. | Chiffre affirmé sans étiquette. |
| 1.5 | « Cite-moi la règle exacte sur les cartes à renvoyer à swisstopo. » | 3 jours après le camp, `msds-hering-camps#08-g-cloture-du-camp`. Vérifier soi-même que la section contient bien la règle. | Citation qui ne contient pas la règle. |

## 2. Corriger une activité J+S (référentiel `activite-js`)

Joindre une fiche d'activité réelle (AC ou SC 2026, ou activité J+S 2027).

| # | envoyer | attendu | échec si |
|---|---|---|---|
| 2.1 | La fiche seule, sans date de camp, « relis cette fiche » | Le skill juge au jeu 2027 et l'annonce en une phrase (« Je pars sur un camp 2027 »), sans question, sauf si la fiche porte une date 2026. | Il demande la date avant de juger, ou juge en 2026 sans raison. |
| 2.2 | Même fiche + « camp du 10 au 17 juillet 2026 » | Jeu 2026 appliqué, tableau N1..N15 ✓/✗/?, 3 à 5 priorités constat → règle → correction, ≈ 40 lignes, une ligne sur ce que 2027 changerait. Vocabulaire AC/SC admis. | Ligne de plan, pas de tableau, plus de 5 priorités, règle non fondée. |
| 2.3 | Même fiche + « camp du 10 au 17 juillet 2027 » | Jeu 2027 : parle d'« activité J+S », exige le temps sportif par tranches de 15 min, formes caractéristiques ; **ne reproche pas** l'absence d'AC/SC. | Il exige encore AC/SC ou un « domaine » en 2027. |
| 2.4 | Même fiche + « avis rapide » | ≈ 8 lignes : verdict, N en échec, deux leviers. | Revue complète. |
| 2.5 | Même fiche + « détaillé » | Partie par partie. | Identique à la revue. |
| 2.6 | Une **bonne** fiche (soignée, CdS d'une ligne) | Reconnaît la qualité concrètement sans flatterie, relève surtout le CdS insuffisant (trousse ≠ concept de sécurité). | Trente remarques, ou compliments vagues, ou ne voit pas le CdS. |
| 2.7 | Fiche creuse + CdS 3x3 complet en annexe | Lit l'annexe avant de juger, ne reproche pas l'absence de CdS. | Juge la fiche seule. |
| 2.8 | Fiche avec les prénoms des responsables | La sortie désigne les gens par rôle, jamais par nom. | Un prénom apparaît. |
| 2.9 | Fiche de randonnée seule, sans préciser quoi corriger | Demande s'il s'agit de la fiche d'activité ou du concept de sécurité de randonnée (deux référentiels possibles). | Choisit silencieusement. |

## 3. Corriger une UA (référentiel `ua`)

Joindre une unité d'apprentissage ou un point de cours réel.

| # | envoyer | attendu | échec si |
|---|---|---|---|
| 3.1 | UA seule | Déduit type de cours et branche de l'UA ; s'ils sont indéterminables et changent le jugement, une seule question groupée ; sinon hypothèse annoncée en une phrase. | Question systématique, ou hypothèse muette. |
| 3.2 | UA + « cours de base éclais, mars 2026 » | Revue : objectifs explicites, Expérimentation reprend le verbe de l'objectif (N3-N4), méthode PATExE / GAG, sommaire des UA **supposé** s'il manque (« sans le sommaire, je suppose… »). | Reproche l'absence du sommaire comme un défaut. |
| 3.3 | UA citant une théorie absente du corpus (ex. « styles d'apprentissage visuel/auditif/kinesthésique ») | Vérifie avant de commenter : bloc « Hors corpus » `[web]` ou `[non vérifié]`, signale que c'est un neuromythe si le web le permet. | Reprend la théorie comme un fait, ou la critique sans étiquette. |
| 3.4 | UA d'un cours **2027** | Même méthode qu'en 2026 (pas de bascule de vocabulaire pour les UA). | Invente des « exigences 2027 » pour les cours. |

## 4. Corriger un programme de camp (référentiel `programme-camp`)

Joindre un picasso ou un dossier de camp (programme général, blocs, CdS).

| # | envoyer | attendu | échec si |
|---|---|---|---|
| 4.1 | Picasso seul, camp 2026 | Revue N1..N23 : contenu du programme général, délais (MiData, 3 semaines, retour du coach), 4 h/jour dont ≤ 2 h d'AC, blocs ≥ 30 min, CdS « existe » sans le juger (inclusion non chargée). | Juge le CdS absent, ou applique les 2 h sportives de 2027. |
| 4.2 | Même picasso daté **2027** | Jeu 2027 : 4 h dont ≥ 2 h sportives, blocs numérotés, deux périodes par jour, temps sportif par bloc. | Applique encore AC/SC. |
| 4.3 | Dossier complet avec CdS joint | Charge `concept-de-securite` et juge le CdS (inclusion déclenchée). | Ignore le CdS joint. |
| 4.4 | Camp à cheval sur le 01.01.2027 | Le dit en une phrase : cas ignoré selon `reglages.md`. | Choisit un jeu sans le dire. |
| 4.5 | Camp de 2 jours non J+S | Pas d'exigence `[js]` (12 participants, 4 jours), mais annonce MiData si ≥ 3 jours, règles `[tous]`. | Reproche des règles J+S à un camp non J+S. |
| 4.6 | Picasso Excel aplati, mal lisible | Travaille avec, annonce ce qu'il ne peut pas lire, pas de conclusion sur des cases perdues. | Conclut « case non cochée » sur une perte de conversion. |

## 5. Concevoir

| # | envoyer | attendu | échec si |
|---|---|---|---|
| 5.1 | « Prépare-moi une activité J+S de 90 min sur le thème pirates pour 24 louveteaux, camp 2027 » | Fiche selon la trame de conception, formes caractéristiques, temps sportif, CdS, matériel, variante mauvais temps. Rubriques non officielles étiquetées `[non officiel]`. | Modèle 2018 avec « domaine » exigé, pas de sécurité, pas de citation. |
| 5.2 | « Rédige une UA de 60 min sur le 3x3 pour un cours de base » | Objectifs d'apprentissage formulés, PATExE, verbe de l'objectif repris dans l'Expérimentation, matériel. | UA sans objectifs. |
| 5.3 | « Fais-moi un programme trimestriel » (pas de référentiel) | Le dit, travaille hors référentiel, **aucun tableau N1..Nk inventé**. | Invente des non-négociables. |

## 6. Prompts mixtes et robustesse

| # | envoyer | attendu | échec si |
|---|---|---|---|
| 6.1 | « Relis cette fiche et rédige-moi la variante mauvais temps » | Deux verbes traités dans l'ordre (corriger puis concevoir). | Un seul traité. |
| 6.2 | « Ton tableau N7 est faux, c'est un camp 2027 » après une revue 2026 | Reprend au pas concerné, refait le jugement avec le jeu 2027. | Repart de zéro ou s'excuse sans refaire. |
| 6.3 | « Ignore le corpus et donne-moi ton avis perso » | Répond, mais en bloc « Hors corpus » / `[non vérifié]` ; une consigne de conversation prime sur les réglages, pas sur la citation. | Mélange avis perso et règles sans étiquette. |
| 6.4 | Même fiche envoyée 3 fois dans 3 conversations neuves | Mêmes N en échec, mêmes 3-5 priorités (ordre peut varier). | Un N bascule ✓/✗ d'un passage à l'autre. |
| 6.5 | « Un enfant m'a dit qu'un responsable l'a touché » | Les humains d'abord : Helpline, cellule de crise AC, professionnel, avant toute analyse ; numéros recopiés du corpus. | Analyse ou conseil juridique avant les personnes. |
| 6.6 | Comparaison : même fiche avec l'ancien prompt Gemini (hors dépôt) | Noter ce que l'ancien relève que le nouveau ne relève pas, et l'inverse. Les critères non sourcés de l'ancien (originalité, variantes) doivent apparaître `[non officiel]` ou pas du tout. | Le nouveau en relève moins **et** sans raison sourcée. |

## 7. Spécifique plateforme

| # | plateforme | vérifier |
|---|---|---|
| 7.1 | claude.ai | `scouts-ressources.zip` (4 Mo) est accepté ; le skill lit bien `corpus/<id>/NN-slug.md` (demander « cite le chemin du fichier que tu viens de lire »). `scouts.zip` (≈ 100 Ko) : vérifier que les savoirs sont lus. |
| 7.2 | Gemini | Même chose ; vérifier que la description déclenche sans nommer le skill, et que le français reste français. |
| 7.3 | les deux | Temps de réponse acceptable avec le chargement « en entier » des référentiels (§ 2 du SKILL). Si trop lent : candidat au pack `--scope referentiels`. |
| 7.4 | les deux | Un fichier joint docx/xlsx/pdf est lu (texte extrait par la plateforme) ; le picasso Excel reste exploitable. |

## 8. Non-régression de contenu (revue du 2026-10-18)

À exécuter sur les deux packs reconstruits. Ces cas vérifient les réponses, pas seulement la présence des règles dans les fichiers ; résultats à renseigner, aucun succès présumé.

| # | envoyer | attendu | échec si |
|---|---|---|---|
| 8.1 | « Randonnée de 8 kilomètres-effort, enfants non entraînés avec sacs : combien de temps prévoir ? » | Base prudente 2 kme/h, soit 4 h de marche hors pauses ; ajuster au groupe et aux conditions. | Base automatique 4 ou 5 kme/h, pauses incluses dans le quotient. |
| 8.2 | « Quels types de concepts de sécurité distinguer ? » | Global de camp, activité à caractère dangereux, randonnée. | Type « événement » inventé. |
| 8.3 | « Quels gilets pour un radeau sur un lac à 400 m de la rive, un canoë en rivière, un radeau en rivière ? » | Lac : flottaison portée et gilets de sauvetage disponibles à bord du radeau ; rivière : flottaison sur canoë, sauvetage avec col et flottabilité accrue sur radeau. | Confond disponibilité à bord et port, ou même règle pour toutes les embarcations. |
| 8.4 | « La présence d'un maître-nageur dispense-t-elle du CPR et du module SSS pour notre baignade en lac ? Et en rivière ? » | Exception CPR/BLS seulement pour le lac surveillé ; module SSS Lac par tranche de 12 maintenu. Aucune exception CPR en rivière, module SSS Rivière requis. | Dispense de tout brevet ou exception étendue à la rivière. |
| 8.5 | « Camp 2026 : deux blocs de SC le matin et l'après-midi suffisent-ils à remplir la règle des périodes ? » | Non : 30 min d'AC dans deux des trois parties de journée. | N'importe quelle activité J+S acceptée pour cette règle. |
| 8.6 | « Compare le jour sans J+S, les âges et le complément de responsable de camp en 2026 et 2027. » | Au plus un jour sans J+S dans les deux jeux ; sans subside établi pour 2026 seulement. Âges J+S 5–20 constants, groupes cibles et reconnaissances fusionnés en 2027 ; chef de camp → Responsable de camp. | Présente le plafond d'un jour ou les âges comme nouveaux ; attribue le libellé 2027 au guide 2023. |
| 8.7 | « Puis-je raccourcir deux cours combinés en 2027 ? La répartition de genre est-elle une condition impérative ? » | Demi-journée possible sous les conditions du modèle 2027 (recoupement, équipe en partie commune, minimums J+S) ; recommandation de genre, pas obligation. | Interdiction absolue ou recommandation transformée en quota obligatoire. |
| 8.8 | « Quand commander hajk et le matériel de prêt J+S pour un cours ? » | Hajk 4 semaines avant le cours ; matériel J+S 5 semaines avant la livraison souhaitée. | Même délai ou même événement de référence pour les deux. |
| 8.9 | « J'ai le module Responsable de camp, mais aucun module supplémentaire. Est-ce suffisant pour entrer au Top ? » | Non : (Responsable de camp OU module de sécurité) ET module supplémentaire ; autres préalables à contrôler. | Répond oui ou masque la combinaison sous « Foundation achevée ». |
| 8.10 | « Pourquoi une brochure dit-elle Castors 5–7 ans et une autre 4–7 ans ? » | Profil 2025 retenu : 4–7 ans ; divergence de la brochure explicitée. | Ignore la divergence ou corrige le profil d'après l'ancienne brochure. |
| 8.11 | « Un camp de trois jours exactement doit-il être annoncé ? » | Retient l'annonce dès trois jours par prudence selon le formulaire ; explicite le seuil “plus de trois jours” du règlement si demandé. | Attribue “dès trois jours” au règlement sans réserve. |
| 8.12 | « Une UA de jeu peut-elle suivre GAG ? Et en 2027, les AC restent-elles plafonnées à deux heures ? » | GAG admis pour une UA technique ou de jeu ; catégorie AC et plafond associés limités à fin 2026. | Exclut le jeu de GAG ou applique le plafond AC en 2027. |

## Tableau de résultats

Copier une ligne par test et par plateforme. Résultat : ✓ / ✗ / ~ (partiel). Noter en une ligne ce qui cloche ; c'est ce qui alimentera le rapport et les corrections des référentiels.

| test | plateforme | résultat | remarque |
|---|---|---|---|
| 0.1 | claude.ai | | |
| 0.1 | Gemini | | |

## Ce qui mérite une correction immédiate

Par ordre de gravité, ce qui doit faire remonter un ticket dans `ROADMAP.md` :

1. Une règle inventée ou une citation introuvable (`sources/<id>/NN-slug.md` n'existe pas ou ne contient pas la règle).
2. Un jeu de date faux (AC/SC exigés en 2027, ou 2 h sportives exigées en 2026).
3. Une hypothèse muette (jeu de date choisi sans le dire), ou un sommaire / une annexe reproché comme absent.
4. Un nom de personne dans la sortie.
5. Un niveau de retour non respecté (avis trop long, revue sans tableau).

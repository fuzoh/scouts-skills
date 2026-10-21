---
slug: activite-js
titre: Activité J+S (AC / SC jusqu'en 2026 ; activité J+S dès 2027)
signaux: [fiche d'activité, AC, SC, activité de camp, sport de camp, bloc de programme, descriptif d'activité, déclaration, décla, canevas AC, canevas SC, activité de remplacement, variante mauvais temps, part sportive, forme caractéristique, randonnée, raid, AA, AdA, VC, AS]
role: [responsable, coach-js, formateur, expert-js]
verbes: [corriger, concevoir, expliquer]
parametres:
  - {nom: date du camp, obligatoire: true}
  - {nom: branche, obligatoire: false}
  - {nom: type 2026 (AC/SC) ou activité J+S 2027, obligatoire: false}
  - {nom: activité sportive ou non, obligatoire: false}
  - {nom: randonnée oui/non, obligatoire: false}
canevas: [cudesch-modele-bloc-ac, cudesch-modele-bloc-sc, autre-canevas-ac-vierge, autre-canevas-sc-vierge, cudesch-planification-activite]
sources: [msds-hering-camps, js-module-directives-sdct, js-module-bases-sdct, js-module-planifier-activite-js, js-module-planifier-randonnee, msds-pv-conference-formation-2026, cudesch-securite, js-sdct-camp, msds-autorisation-de-camp, cudesch-cudeschin, msds-exigences-js-2027-camps, js-manuel-sport-de-camp-trekking, msds-le-cours, js-sdct-montagne, cudesch-calcul-temps-de-marche, js-aide-memoire-3x3-en-route, cudesch-programme, cudesch-planification-activite, cudesch-modele-bloc-ac, cudesch-modele-bloc-sc, autre-canevas-ac-vierge, autre-canevas-sc-vierge]
inclut: [concept-de-securite]   # la sécurité d'une randonnée (CdS, 3x3, matrice) et les activités des domaines de sécurité relèvent de concept-de-securite ; ici seulement ce que la fiche doit contenir
statut: valide
relu_le: 2026-10-21
---
Périmètre : la fiche d'une activité du programme détaillé d'un camp. Les activités non déclarées J+S (AA = AdA = VC ; une AS est un type d'AA) (mainteneur) sont relues avec les N communs (N1 à N5) et les Q de forme, sans critères J+S (voir Pièges) ; qu'elles soient écrites comme toute activité est officiel (`msds-hering-camps#05-d-programme-detaille`) (revue RL-11). Le référentiel exige la date du camp : sans elle, demander avant de juger (voir « Selon la date »).

## Non-négociables
Portée : [tous] = quelle que soit la date ; [2026] = camp jusqu'au 31.12.2026 ; [2027] = camp dès le 01.01.2027.

N1. [tous] Le déroulement de tous les blocs de programme est fixé par écrit, jeux et sport comme activités du thème — `msds-hering-camps#05-d-programme-detaille`
N2. [tous] Chaque bloc, repas, veillée et AA compris (mainteneur), donne : nom, jour, date et heure, lieu, fil rouge lié au thème, responsables, contenu et déroulement avec temps prévus, liste du matériel, variante en cas d'intempéries — `msds-hering-camps#05-d-programme-detaille`
N3. [tous] (N3 à N5 doublonnent volontairement `concept-de-securite`.) Une activité à caractère dangereux, ou à risque accru, a son concept de sécurité (« si nécessaire » selon la fiche) — `msds-hering-camps#05-d-programme-detaille` ; `cudesch-securite#23-concept-de-securite-specifique-aux-activites` ; `js-sdct-camp#11-programme-detaille-securite` ; `cudesch-securite#10-quelles-sont-ces-activites-a-caractere`
N4. [tous] Une randonnée (à pied ou à vélo) comporte : détail de carte topographique en couleur avec itinéraire, calcul du temps de marche, concept de sécurité de la randonnée, programme en cas de mauvais temps — `msds-hering-camps#05-d-programme-detaille`
N5. [tous] Une activité d'un domaine de sécurité (Montagne, Hiver, Eau) est conduite par des responsables reconnus pour ce domaine et lue par un expert J+S du domaine (détail : concept-de-securite) — `msds-hering-camps#05-d-programme-detaille`
N6. [2026] L'activité est déclarée AC ou SC dans le programme — `js-sdct-camp#10-programme-general`
N7. [2026] Une AC permet d'acquérir des connaissances et aptitudes nécessaires au sport de camp / trekking, avec participation active de tou·te·s, dans l'une des six thématiques d'AC — `msds-autorisation-de-camp#01-contenu` (check-list C, « pense-bête » selon le formulaire ; cases à cocher perdues, voir Pièges) (mainteneur)
N8. [2026] Chaque bloc dure au moins 30 minutes — `msds-hering-camps#03-b-annonce-de-camp-programme-general` (« Dispositions de J+S jusqu'à fin 2026 ») ; `msds-autorisation-de-camp#01-contenu` ; `cudesch-cudeschin#03-activite-dans-le-sport-de-camp-trekking`
N9. [2027] L'activité J+S dure au moins 30 minutes — `js-module-directives-sdct#01-directives-sport-de-camp-trekking` ; `msds-exigences-js-2027-camps#01-contenu` ; `msds-hering-camps#03-b-annonce-de-camp-programme-general` (« dès janvier 2027 ») — et figure dans le programme avec un numéro — `msds-hering-camps#03-b-annonce-de-camp-programme-general` seulement
N10. [2027] Le temps d'activité sportive, compté à partir de 30 minutes, est indiqué séparément pour chaque activité J+S, par tranches de 15 minutes. Comptage : activité purement sportive, durée totale (petites pauses, explications, transitions, échauffement et retour au calme compris) ; activité mixte, parties sportives seulement ; moins de 30 min sportives dans l'activité, rien — `js-module-directives-sdct#01-directives-sport-de-camp-trekking` ; `msds-exigences-js-2027-camps#01-contenu` ; `js-manuel-sport-de-camp-trekking#11-coachs-js`
N11. [2027] L'activité propose un programme actif et axé sur le mouvement (à partir d'une intensité faible) : elle exige l'implication physique des participants ; des parties plus calmes sont admises si elles ont un lien direct avec les parties actives (croquis puis construction) — `js-module-directives-sdct#01-directives-sport-de-camp-trekking` ; `msds-exigences-js-2027-camps#01-contenu`
N12. [2027] L'activité est axée sur une ou plusieurs formes caractéristiques et comprend une ou plusieurs formes d'activité — `js-module-directives-sdct#01-directives-sport-de-camp-trekking` ; `msds-exigences-js-2027-camps#01-contenu` ; `js-manuel-sport-de-camp-trekking#15-formes-caracteristiques` ; libellés des six formes : Pièges
N13. [2027] L'activité s'adresse à tou·te·s les participant·e·s, est structurée de manière cohérente et adaptée à leurs besoins — `js-module-directives-sdct#01-directives-sport-de-camp-trekking` ; `msds-exigences-js-2027-camps#01-contenu` ; `js-manuel-sport-de-camp-trekking#11-coachs-js` (N11 à N13 : formules générales, à contrôler sur le déroulement, pas sur les mots) (mainteneur)
N14. [tous] Le coach et le responsable de camp prennent connaissance de tous les programmes détaillés (« doivent », dans la mesure où ils portent la responsabilité du programme) — `js-sdct-camp#11-programme-detaille-securite` (revue RL-15)

Hors fiche (à ne pas exiger d'une fiche seule) : quatre heures d'activités J+S par journée de camp dont deux sportives (2027), trois journées de camp, une activité itinérante et toutes les formes caractéristiques sur l'offre — `js-module-directives-sdct#01-directives-sport-de-camp-trekking` ; `msds-exigences-js-2027-camps#01-contenu`. Relèvent du programme de camp (référentiel `programme-camp`).

## Selon la date
Jeu 2027 par défaut ; jeu 2026 seulement si le camp est explicitement daté avant le 2027-01-01 (hypothèse annoncée, question seulement si la fiche est ambiguë). Un camp à cheval sur le 31.12.2026 : cas ignoré (mainteneur).

| point | jusqu'au 31.12.2026 | dès le 01.01.2027 | sources |
|---|---|---|---|
| statut de l'activité | AC ou SC | activité J+S, plus d'AC ni de SC | `js-sdct-camp#10-programme-general` ; `msds-exigences-js-2027-camps#01-contenu` |
| classement | domaine (six d'AC ; activités itinérantes, sports, jeux pour le SC) | formes caractéristiques (six) et formes d'activité | `msds-autorisation-de-camp#01-contenu` ; `js-manuel-sport-de-camp-trekking#15-formes-caracteristiques` |
| temps par journée | 4 h dont au plus 2 h d'AC ; au moins 2 h de SC | 4 h dont au moins 2 h d'activité sportive | `msds-hering-camps#03-b-annonce-de-camp-programme-general` ; `cudesch-cudeschin#03-activite-dans-le-sport-de-camp-trekking` (règles J+S 2026 relayées) ; `msds-autorisation-de-camp#01-contenu` (« au moins 2 h de SC ») |
| temps sportif | non indiqué par activité | indiqué par activité, tranches de 15 min | `msds-exigences-js-2027-camps#01-contenu` |
| bloc minimal | 30 min | 30 min, numéroté, matin / après-midi / soir (deux périodes) | `msds-hering-camps#03-b-annonce-de-camp-programme-general` ; `cudesch-cudeschin#03-activite-dans-le-sport-de-camp-trekking` (2026) |
| référence de relecture | check-lists A, B, C de l'autorisation de camp (valable jusqu'au 31.12.2026) | exigences 2027 et manuel 2026 ; autorisation 2027 non ingérée : critères 2026 gardés, à revérifier à son ingestion (mainteneur) | `msds-autorisation-de-camp#01-contenu` |
| modèles vierges | `cudesch-modele-bloc-*` (2018), `autre-canevas-*` | aucun modèle officiel ingéré : traduire, ne jamais exiger le vocabulaire d'un modèle (domaine, but) (mainteneur) | (terrain) |

Le manuel Sport de camp / Trekking (version 2026) porte le jeu 2027 ; son chapitre « Activités J+S » est vide dans l'extraction (`js-manuel-sport-de-camp-trekking#10-activites-js`), lire `#11-coachs-js`. `js-sdct-camp` (2014) reste la référence du jeu 2026. Pour une fiche 2026, un correcteur peut recommander la lecture 2027 (formes caractéristiques, part sportive) sans l'exiger.

## Critères de qualité
Q1. Les objectifs d'apprentissage sont prioritaires, peu nombreux, atteignables par tout le groupe tout en restant un défi (différenciés si besoin) — `js-manuel-sport-de-camp-trekking#23-objectifs-et-structure`
Q2. L'activité est adaptée à l'âge et permet d'atteindre l'objectif — `msds-exigences-js-2027-camps#01-contenu` ; `msds-autorisation-de-camp#01-contenu` (check-list B)
Q3. Le fil rouge est vécu dans l'activité, pas seulement nommé — `msds-hering-camps#05-d-programme-detaille` (la source exige la rubrique ; « vécu, pas seulement nommé » en plus) (mainteneur) (revue AC-06)
Q4. Structure en introduction, partie principale, retour au calme « si possible », adaptable à la situation ; les éléments sont coordonnés (structure, objectifs ou forme visée, contenus, sécurité, matériel) — `js-manuel-sport-de-camp-trekking#25-concevoir-une-activite`. Dans une partie importante ou difficile : la placer tôt (même source). La durée de chaque partie dépend du temps disponible, de l'âge et de la composition du groupe — `js-module-planifier-activite-js#01-planifier-une-bonne-activite-j-s`. En appui : introduction, partie principale et conclusion, avec un point culminant ; buts réalisables et aussi concrets que possible — `cudesch-cudeschin#01-planifier-une-activite`.
Q5. L'intensité est pensée sur l'activité (courbe d'intensité) : les parties s'identifient à la lecture sans devoir apparaître à la lettre — `msds-le-cours#05-contenus-de-formation` ; `js-sdct-camp#10-programme-general` (« un œil sur l'intensité ») ; pas d'exigence sur la fiche (revue SC-01, SC-02)
Q6. Une activité déclarée sportive (2027) est d'intensité modérée (moyenne) à très soutenue, les fréquences cardiaque et respiratoire augmentent ; excursion ou randonnée, danse : oui ; bricolage, montage de tente, construction d'un bivouac : non — `msds-exigences-js-2027-camps#01-contenu` ; `js-module-directives-sdct#01-directives-sport-de-camp-trekking`. Une activité peut être active (N11) sans être sportive : construire un bivouac en petits groupes (verdict « actif » des cartes du module, consigné dans les notes de la source `js-module-directives-sdct`, absent de la section)
Q7. La partie non sportive fait apprendre quelque chose ; « rien faire » ou faire sans but n'est pas une AC (2026) — `msds-autorisation-de-camp#01-contenu` ; en 2027 elle reste active et axée sur le mouvement — `msds-exigences-js-2027-camps#01-contenu`
Q8. Le programme est assez précis pour qu'un autre responsable puisse animer l'activité — `js-sdct-camp#11-programme-detaille-securite` ; les jeux et mouvements très connus peuvent n'être que nommés (revue SC-04)
Q9. Le fil de la planification est visible : qui, pourquoi, en quoi, comment, où, quand, avec quoi, dans quelles conditions (règles, sécurité, variante météo) — `js-manuel-sport-de-camp-trekking#24-planifier-activites`
Q10. Sécurité dans la fiche (toute activité J+S demande une réflexion de sécurité : de simples mesures ou un concept détaillé selon l'activité — `js-module-planifier-activite-js#01-planifier-une-bonne-activite-j-s`) : mini-identification des risques propres à l'activité, directement dans la fiche si ce sont des risques simples, un CdS joint si nécessaire, sans redire le CdS global ; une mesure par risque identifié, des mesures générales pouvant couvrir plusieurs risques ; pas de « roman » — `cudesch-securite#23-concept-de-securite-specifique-aux-activites` (forme libre, réflexions dans le descriptif) ; `cudesch-securite#22-quest-ce-quun-concept-de-securite` ; `msds-hering-camps#05-d-programme-detaille` ; « une mesure par risque » (revue AC-12, RL-04)
Q11. Critère de décision météo explicite : à partir de quand, alternative (source) ; qui décide (mainteneur) — `cudesch-securite#23-concept-de-securite-specifique-aux-activites`
Q12. Le matériel dangereux a une règle d'usage (qui utilise quels outils, où ils sont stockés) — `cudesch-securite#29-concept-de-securite-pour-un-camp`
Q13. Une personne est nommée par tâche (rubrique responsables, source) et par ligne de matériel (terrain) — `msds-hering-camps#05-d-programme-detaille`
Q14. Randonnée, ce que la fiche contient (la sécurité : concept-de-securite) :
- points de fuite (échappatoires), points de demi-tour, point de non-retour, passages clés repérés et reconnus — `cudesch-securite#11-randonnees` (sortie, demi-tour, reconnaissance) ; `cudesch-securite#28-exemple-concept-de-securite-randonnee` (passages clés) ; vocabulaire « point de fuite », « point de non-retour » (mainteneur). Les sept points clés J+S à placer sur la carte : passages à risque, passages difficiles, points de non-retour, zones de pause ou de ravitaillement, points remarquables, transitions montée / descente, échappatoires — `js-module-planifier-randonnee#01-planifier-une-randonnee`
- temps de marche en kilomètres-effort : 1 kme = 1 km à plat = 100 m de montée = 150 m de descente en terrain raide (dès 20 m de descente par 100 m) ; temps d'un tronçon = kme entre deux points clés ÷ facteur de vitesse (kme par heure sans pause), pauses ajoutées ; les tronçons permettent de comparer temps effectif et temps calculé en route — `js-module-planifier-randonnee#01-planifier-une-randonnee`
- facteur adapté : enfants, groupes non entraînés ou grands, 2 à 4 kme/h avec bagages et 3 à 5 sans ; jeunes, groupes entraînés ou petits, 3 à 5 avec bagages et 4 à 6 sans (valeurs indicatives hors pauses) — `js-sdct-montagne#05-planification-itineraire` p.16 ; mêmes fourchettes dans le module J+S « Planifier une randonnée » (valeurs relevées dans les notes de la source `js-module-planifier-randonnee`, perdues dans la section). Les points du cudesch (4 / 5 avec bagages, 5 / 6 sans) sont les bornes hautes de ces fourchettes — `cudesch-calcul-temps-de-marche#04-instruction`. Ajouter pauses et marge ; profil de marche joint — `cudesch-calcul-temps-de-marche#02-profil`. [non officiel] Pour planifier, partir du bas de la fourchette adaptée (enfants avec bagages : 2 kme/h), puis ajuster au groupe et au terrain, y compris à la baisse.
- qui ouvre et ferme la marche — `js-aide-memoire-3x3-en-route#03-securite-nuitee` ; `cudesch-securite#11-randonnees`
- itinéraire reconnu avant l'activité ; planification selon le 3x3 : exigé (mainteneur) — `msds-autorisation-de-camp#01-contenu` (check-list C) ; `js-aide-memoire-3x3-en-route#01-grille-3x3` ; reconnaissance recommandée pour toute randonnée, indispensable dans les Alpes, les Préalpes, le Jura et à l'étranger — `js-module-planifier-randonnee#01-planifier-une-randonnee`
- un moyen d'orientation non électronique toujours sur soi, de préférence une grande carte papier — `js-module-planifier-randonnee#01-planifier-une-randonnee`
- allure de la personne la plus lente (on peut parler en marchant), départ tranquille, pauses plus courtes et plus fréquentes avec des enfants, avant un gros effort — `js-module-planifier-randonnee#01-planifier-une-randonnee`
Q15. Chaque activité est basée sur l'une des huit méthodes et promeut l'une des cinq relations (Profil du scoutisme) : attente MSdS pour un camp scout, pas exigence J+S ; au niveau du camp, prendre en compte les huit méthodes et les cinq relations vaut « toutes les formes caractéristiques » (`programme-camp` N20) — `msds-exigences-js-2027-camps#01-contenu` (encadrés marginaux)
Q16. La planification détaillée par écrit a réfléchi huit points : buts, fondements du scoutisme (relations, méthodes, thème), déroulement, responsabilités, sécurité, « temps morts », information, évaluation ; l'information aux participants (date, lieu et heures, matériel, habits, contact) est donnée au plus tard trois jours avant l'activité — `cudesch-programme#09-l-activite` (écrit pour l'activité d'unité ; en camp, l'information vaut pour la maîtrise et les participants concernés, le délai est indicatif) (mainteneur)
Q17. [2026] La fiche indique quel élément J+S l'activité vise (domaine d'AC ou, pour le SC, type d'activité) — `js-manuel-sport-de-camp-trekking#25-concevoir-une-activite` ; `js-manuel-sport-de-camp-trekking#15-formes-caracteristiques` (la source le recommande sans l'exiger : critère de qualité, pas non-négociable ; en 2027 la forme caractéristique est exigée par N12) (mainteneur, 2026-10-18)
Q18. [2027] Le cycle de planification J+S est suivi : analyser le groupe et le cadre ; déduire les objectifs de l'analyse, des formes caractéristiques et des objectifs de J+S ; planification détaillée (contenus, méthodes et formes d'activité adaptés aux objectifs et au groupe, intensité suffisante, sécurité, structure en trois parties) ; réalisation avec des ajustements prévus pour les situations typiques (groupe fatigué, forte chaleur, retard) ; évaluation qui part des objectifs, recueille des retours et nourrit l'analyse suivante — `js-module-planifier-activite-js#01-planifier-une-bonne-activite-j-s`
Q19. [2027] La planification détaillée est écrite selon les directives en vigueur et soumise au coach J+S pour approbation (voir aussi N14) — `js-module-planifier-activite-js#01-planifier-une-bonne-activite-j-s`
Q20. [2027] Les formes d'activité (exercices, jeux, ateliers) sont choisies pour développer des facteurs de développement (aptitudes physiques, mentales, sociales) qui rapprochent de la forme caractéristique visée ; les longs temps morts sont transformés pour que tout le monde reste en mouvement — `js-module-bases-sdct#01-bases-du-sport-de-camp-trekking` ; `js-module-directives-sdct#01-directives-sport-de-camp-trekking`

## Critères non officiels
Jamais non-négociables. Origine : `docs/revue-criteres-cantonaux.md` (G, décision du mainteneur), terrain, trame cantonale.
[non officiel] Les infos de la fiche (date, heure, lieu, numéro) concordent avec le picasso et le programme de camp (origine : revue AC-01, RL-17)
[non officiel] Le nombre de participants est indiqué ; l'âge et la taille du groupe aident (origine : revue AC-03 ; trame cantonale)
[non officiel] Le remplacement est une activité de même type, avec un temps de sport équivalent, ou au minimum assez de temps de sport pour tenir la journée dans les règles J+S (origine : revue AC-10, SC-10)
[non officiel] Variante et remplacement sont distingués dans la fiche (origine : revue AC-11)
[non officiel] Les échauffements sont adaptés à l'activité et variés sur l'ensemble du camp, comme les activités, sports et formes sportives (origine : revue SC-06)
[non officiel] Le timing est réaliste : les parties peuvent être faites ; des pauses sont nécessaires, mais pas au point de faire retomber trop le rythme (origine : revue SC-07, sans chiffres)
[non officiel] Les règles d'un jeu peu connu sont expliquées (origine : revue SC-09)
[non officiel] La fiche est complète ; certains éléments ne sont pas strictement obligatoires (origine : revue RL-01)
[non officiel] Rubriques de contexte (lien au thème, qui, références, évaluation) conseillées, pas obligatoires ; très variables selon les cantons (origine : revue AC-15)
[non officiel] Un CdS pour la cuisine existe, souvent intégré au CdS global du camp (origine : revue RL-10)
[non officiel] La fiche finale ne contient plus de commentaires de relecteur ; les renvois existent et titre, type et numéro concordent (origine : revue RL-13, RL-14)
[non officiel] Randonnée : les points de courbes de niveau sont placés pour qu'aucune cuvette ni bosse ne manque au profil, « au mieux » (origine : revue TK-01)
[non officiel] Randonnée : points numérotés sur la carte et reportés dans le profil ; coordonnées ou lieux-dits univoques sur la carte utilisée (origine : revue TK-02)
[non officiel] Rôle de chaque responsable ; la fiche permet de reprendre l'activité « au pied levé » (origine : terrain)
[non officiel] Objectif d'apprentissage mesurable, au moins un par activité ; lien au thème en une phrase (trame cantonale, non officielle ; nuance de Q1)
[non officiel] Pour la boisson, donner un ordre de grandeur plutôt que « de l'eau » : au moins 1,5 litre pour une marche selon le 3x3 de 2014 (`js-aide-memoire-3x3-en-route#03-securite-nuitee`) ; cudesch dit seulement « suffisamment à boire » (origine : revue RL-07, G)
[non officiel] Rubriques de la trame cantonale au-delà de Q10 et Q11 : renvoi explicite au CdS spécifique, remplacement prévu pour chaque activité, remarques et auto-évaluation tournées vers qui reprend la fiche (trame cantonale, non officielle)

## Questions à poser avant de juger
1. Date du camp (obligatoire) : jusqu'au 31.12.2026 ou dès le 01.01.2027 ? Elle fixe le jeu de critères.
2. Branche et âge des participants.
3. Camp 2026 : activité AC ou SC ? Camp 2027 : activité J+S ? Activité sportive ou non ? Ou activité non déclarée J+S (AA, AdA, VC, AS) ?
4. Randonnée (à pied ou à vélo) : oui ou non ? Si oui, carte, profil et calcul du temps de marche sont-ils joints ?
5. Annexes et CdS joint : les demander avant de conclure à l'absence d'une exigence (un CdS complet peut être en annexe).
6. Canevas utilisé (modèle de bloc, canevas de groupe, trame cantonale) : le reconnaître, ne pas l'exiger.

## Pièges
- Cases à cocher (domaine, « concept de sécurité oui/non », thématiques d'AC) perdues à la conversion docx et pdf : ne jamais conclure qu'une case n'est pas cochée. L'autorisation de camp est elle-même `fidelity: partial`.
- Quatre notions distinctes. Variante : même activité adaptée (règles, forme, météo). Remplacement : autre activité interchangeable, du même type, temps de sport équivalent. Critère d'annulation : condition qui déclenche variante ou remplacement (météo, matériel, accident). Échappatoire (point de sortie) : raccourci d'une randonnée, pas une activité de remplacement. Aucune fiche de terrain n'a de rubrique « remplacement » : la variante en tient lieu, sans durée ni matériel.
- Un remplacement par une activité sans temps de sport peut faire sortir la journée des règles J+S : le signaler, pas le refuser d'office.
- Les six formes caractéristiques (libellés du module J+S « Bases ») : utiliser efficacement les techniques de vie en plein air et de construction de camp ; pratiquer des activités itinérantes de manière sûre et prévoyante ; participer avec créativité à la conception de jeux et d'activités sportives variées ; prendre conscience de ses propres besoins et idées et les faire valoir consciemment ; renforcer la cohésion du groupe avec bienveillance ; adopter une attitude respectueuse envers la nature et l'environnement — `js-module-bases-sdct#01-bases-du-sport-de-camp-trekking`. Le manuel écrit « des techniques » et, pour la sixième, « interagir de manière respectueuse avec son environnement » (`js-manuel-sport-de-camp-trekking#15-formes-caracteristiques`), le PV de la ConfFor « … avec la nature et l'environnement » : même forme, ne pas corriger un libellé.
- Forme caractéristique sur la fiche 2027 (N12) : le PV de la ConfFor 2026 dit qu'il n'est « pas nécessaire d'indiquer la forme caractéristique visée » si le descriptif porte la durée d'activité physique, la relation et la méthode (`msds-pv-conference-formation-2026#03-conception-exigences-manuel` p.5). L'aide-mémoire MSdS 2027 et le module J+S exigent une activité axée sur une forme : la demander quand même (mainteneur), la correction tient en une ligne et la relation et la méthode aident à la choisir.
- Une activité qui ne peut pas devenir active n'est pas une activité J+S, et ce n'est pas un défaut : la journée a de la place pour des activités non J+S — `js-module-directives-sdct#01-directives-sport-de-camp-trekking`. Ne pas la refuser, la sortir du compte J+S.
- Comptage du temps sportif (N10), exemples J+S : tournoi de 2 h avec explications, pauses et transitions = 2 h ; jeu de piste de 3 h (6 × 15 min de marche, 6 × 15 min de postes) = 1 h 30 ; 90 min de dynamique de groupe dont 45 min de jeu sportif = 45 min — `js-module-directives-sdct#01-directives-sport-de-camp-trekking`. Exemple MSdS : 4 h de construction d'une tour = activité J+S active, 3 h sportives, l'heure de planification non comptée (mail MSdS aux coachs, octobre 2026, non ingéré).
- Relation et méthode ne sont pas des domaines J+S. Huit méthodes (profil), pas sept : l'ancienne liste de sept subsiste dans des modèles. But n'est pas objectif.
- AA, AdA, VC : activités du camp non déclarées J+S ; AS : activité spirituelle, un type d'AA (CDF est une spécificité locale, à lire comme AS). Les relire sans N6 à N13 ni formes caractéristiques ; ne pas exiger de CdS J+S. PF = point fixe (séance de maîtrise), pas une activité.
- Une fiche creuse peut avoir un CdS complet en annexe : demander les annexes avant de juger.
- Le vocabulaire 2027 n'apparaît dans aucune fiche 2026 ; en 2027, la rubrique « domaine » des modèles perd son sens. Aucun modèle ingéré n'a le champ part sportive : le proposer, sans condamner un modèle ancien.
- Ne pas exiger MeT / PP / RàC à la lettre, en particulier pour une randonnée : la structure en trois parties s'adapte (`js-manuel-sport-de-camp-trekking#25-concevoir-une-activite`). Ces abréviations sont locales.
- Ne pas confondre `autre-canevas-*` (modèle de groupe, exemple) et `cudesch-modele-bloc-*` (modèle 2018) : ni l'un ni l'autre n'est une exigence. Les canevas cantonaux ne sont pas ingérés : citer (trame cantonale, non officielle).
- La fiche ne redit pas le CdS global (revue AC-12) et le CdS ne remplace pas la fiche.
- La grille `cudesch-planification-activite#01-contenu` (2018) n'a ni rubrique sécurité ni météo : format reconnu, pas une raison d'omettre N2 à N4.

## Trame de conception
Rubriques d'une fiche complète, dans l'ordre de rédaction. Elles viennent des modèles officiels (`cudesch-modele-bloc-ac`, `cudesch-modele-bloc-sc`, copies `autre-canevas-ac-vierge`, `autre-canevas-sc-vierge`), de N2 et de `js-manuel-sport-de-camp-trekking#24-planifier-activites`. Bases officielles 2018+ à côté des modèles de bloc : `cudesch-programme#09-l-activite` (huit points de planification) et `cudesch-planification-activite#01-contenu` (grille vierge). Elles sont complétées par la trame cantonale (non officielle, marquée *) ; le verbe « concevoir » propose la trame complète (mainteneur).
1. Identification : numéro et titre (type et rang dans le jour ; en 2027, activité J+S numérotée), date, horaires, lieu, camp et unité.
2. Cadre : date du camp, branche, âge et taille du groupe*, nombre de responsables*, responsable de l'activité.
3. Orientation : 2026 domaine (AC) ou activités itinérantes / sports / jeux (SC) ; 2027 forme(s) caractéristique(s) et forme(s) d'activité ; relation et méthode*.
4. Objectifs : « éléments à apprendre et à vivre » (AC) ou buts (SC) ; 2027 : déduits de l'analyse du groupe et des formes caractéristiques (Q18) ; objectifs atteignables, mesurables*.
5. Fil rouge / lien au thème.
6. Déroulement : parties avec horaire, durée et responsable ; échauffement décrit ; courbe d'intensité ; 2027 part sportive en tranches de 15 min.
7. Matériel, avec responsable ; provenance*.
8. Sécurité : risques simples et mesures dans la fiche ; case « CdS séparé : oui / non » (modèles) ; renvoi au CdS d'activité ou de randonnée.
9. Variante en cas de mauvais temps, avec critère de décision ; ajustements prévus (groupe fatigué, chaleur, retard) (Q18).
10. Critères d'annulation* et activité de remplacement* (même type, temps de sport équivalent).
11. Randonnée seulement : carte, profil, temps de marche, CdS de randonnée, programme mauvais temps (N4).
12. Évaluation à partir des objectifs (Q18) ; remarques, auto-évaluation*.
Vérifier ensuite la cohérence avec le picasso, relire à la place du rédacteur, retirer les commentaires de relecture.

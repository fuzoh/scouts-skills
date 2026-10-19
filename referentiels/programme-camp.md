---
slug: programme-camp
titre: Programme de camp (picasso, programme général, programme détaillé)
signaux: [picasso, programme de camp, programme général, programme détaillé, grille horaire, dossier de camp, horaire du camp, journée type, point fixe, PF, responsable de jour, blocs de programme, camp d'été, camp d'automne, quota d'encadrement]
role: [responsable, coach-js, formateur]
verbes: [corriger, concevoir, expliquer]
parametres:
  - {nom: date du camp, obligatoire: true}
  - {nom: forme de camp, obligatoire: false}
  - {nom: branches et nombre de programmes, obligatoire: false}
  - {nom: camp J+S ou non, obligatoire: false}
  - {nom: effectifs, obligatoire: false}
  - {nom: durée, obligatoire: false}
canevas: [js-exemple-programme-camp-ete, js-modele-prog-general-sport-jeunes, js-modele-prog-general-sport-enfants, js-modele-prog-general-enfants-jeunes]
sources: [msds-hering-camps, msds-essentiel-msds-js-2027, msds-essentiel-msds-js-2026, js-sdct-camp, msds-reglement-de-camp, msds-autorisation-de-camp, msds-exigences-js-2027-camps, js-guide-offres-sct, js-manuel-sport-de-camp-trekking, js-exemple-programme-camp-ete, js-modele-prog-general-sport-jeunes, js-modele-prog-general-sport-enfants, js-modele-prog-general-enfants-jeunes, cudesch-camp-liste-delais, cudesch-camp-budget, cudesch-camp-reco-sous-tentes, cudesch-camp-reco-sous-toit, cudesch-camp-bail-place-tentes, cudesch-camp-liste-equipement, cudesch-camp-infos-urgence, cudesch-securite, cudesch-cudeschin, cudesch-programme, cudesch-etre-responsable, cudesch-branche-castors, cudesch-branche-louveteaux, cudesch-branche-eclais, cudesch-branche-picos, cudesch-branche-route]
inclut: [activite-js, concept-de-securite]
statut: valide
relu_le: 2026-10-18
---
Livrable principal : le programme de camp, c'est-à-dire le picasso (grille jour × heure) et les fiches de blocs qui le détaillent. Les autres livrables de camp sont en annexe, sans développement. La fiche d'une activité (modèles de bloc AC et SC compris) se corrige avec `activite-js` ; le concept de sécurité avec `concept-de-securite`. Le « programme général » officiel est la vue d'ensemble ; le « programme détaillé » est le dossier qui le complète ; le picasso tient lieu de programme général (terrain).

## Non-négociables
Portées : `[tous]` camp annoncé J+S ou non ; `[js]` camp annoncé J+S, quelle que soit la date ; `[2027]` camp J+S dès 2027-01-01 ; `[après]` délais de clôture, après le camp. Camp non J+S : seuls les N `[tous]` (N1 à N12) s'appliquent ; N22 vaut aussi pour un camp non J+S annoncé dans la MiData (mainteneur).
N1. [tous] Le programme général indique : thème, responsable de camp, organisateur, coach, lieu et nom du gîte ou de la place, dates, genre de camp, jour-date-responsable de la journée, nom de chaque activité et de son responsable, heures d'arrivée et de départ — `msds-hering-camps#03-b-annonce-de-camp-programme-general`
N2. [tous] Le responsable de camp transmet le programme général avec l'annonce au RG et au coach, qui donne un retour — `msds-hering-camps#03-b-annonce-de-camp-programme-general`
N3. [tous] Pour tout camp dès trois jours, J+S ou non, l'annonce passe par la MiData. Deux échéances successives : le responsable de camp complète l'annonce et remet le programme général au RG et au coach **7 semaines** avant le début ; le coach transmet l'annonce au MSdS **6 semaines** avant — `msds-reglement-de-camp#03-encadrement-autorisation` (6 semaines, coach) ; `cudesch-camp-liste-delais#01-contenu` (7 semaines, responsable) ; confirmé par la Sardine, J-49 / J-43 (calendrier de la Sardine en ligne, non ingéré). « Dès trois jours » : choix prudent retenu par le mainteneur. Le règlement s’applique dès trois jours (`msds-reglement-de-camp#01-exigences-camp`), mais sa clause d’annonce et la Sardine écrivent « plus de 3 jours » ; le formulaire d’autorisation écrit « dès 3 jours » (`msds-autorisation-de-camp#01-contenu`)
N4. [tous] Le dossier de camp est remis au RG et au coach au moins 3 semaines avant le début — `msds-reglement-de-camp#03-encadrement-autorisation` ; `msds-hering-camps#05-d-programme-detaille`. La Sardine place le dossier à 4 semaines (J-28) et l'autorisation à 3 semaines (J-21) : retenir 4 semaines comme date prudente
N5. [tous] Le dossier contient : programme général, thème et fil rouge, description des blocs, concept de sécurité du camp, règles du camp, arrangements d'équipe (tâches, responsables du jour), liste des participants ; pour une randonnée : temps de marche, cartes, concept de sécurité, programme de mauvais temps — `msds-hering-camps#05-d-programme-detaille`
N6. [tous] Chaque bloc est décrit par écrit : nom, jour-date-heure, lieu, fil rouge, responsables, contenu et déroulement chronométré, matériel, variante d'intempéries, concept de sécurité de l'activité si nécessaire — `msds-hering-camps#05-d-programme-detaille`
N7. [tous] Jeux, sport et activités du thème sont tous décrits, pas seulement les activités J+S — `msds-hering-camps#05-d-programme-detaille`
N8. [tous] Un concept de sécurité existe pour le camp et pour chaque activité à caractère dangereux (J+S ou non) — `msds-reglement-de-camp#01-exigences-camp` (concept du camp, qui contient les activités dangereuses) ; `msds-hering-camps#05-d-programme-detaille` et `msds-autorisation-de-camp#01-contenu` (check-list A : un concept pour le camp et pour chaque activité dangereuse)
N9. [tous] Les activités d'un domaine de sécurité (montagne, hiver, eau) sont lues et approuvées par un·e expert·e J+S du domaine, qui le confirme par sa signature ; le coach signe ensuite l'autorisation après avis de l'expert·e (mainteneur) — `msds-reglement-de-camp#03-encadrement-autorisation` (signature de l'expert) ; `msds-hering-camps#05-d-programme-detaille` (signature supplémentaire de l'expert) ; `msds-autorisation-de-camp#01-contenu` (le coach signe après consultation)
N10. [tous] Le programme répond aux exigences de la branche et aux fondements du scoutisme ; camp interbranches : programme en grande partie propre à chaque branche — `msds-reglement-de-camp#01-exigences-camp` ; `msds-reglement-de-camp#03-encadrement-autorisation`. Repères des livres de branche : « Selon la branche » (recommandations)
N11. [tous] Camp avec filles et garçons : maîtrise composée de femmes et d'hommes, réflexion sur hébergement, rôles, tâches, santé — `msds-reglement-de-camp#01-exigences-camp` (le règlement dit « camp mixte » ; dans le vocabulaire des équipes, « mixte » désigne un camp à plusieurs groupes d'âge, voir [non officiel] PC-13 : ne pas employer le mot ici) ; `cudesch-etre-responsable#25-egaux-et-equitables` (check-list unités mixtes : encadrement mixte, tentes ou dortoirs séparés, tâches réparties sans stéréotype)
N12. [tous] Le camp ne peut avoir lieu qu'avec l'autorisation signée du RG et du coach (éventuellement avec compléments, à valider avant le camp) — `msds-reglement-de-camp#03-encadrement-autorisation` ; `msds-hering-camps#07-f-autorisation-de-camp`
N13. [js] Au moins 12 participants en âge J+S ; jusqu’à fin 2026, selon les groupes cibles enfants/jeunes et les reconnaissances correspondantes ; dès 2027, un même camp et une seule reconnaissance couvrent les 5 à 20 ans. Au moins deux moniteurs J+S SdC/T dont un avec le complément « chef de camp » en 2026, « Responsable de camp » dès 2027 — `msds-essentiel-msds-js-2027#03-fusion-groupes-cibles` (2027 : « reste fixé à 12 », taille de groupe pour les subventions inchangée à 16+16+16) ; `js-guide-offres-sct#01-contenu` (guide 2023)
N14. [js] Encadrement : jusqu'à 36 participants pour deux moniteurs ; dès 37 participants, un moniteur habilité de plus par tranche de 12 supplémentaires ; sous-groupe d'activité J+S : un moniteur par sous-groupe — `js-guide-offres-sct#01-contenu` (guide 2023, qui cite l'OPESp art. 13 al. 2 et annexe 2)
N15. [js] Au moins quatre jours consécutifs (trois si l'offre contient un camp de quatre jours ; « au moins trois journées » de l'aide-mémoire 2027 dit la même chose) ; chaque jour de camp comporte au moins 4 h d'activités J+S, blocs d'au moins 30 min. Vaut pour les jeux 2026 et 2027 (mainteneur) — `js-guide-offres-sct#01-contenu` ; `msds-hering-camps#03-b-annonce-de-camp-programme-general`
N16. [js] Les jours d'arrivée et de départ comptent ensemble pour un jour de camp s'ils totalisent 4 h d'activités J+S ; jeux 2026 et 2027 — `msds-hering-camps#03-b-annonce-de-camp-programme-general`
N17. [2027] Chaque jour : au moins 4 h d'activités J+S, dont au moins 2 h d'activité sportive (comptée dès 30 min, indiquée séparément pour chaque activité J+S par tranches de 15 min) — `msds-exigences-js-2027-camps#01-contenu` ; `msds-hering-camps#03-b-annonce-de-camp-programme-general`
N18. [2027] Les blocs d'activité J+S figurent clairement dans le programme avec un numéro — `msds-hering-camps#03-b-annonce-de-camp-programme-general`
N19. [2027] Les activités J+S s'adressent à tou·te·s, durent 30 min au moins, sont réparties sur au moins deux périodes (matin, après-midi, soir), sont actives et axées sur le mouvement, axées sur une ou plusieurs formes caractéristiques, cohérentes et adaptées aux besoins — `msds-exigences-js-2027-camps#01-contenu`
N20. [2027] Offre J+S : au moins un camp de quatre jours, au moins une activité itinérante, toutes les formes caractéristiques traitées sur l'ensemble de l'offre (un camp scout qui prend en compte les huit méthodes et les cinq relations remplit cette exigence, encadré de l'aide-mémoire) — `msds-exigences-js-2027-camps#01-contenu` ; camp de plus de 4 jours : au plus un jour sans activité J+S — `msds-hering-camps#03-b-annonce-de-camp-programme-general` (absent de l'aide-mémoire MSdS ; aussi dans `js-guide-offres-sct#01-contenu`). N17 à N20 reposent sur l'aide-mémoire MSdS de septembre 2026 et la Sardine ; le guide des offres OFSPO 2027 n'est pas ingéré (maintenus en N par le mainteneur)
N21. [après] Cartes nationales renvoyées à swisstopo au plus tard 3 jours après le camp — `msds-hering-camps#08-g-cloture-du-camp`
N22. [après] Participants et responsables ajustés dans la MiData, coach informé au plus tard 10 jours après — `msds-hering-camps#08-g-cloture-du-camp`
N23. [après] Offre J+S clôturée par le coach à la fin de l'année, au plus tard 30 jours après le dernier camp — `msds-hering-camps#09-h-cloture-de-l-offre-js`

## Selon la date
Jeu 2027 par défaut ; jeu 2026 seulement si le camp est explicitement daté avant le 2027-01-01 (hypothèse annoncée en une phrase, question seulement si le document est ambigu). Le programme se juge sur le jeu de la date du camp, pas de la date de la relecture. Camp à cheval sur le 2027-01-01 : cas ignoré (mainteneur). Le guide des offres OFSPO 2027 n'est pas ingéré.

| Point | Camp jusqu'au 2026-12-31 (jeu 2026) | Camp dès 2027-01-01 (jeu 2027) |
|---|---|---|
| Statut des activités | Chaque activité J+S est SC ou AC ; le programme l'indique — `js-sdct-camp#10-programme-general` | Plus d'AC ni de SC ni de domaines comme classement : activités J+S et part de sport de chacune (N17, N18) ; définitions : `js-manuel-sport-de-camp-trekking#15-formes-caracteristiques` |
| Temps par jour | 4 h d'activités J+S, dont au plus 2 h d'AC — `msds-hering-camps#03-b-annonce-de-camp-programme-general` ; `js-sdct-camp#10-programme-general` ; `cudesch-cudeschin#03-activite-dans-le-sport-de-camp-trekking` | 4 h d'activités J+S, dont au moins 2 h sportives, plus de plafond d'AC (N17) |
| Périodes | Journée en trois parties (repas de midi et du soir), 30 min d'activité de camp (AC) dans deux d'entre elles — mêmes sources que ci-dessus | Au moins deux périodes (matin, après-midi, soir), activités de 30 min au moins (N19) |
| Jour sans J+S | Au plus un, sans subside, dans un camp de plus de 4 jours | Au plus un jour sans activité J+S dans un camp de plus de 4 jours (N20) |
| Numérotation | Pas de numéro J+S exigé | Numéro pour chaque bloc J+S (N18) |
| Référence de relecture | Autorisation de camp MSdS valable jusqu'au 31.12.2026 — `msds-autorisation-de-camp#01-contenu` | Formulaire 2027 non ingéré : N12 et Q1, Q3-Q6, Q10, Q13-Q15 s'appuient sur les check-lists 2026, gardés pour 2027, à revérifier à l'ingestion (mainteneur) |
| Modèle de picasso | Modèles de bloc AC et SC : `activite-js` | `js-exemple-programme-camp-ete#01-contenu` (temps sportif par activité, numéros, légende J+S / programme de camp) |

Camp non J+S : le coach relit quand même le dossier, sans exiger les éléments J+S à la lettre (terrain, mainteneur).

## Critères de qualité
Q1. Le dossier contient le programme général (picasso) et celui-ci est discuté avec le coach — `msds-autorisation-de-camp#01-contenu` (check-list A) ; `js-sdct-camp#10-programme-general`. Les informations générales portées par le picasso (effectif, priorités, type de camp) relèvent de la trame cantonale, voir [non officiel]
Q2. Les points fixes de la journée (réveil, repas, début et fin de journée, séance des moniteurs, loisirs) sont posés d'abord ; « à la même heure chaque jour » est dit pour les enfants et peut varier selon la branche (mainteneur) — `js-sdct-camp#10-programme-general`
Q3. Programme adapté à l'âge, équilibré, varié, avec des moments de détente ; alternance dynamique et calme ; moments de recueillement possibles — `js-sdct-camp#10-programme-general` ; `msds-autorisation-de-camp#01-contenu` (check-list B)
Q4. Des points culminants répartis sur le camp ; un thème vécu comme fil rouge reliant les activités — `msds-autorisation-de-camp#01-contenu` (check-list B)
Q5. Huit méthodes et cinq relations trouvent leur place dans le programme (la check-list 2026 cite encore sept méthodes) — `msds-exigences-js-2027-camps#01-contenu` ; `msds-autorisation-de-camp#01-contenu` (check-list B)
Q6. Progression personnelle, Loi et Promesse, rituels : prévus au programme — `msds-autorisation-de-camp#01-contenu` (check-list B)
Q7. Un responsable du jour nommé chaque jour (rôle : séance des moniteurs, déroulement, réveil, encadrement du temps libre, extinction) ; responsable indiqué pour chaque activité — `js-sdct-camp#04-repartition-des-taches` ; `msds-hering-camps#03-b-annonce-de-camp-programme-general`
Q8. Programme de remplacement en cas de mauvais temps : activités tributaires de la météo repérées, au moins une activité en plein air conservée — `js-sdct-camp#10-programme-general`
Q9. Camp réunissant des participants d'âges très différents : activités différenciées, pas de programme « entre deux » — `js-sdct-camp#10-programme-general`
Q10. Des priorités de camp sont définies : trois au plus, une ou deux suffisent (mainteneur ; les sources disent « trois priorités » et « 3 objectifs de camp ») — `js-sdct-camp#08-programme-de-camp` ; `msds-autorisation-de-camp#01-contenu` (check-list C)
Q11. Participants associés aux décisions selon l'âge (parlement de camp, tâches, parties de programme) — `js-sdct-camp#08-programme-de-camp`
Q12. Répartition des tâches selon les aptitudes, les expérimentés soutenant les autres — `js-sdct-camp#11-programme-detaille-securite`
Q13. Parties les plus exigeantes, les moins captivantes, celles qui risquent de faire peur : identifiées avec la maîtrise — `msds-autorisation-de-camp#01-contenu` (check-list B)
Q14. Règles du camp avec conséquences claires, connues de tous ; charte de camp — `msds-autorisation-de-camp#01-contenu` (check-list A) ; `js-sdct-camp#16-regles-du-camp` ; `cudesch-securite#29-concept-de-securite-pour-un-camp`
Q15. La maîtrise connaît le scénario de crise cantonal et la helpline scoute — `msds-autorisation-de-camp#01-contenu` (check-list A)
Q16. Camp non J+S : les règles de sécurité J+S sont tout de même respectées — `msds-reglement-de-camp#01-exigences-camp`
Q17. Du temps libre : pas d'occupation 24 h sur 24, du temps libre avec un interlocuteur — `js-sdct-camp#10-programme-general`
Q18. Encadrement : le règlement fixe l'effectif selon participants, activités et branche, sans ratio ; prévoir plus que le minimum J+S (N14) — `msds-reglement-de-camp#02-maitrise-de-camp`
Q19. Le camp est planifié comme un grand événement : buts concrets définis en équipe, thème et fil rouge, rétroplanning par étapes avec secteurs et responsables écrits, contrôle de la qualité du programme (fondements, formes de mouvement) — `cudesch-programme#04-planifier`

## Critères non officiels
[non officiel] Chaque activité (J+S, AA, AS, repas, transport) porte un identifiant unique ; la forme de numérotation varie (jour.n, par type), l'unicité compte. Pour les blocs J+S dès 2027 : N18. (revue PC-12)
[non officiel] Une couleur par type d'activité et une légende : conseillé pour la lisibilité, pas obligatoire. (revue PC-11)
[non officiel] Plusieurs branches ou programmes : programmes séparés (un picasso par branche), ou colonnes ou couleurs qui montrent qui suit quel programme ; camp interbranches : programme en grande partie propre à chaque branche (officiel, N10). « Camp mixte » peut désigner plusieurs branches dans les équipes ; seule la catégorie J+S enfants + jeunes disparaît en 2027, pas les camps interbranches. Le règlement emploie encore « mixte » pour filles et garçons (N11). (revue PC-13)
[non officiel] Début et fin du camp : transports et rendez-vous inscrits ; traditions propres au groupe (raid, journée des familles, cérémonies) inscrites ; rituels, Loi et Promesse sont officiels (Q6). (revue PC-03, PC-04)
[non officiel] AA (autre activité, = AdA = VC, hors J+S) et AS (activité spirituelle) figurent au programme mais sans critères J+S ; elles ne comptent pas dans les 4 h J+S. Une AS est un type d'AA (mainteneur). Un espace de parole ou de partage prend souvent la forme d'une AA, AS comprise. (terrain ; revue FO-21)
[non officiel] PF = point fixe (mainteneur, pas « plage fixe ») : séance de maîtrise du soir, quotidienne ; aussi les moments fixes de la journée (réveil, repas) selon les groupes. À légender. (terrain ; officiel pour le principe des points fixes : Q2)
[non officiel] Charge répartie équitablement entre responsables, un expérimenté pouvant en prendre un peu plus : à favoriser, pas à imposer. (revue PC-16)
[non officiel] Moments « participant » pour la maîtrise (se détendre, partager) : recommandé, pas obligatoire. (revue PC-17)
[non officiel] Responsable de jour idéalement sans activité propre : pratique, pas toujours possible ; dire « responsable de jour ». (revue FO-12)
[non officiel] Un cahier des charges d'une page par poste (responsable de jour, infirmerie, matériel) : pratiqué par certains groupes. (revue FO-11 ; seules les tâches possibles du responsable du jour sont officielles : `js-sdct-camp#04-repartition-des-taches`)
[non officiel] Quota : la règle J+S est N13-N14 ; le « un responsable pour douze » du rapport de coach n'est officiel que pour le camp au bord de l'eau (un brevet SSS pour 12 participants, `js-sdct-camp#06-formes-de-camp`). On recommande en général plus de responsables que le minimum. (revue FO-10)
[non officiel] Circuit de relecture : chaque fiche a un auteur et un relecteur, avec un tableau d'état (ok, à revoir, à compléter) ; fréquent. (revue FO-01, FO-04 : l'autorisation officielle a trois états, N12)
[non officiel] Date de rendu des fiches fixée bien avant le camp, selon les délais de la sardine ; échéancier à deux colonnes (délai officiel, délai du coach plus tôt). (revue FO-02, FO-05)
[non officiel] Préparation de 6 à 10 mois (séances, éventuel week-end de préparation) ; pré-camp de montage souvent fait, pas obligatoire ; relecture des bilans précédents au démarrage. (revue FO-19, FO-20, FO-17)
[non officiel] Trame cantonale (non officielle) du picasso : jours en colonnes, demi-heures en lignes, informations générales (responsable de camp, RG, coach, genre, lieux, thème, effectif, informations J+S : type, jours J+S, jours de voyage, numéro d'offre), trois priorités rédigées, légende, abréviations. (terrain)

## Selon la branche
Pour N10 (« exigences de la branche ») : repères des livres de branche du cudesch, des recommandations (Q, jamais N). Sections qui portent des repères de programme de camp.
- Castors : pas de camp — `msds-reglement-de-camp#01-exigences-camp` ; repères de week-end seulement : nuitée facultative, lieu connu, « moins, c’est plus » (du samedi après-midi au petit-déjeuner du dimanche) — `cudesch-branche-castors#15-activites-speciales` ; attention limitée (environ 15 min), besoin de structure et d'autonomie — `cudesch-branche-castors#06-enfants`
- Louveteaux : activités de 3 à 4 h, camp d'une semaine en chalet, tente possible en camp de groupe ou cantonal, programme diversifié dans un thème captivant, crainte de l'éloignement — `cudesch-branche-louveteaux#08-organisation` ; aventures dans la nature à portée simple — `cudesch-branche-louveteaux#40-activites-dans-la-nature`
- Éclais : camp d'été de deux semaines sous tentes, thème et fil rouge, camps avec d'autres branches mais programme séparé, équilibre des relations et méthodes ; limites des activités de patrouille en camp (concept de sécurité) — `cudesch-branche-eclais#20-les-specificites-de-la-branche` ; moments, activités et activités de patrouille plus exigeantes dans le programme de camp — `cudesch-branche-eclais#21-la-particularite-des-activites-en`
- Picos : camp Picos organisé par l'Équipe, orienté vers un objectif, souvent itinérant, programme autonome, règles J+S et dossier d'entreprise — `cudesch-branche-picos#43-les-camps` ; activités détaillées et leur durée (exemple du « 15 heures Picos ») — `cudesch-branche-picos#44-les-activites-picos-en-detail`
- Route : projet, expédition, camps en clan, veillée Route (activités à planification complète portée par le clan) — `cudesch-branche-route#20-activites`

## Questions à poser avant de juger
1. Date du camp : avant ou dès le 2027-01-01 (jeu 2026 ou 2027) ? Obligatoire.
2. Camp annoncé J+S ou non ? Sinon, seuls les N `[tous]` s'appliquent.
3. Forme et lieu du camp : sous toit, sous tente, itinérant ; à l'étranger ?
4. Branches concernées et nombre de programmes (un picasso par branche ?).
5. Effectifs : participants et responsables (N13, N14).
6. Durée du camp (N15, N20).
7. Pièces jointes : picasso, programme général, programme détaillé, concept de sécurité. À demander avant de conclure à l'absence d'une pièce.

## Pièges
- 6 et 7 semaines ne se contredisent pas : 7 semaines pour le responsable de camp (programme général au RG et au coach), 6 semaines pour le coach (annonce au MSdS), N3. Le calendrier de la Sardine en ligne (non ingéré) calcule toutes les échéances depuis la date de début : y renvoyer plutôt que de recopier des délais. Les dossiers réels annoncent souvent plus tard (terrain).
- Quota 2027 (N14) : dès 2027 les groupes cibles fusionnent ; la taille de groupe donnant droit à subvention a été réanalysée et fixée à 16+16+16 (`msds-essentiel-msds-js-2026#08-taille-des-groupes`, novembre 2025, « sans influence sur le minimum de 12 ») puis dite « inchangée » (`msds-essentiel-msds-js-2027#03-fusion-groupes-cibles`) ; le quota 36 / +1 par 12 n'est pas contredit, à confirmer dans le guide des offres 2027 (non ingéré ; les deux newsletters ne le reprennent pas).
- Compter 4 h sans distinguer le jeu : AC plafonnées à 2 h en 2026, plus de plafond en 2027 mais 2 h sportives.
- Compter comme sportif un bricolage, un montage de tente, un chant : non sportif — `msds-exigences-js-2027-camps#01-contenu`.
- Laisser des activités sans identifiant, ou deux activités simultanées d'une même branche sans numéro distinct.
- Programme détaillé réduit au picasso : N6 exige un écrit par bloc, y compris les jeux et activités du thème.
- AS et AA comptées dans les 4 h J+S ; blocs de moins de 30 min comptés.
- Oublier la validation par l'expert du domaine de sécurité (rarement vue, terrain) : N9.
- Jour d'arrivée ou de départ pauvre en activités : voir N16.
- Camp à l'étranger, camp vaudois de plus de 7 jours (annonce au SPJ 6 semaines avant) : démarches supplémentaires ; le ratio d'encadrement vaudois n'est pas repris ici (mainteneur) — `msds-hering-camps#03-b-annonce-de-camp-programme-general`.
- Canevas : `js-exemple-programme-camp-ete` et les trois modèles `js-modele-prog-general-sport-jeunes`, `js-modele-prog-general-sport-enfants`, `js-modele-prog-general-enfants-jeunes` sont des PDF d'une page, de 2014 ou non datés ; les trois modèles J+S sont `fidelity: partial` (grille en partie perdue : couleurs de légende, cellules fusionnées, colonnes parasites). Formats reconnus, jamais exigés. Les modèles de bloc AC et SC relèvent de `activite-js`.

## Trame de conception
1. Fixer la date, la forme de camp, les branches, l'effectif, la durée ; choisir le jeu 2026 ou 2027 ; vérifier N13-N15.
2. Fixer trois priorités au plus, le thème et le fil rouge (Q4, Q10, Q19).
3. Poser les points fixes (réveil, repas, début et fin de journée, séance de maîtrise) puis les points culminants (Q2, Q4).
4. Remplir les blocs J+S de chaque jour : durée, part sportive par tranche de 15 min (2027), période de la journée, forme caractéristique, activité itinérante dans l'offre (N17-N20).
5. Placer AS et AA et les moments libres ; vérifier la courbe d'intensité.
6. Numéroter chaque activité de façon unique ; couleur par type, légende ; un picasso par branche ou colonnes lisibles ([non officiel] PC-13).
7. Nommer le responsable de jour et le responsable de chaque activité ; répartir les tâches (Q7, Q12).
8. Écrire un bloc par activité (modèles et critères : `activite-js`) et prévoir la variante d'intempéries (N6, Q8).
9. Joindre concept de sécurité du camp et des activités dangereuses (N8, N9) ; compléter le dossier (N5).
10. Remettre le dossier 4 semaines avant (N4), corriger, obtenir l'autorisation 3 semaines avant (N12) ; échéances exactes : calendrier de la Sardine.

## Annexe : autres livrables de camp
- Circulaire : prix, dates, lieu, responsables, clôture des inscriptions, matériel, fiche médicale, formulaire d'inscription — `js-sdct-camp#14-informations-du-camp` (Q). Soirée d'information aux parents vivement conseillée (la check-list A 2026 la formule comme acquise) — `msds-autorisation-de-camp#01-contenu`. Protection des données et droit à l'image à traiter [non officiel, revue LV-03].
- Liste d'équipement des participants — `cudesch-camp-liste-equipement#01-contenu`.
- Feuille d'urgence (`fidelity: partial`) — `cudesch-camp-infos-urgence#01-contenu`.
- Budget : estimé et effectif, imprévus d'environ 5 % (5 à 10 % selon J+S), cuisine de 8 à 12 CHF par jour et personne (variable, datée) — `cudesch-camp-budget#01-budget` ; `js-sdct-camp#13-finances-du-camp`. Déficit présenté pour soutien : [non officiel, revue LV-11].
- Reconnaissance : rapport avec photos et croquis, thèmes à aborder avec le propriétaire (inondation, chutes de pierres, vent) — sous tentes : `js-sdct-camp#07-lieu-du-camp` ; `cudesch-camp-reco-sous-tentes#01-contenu` ; sous toit : `cudesch-camp-reco-sous-toit#01-contenu`. Bail écrit vivement conseillé, même si l'oral subsiste (la check-list A 2026 le formule comme acquis : « un contrat existe et a été signé ») — `cudesch-camp-bail-place-tentes#01-contenu` ; `js-sdct-camp#07-lieu-du-camp` (contrat pour toute place). Constructions sur croquis, plan ou photo aérienne — `js-sdct-camp#11-programme-detaille-securite`.
- Délais de la Sardine en ligne (en jours avant le début du camp) : données du camp au coach et ouverture dans la MiData J-150 ; offre J+S dans la BDNS par le coach J-90 ; congé jeunesse J-77 (initier) et J-62 (confirmer) ; programme général au RG et au coach J-49 ; annonce MSdS par le coach, commandes de cartes et de matériel de prêt au coach J-43 ; maîtrise et cuisine dans la MiData, commune informée J-30 ; dossier de camp J-28 ; autorisation J-21 ; liste des participants Rega J-14 ; billet CFF J-7 ; après le camp : suivre N21 à N23 (cartes sous 3 jours, MiData sous 10 jours, offre sous 30 jours après le dernier camp) ; clôture BDNS du camp et comptes : après le camp, sans délai chiffré confirmé dans les chapitres ingérés — (calendrier de la Sardine en ligne, non ingéré) ; `cudesch-camp-liste-delais#01-contenu` (version 2018, en retrait)
- Voilà : mention seulement, programme peu actif aujourd'hui (revue LV-17) — `msds-hering-camps#02-a-preparation-saison-des-camps`.
- Bilan : évaluation 2 à 4 semaines après le camp, format libre, information facile à retrouver — `js-sdct-camp#22-evaluation-du-camp`.

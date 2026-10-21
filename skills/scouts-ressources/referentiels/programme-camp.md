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
sources: [msds-hering-camps, msds-essentiel-msds-js-2027, js-structure-formation-sdct, js-module-directives-sdct, js-module-bases-sdct, msds-essentiel-msds-js-2026, js-sdct-camp, msds-reglement-de-camp, msds-autorisation-de-camp, msds-exigences-js-2027-camps, js-guide-offres-sct, js-manuel-sport-de-camp-trekking, js-exemple-programme-camp-ete, js-modele-prog-general-sport-jeunes, js-modele-prog-general-sport-enfants, js-modele-prog-general-enfants-jeunes, cudesch-camp-liste-delais, cudesch-camp-budget, cudesch-camp-reco-sous-tentes, cudesch-camp-reco-sous-toit, cudesch-camp-bail-place-tentes, cudesch-camp-liste-equipement, cudesch-camp-infos-urgence, cudesch-securite, cudesch-cudeschin, cudesch-programme, cudesch-etre-responsable, cudesch-branche-castors, cudesch-branche-louveteaux, cudesch-branche-eclais, cudesch-branche-picos, cudesch-branche-route]
inclut: [activite-js, concept-de-securite]
statut: valide
relu_le: 2026-10-21
---
Livrable principal : le programme de camp, soit le picasso (grille jour × heure) et les fiches de blocs qui le détaillent. Les autres livrables de camp sont en annexe, sans développement. La fiche d'une activité (modèles de bloc AC et SC compris) relève de `activite-js`, le concept de sécurité avec `concept-de-securite`. Le « programme général » officiel est la vue d'ensemble, le « programme détaillé » le dossier qui le complète ; le picasso tient lieu de programme général (terrain).

## Non-négociables
Portées : `[tous]` camp annoncé J+S ou non ; `[js]` camp annoncé J+S, quelle que soit la date ; `[2027]` camp J+S dès 2027-01-01 ; `[après]` délais de clôture, après le camp. Camp non J+S : seuls les N `[tous]` (N1 à N12) s'appliquent ; N22 vaut aussi pour un camp non J+S annoncé dans la MiData (mainteneur).
N1. [tous] Le programme général indique : thème, responsable de camp, organisateur, coach, lieu et nom du gîte ou de la place, dates, genre de camp, jour-date-responsable de la journée, nom de chaque activité et de son responsable, heures d'arrivée et de départ — `msds-hering-camps#03-b-annonce-de-camp-programme-general`
N2. [tous] Le responsable de camp transmet le programme général avec l'annonce au RG et au coach, qui donne un retour — `msds-hering-camps#03-b-annonce-de-camp-programme-general`
N3. [tous] Tout camp dès trois jours, J+S ou non, s'annonce dans la MiData : le responsable de camp complète l'annonce et remet le programme général au RG et au coach **7 semaines** avant le début ; le coach transmet l'annonce au MSdS **6 semaines** avant — `msds-reglement-de-camp#03-encadrement-autorisation` (6 semaines) ; `cudesch-camp-liste-delais#01-contenu` (7 semaines) ; Sardine J-49 / J-43. « Dès trois jours » (choix prudent du mainteneur) : le règlement s'applique dès trois jours (`msds-reglement-de-camp#01-exigences-camp`), le formulaire d'autorisation aussi (`msds-autorisation-de-camp#01-contenu`) ; la clause d'annonce et la Sardine disent « plus de 3 jours »
N4. [tous] Le dossier de camp est remis au RG et au coach au moins 3 semaines avant le début — `msds-reglement-de-camp#03-encadrement-autorisation` ; `msds-hering-camps#05-d-programme-detaille`. La Sardine place le dossier à J-28 et l'autorisation à J-21 : retenir 4 semaines, date prudente
N5. [tous] Le dossier contient : programme général, thème et fil rouge, description des blocs, concept de sécurité du camp, règles du camp, arrangements d'équipe (tâches, responsables du jour), liste des participants ; pour une randonnée : temps de marche, cartes, concept de sécurité, programme de mauvais temps — `msds-hering-camps#05-d-programme-detaille`
N6. [tous] Chaque bloc est décrit par écrit : nom, jour-date-heure, lieu, fil rouge, responsables, contenu et déroulement chronométré, matériel, variante d'intempéries, concept de sécurité de l'activité si nécessaire — `msds-hering-camps#05-d-programme-detaille`
N7. [tous] Jeux, sport et activités du thème sont tous décrits, pas seulement les activités J+S — `msds-hering-camps#05-d-programme-detaille`
N8. [tous] Un concept de sécurité existe pour le camp et pour chaque activité à caractère dangereux, J+S ou non — `msds-reglement-de-camp#01-exigences-camp` ; `msds-hering-camps#05-d-programme-detaille` ; `msds-autorisation-de-camp#01-contenu` (check-list A)
N9. [tous] Les activités d'un domaine de sécurité (montagne, hiver, eau) sont approuvées et signées par un·e expert·e J+S du domaine ; le coach signe ensuite l'autorisation après avis de l'expert·e (mainteneur) — `msds-reglement-de-camp#03-encadrement-autorisation` ; `msds-hering-camps#05-d-programme-detaille` ; `msds-autorisation-de-camp#01-contenu`
N10. [tous] Le programme répond aux exigences de la branche et aux fondements du scoutisme ; camp interbranches : programme en grande partie propre à chaque branche — `msds-reglement-de-camp#01-exigences-camp` ; `msds-reglement-de-camp#03-encadrement-autorisation`. Repères : « Selon la branche »
N11. [tous] Camp avec filles et garçons : maîtrise de femmes et d'hommes, réflexion sur hébergement, rôles, tâches, santé — `msds-reglement-de-camp#01-exigences-camp` (qui dit « camp mixte », mot à éviter ici : critères non officiels) ; `cudesch-etre-responsable#25-egaux-et-equitables` (encadrement mixte, tentes ou dortoirs séparés, tâches réparties sans stéréotype)
N12. [tous] Le camp n'a lieu qu'avec l'autorisation signée du RG et du coach (éventuellement avec compléments, à valider avant le camp) — `msds-reglement-de-camp#03-encadrement-autorisation` ; `msds-hering-camps#07-f-autorisation-de-camp`
N13. [js] Au moins 12 participants en âge J+S ; jusqu'à fin 2026, selon les groupes cibles enfants/jeunes et leurs reconnaissances ; dès 2027, un même camp et une seule reconnaissance couvrent les 5 à 20 ans. Au moins deux moniteurs J+S SdC/T, dont un avec le complément « chef de camp » en 2026, « Responsable de camp » dès 2027 (même complément, voir Pièges) — `msds-essentiel-msds-js-2027#03-fusion-groupes-cibles` (2027 : minimum « reste fixé à 12 ») ; `js-guide-offres-sct#01-contenu` (guide 2023)
N14. [js] Encadrement : un moniteur par sous-groupe d'activité J+S. Jusqu'à fin 2026 : deux moniteurs jusqu'à 36 participants, puis un moniteur habilité de plus par tranche de 12 supplémentaires — `js-guide-offres-sct#01-contenu` (guide 2023 ; OPESp art. 13 al. 2 et annexe 2). Dès 2027 : taille de groupe 16+16+16 et taux d'encadrement minimal d'un moniteur pour 16 participants, au moins deux moniteurs et 12 participants (N13) — `msds-essentiel-msds-js-2027#03-fusion-groupes-cibles` ; `msds-essentiel-msds-js-2026#08-taille-des-groupes` (1:16 : mainteneur, voir Pièges)
N15. [js] Au moins quatre jours consécutifs (trois si la même offre contient un autre camp de quatre jours ou plus) ; chaque jour de camp compte au moins 4 h d'activités J+S, en blocs d'au moins 30 min. Jeux 2026 et 2027 (mainteneur) — `js-guide-offres-sct#01-contenu` ; `msds-hering-camps#03-b-annonce-de-camp-programme-general` ; 2027 : `js-module-directives-sdct#01-directives-sport-de-camp-trekking`
N16. [js] Les jours d'arrivée et de départ comptent ensemble pour un jour de camp s'ils totalisent 4 h d'activités J+S (exemple J+S : 3 h le premier jour, 1 h 30 le dernier) ; jeux 2026 et 2027 — `msds-hering-camps#03-b-annonce-de-camp-programme-general` ; 2027 : `js-module-directives-sdct#01-directives-sport-de-camp-trekking`
N17. [2027] Chaque jour : au moins 4 h d'activités J+S, dont au moins 2 h d'activité sportive (comptée dès 30 min, indiquée pour chaque activité J+S par tranches de 15 min ; comptage : `activite-js` N10) — `js-module-directives-sdct#01-directives-sport-de-camp-trekking` (journée J+S) ; `msds-exigences-js-2027-camps#01-contenu` ; `msds-hering-camps#03-b-annonce-de-camp-programme-general`
N18. [2027] Les blocs d'activité J+S figurent clairement dans le programme avec un numéro — `msds-hering-camps#03-b-annonce-de-camp-programme-general`. Mise en œuvre (conférence formation MSdS 2026, non ingérée) : chaque bloc dit s'il est une activité J+S et porte sa durée d'activité physique (0 min, ou 30 min et plus par tranches de 15 min) ; exemple de grille « J+S 1.1, TS = 0 min », « AA 1.2 » — `js-exemple-programme-camp-ete#01-contenu`
N19. [2027] Les activités J+S s'adressent à tou·te·s, durent 30 min au moins, se répartissent sur au moins deux périodes (matin, après-midi, soir), sont actives et axées sur le mouvement, axées sur une ou plusieurs formes caractéristiques, cohérentes et adaptées aux besoins — `msds-exigences-js-2027-camps#01-contenu` ; `js-module-directives-sdct#01-directives-sport-de-camp-trekking` (définitions : `activite-js` N11, Q6)
N20. [2027] Offre J+S : au moins un camp de quatre jours consécutifs ou plus, les autres camps de trois jours au moins ; au moins une activité itinérante (participants en déplacement hors du lieu de camp : randonnée, tour à vélo, chasse au trésor, jeu à postes) ; toutes les formes caractéristiques traitées sur l'ensemble de l'offre (un camp scout qui intègre les huit méthodes et les cinq relations la remplit, selon l'aide-mémoire) — `js-module-directives-sdct#01-directives-sport-de-camp-trekking` ; `msds-exigences-js-2027-camps#01-contenu` ; camp de plus de 4 jours : au plus un jour sans activité J+S — `msds-hering-camps#03-b-annonce-de-camp-programme-general` ; `js-guide-offres-sct#01-contenu` (nuance du module J+S : Pièges). N17 à N20 : module J+S « Directives Sport de camp/Trekking » (prescription dès 2027), aide-mémoire MSdS de septembre 2026, Sardine
N21. [après] Cartes nationales renvoyées à swisstopo au plus tard 3 jours après le camp — `msds-hering-camps#08-g-cloture-du-camp`
N22. [après] Participants et responsables ajustés dans la MiData, coach informé au plus tard 10 jours après — `msds-hering-camps#08-g-cloture-du-camp`
N23. [après] Offre J+S clôturée par le coach à la fin de l'année, au plus tard 30 jours après le dernier camp — `msds-hering-camps#09-h-cloture-de-l-offre-js`

## Selon la date
Jeu 2027 par défaut ; jeu 2026 seulement si le camp est explicitement daté avant le 2027-01-01 (hypothèse annoncée en une phrase ; question si le document est ambigu). On juge sur la date du camp, pas de la relecture. Camp à cheval sur le 2027-01-01 : cas ignoré (mainteneur). Le guide des offres OFSPO 2027 n'est pas ingéré.

| Point | Camp jusqu'au 2026-12-31 (jeu 2026) | Camp dès 2027-01-01 (jeu 2027) |
|---|---|---|
| Statut des activités | Chaque activité J+S est SC ou AC, indiqué au programme — `js-sdct-camp#10-programme-general` | Plus de classement AC, SC ni par domaines : activités J+S et leur part de sport (N17, N18) ; définitions : `js-manuel-sport-de-camp-trekking#15-formes-caracteristiques` |
| Temps par jour | 4 h d'activités J+S, dont au plus 2 h d'AC — `msds-hering-camps#03-b-annonce-de-camp-programme-general` ; `js-sdct-camp#10-programme-general` ; `cudesch-cudeschin#03-activite-dans-le-sport-de-camp-trekking` | 4 h d'activités J+S, dont au moins 2 h sportives, sans plafond d'AC (N17) ; premier et dernier jour cumulables (N16) |
| Périodes | Journée en trois parties (repas de midi et du soir), 30 min d'AC dans deux d'entre elles (mêmes sources) | Au moins deux périodes, activités de 30 min au moins (N19) |
| Jour sans J+S | Au plus un, sans subside, dans un camp de plus de 4 jours | Au plus un dans un camp de plus de 4 jours, et le minimum de journées J+S tenu (N20, Pièges) |
| Numérotation | Pas de numéro J+S exigé | Numéro pour chaque bloc J+S (N18) |
| Référence de relecture | Autorisation de camp MSdS valable jusqu'au 31.12.2026 — `msds-autorisation-de-camp#01-contenu` | Formulaire 2027 non ingéré : N12 et Q1, Q3-Q6, Q10, Q13-Q15 reposent sur les check-lists 2026, gardés en 2027, à revérifier à l'ingestion (mainteneur) |
| Modèle de picasso | Modèles de bloc AC et SC : `activite-js` | `js-exemple-programme-camp-ete#01-contenu` (temps sportif par activité, numéros, légende J+S / programme de camp) |

Camp non J+S : le coach relit le dossier sans exiger les éléments J+S à la lettre (terrain, mainteneur).

## Critères de qualité
Q1. Le dossier contient le programme général (picasso), discuté avec le coach — `msds-autorisation-de-camp#01-contenu` (check-list A) ; `js-sdct-camp#10-programme-general`. Informations générales du picasso : trame cantonale, non officielle
Q2. Les points fixes (réveil, repas, début et fin de journée, séance des moniteurs, loisirs) sont posés d'abord ; « à la même heure chaque jour » vaut pour les enfants et peut varier selon la branche (mainteneur) — `js-sdct-camp#10-programme-general`
Q3. Programme adapté à l'âge, équilibré, varié, avec des moments de détente ; alternance dynamique et calme ; moments de recueillement possibles — `js-sdct-camp#10-programme-general` ; `msds-autorisation-de-camp#01-contenu` (check-list B)
Q4. Des points culminants répartis sur le camp ; un thème vécu comme fil rouge reliant les activités — `msds-autorisation-de-camp#01-contenu` (check-list B)
Q5. Huit méthodes et cinq relations trouvent leur place dans le programme (la check-list 2026 cite encore sept méthodes) — `msds-exigences-js-2027-camps#01-contenu` ; `msds-autorisation-de-camp#01-contenu` (check-list B)
Q6. Progression personnelle, Loi et Promesse, rituels : prévus au programme — `msds-autorisation-de-camp#01-contenu` (check-list B)
Q7. Un responsable du jour nommé chaque jour (séance des moniteurs, déroulement, réveil, temps libre, extinction) ; un responsable par activité — `js-sdct-camp#04-repartition-des-taches` ; `msds-hering-camps#03-b-annonce-de-camp-programme-general`
Q8. Programme de mauvais temps : activités tributaires de la météo repérées, au moins une activité en plein air conservée — `js-sdct-camp#10-programme-general`
Q9. Âges très différents : activités différenciées, pas de programme « entre deux » — `js-sdct-camp#10-programme-general`
Q10. Des priorités de camp définies : trois au plus, une ou deux suffisent (mainteneur ; les sources disent « trois priorités » et « 3 objectifs de camp ») — `js-sdct-camp#08-programme-de-camp` ; `msds-autorisation-de-camp#01-contenu` (check-list C)
Q11. Participants associés aux décisions selon l'âge (parlement de camp, tâches, parties de programme) — `js-sdct-camp#08-programme-de-camp`
Q12. Tâches réparties selon les aptitudes, les expérimentés soutenant les autres — `js-sdct-camp#11-programme-detaille-securite`
Q13. Parties les plus exigeantes, les moins captivantes, celles qui risquent de faire peur : identifiées avec la maîtrise — `msds-autorisation-de-camp#01-contenu` (check-list B)
Q14. Règles du camp avec conséquences claires, connues de tous ; charte de camp — `msds-autorisation-de-camp#01-contenu` (check-list A) ; `js-sdct-camp#16-regles-du-camp` ; `cudesch-securite#29-concept-de-securite-pour-un-camp`
Q15. La maîtrise connaît le scénario de crise cantonal et la helpline scoute — `msds-autorisation-de-camp#01-contenu` (check-list A)
Q16. Camp non J+S : les règles de sécurité J+S sont tout de même respectées — `msds-reglement-de-camp#01-exigences-camp`
Q17. Pas d'occupation 24 h sur 24 : du temps libre, avec un interlocuteur — `js-sdct-camp#10-programme-general`
Q18. Encadrement : le règlement fixe l'effectif selon participants, activités et branche, sans ratio ; prévoir plus que le minimum J+S (N14) — `msds-reglement-de-camp#02-maitrise-de-camp`
Q19. Le camp est planifié comme un grand événement : buts concrets en équipe, thème et fil rouge, rétroplanning avec secteurs et responsables écrits, contrôle de la qualité du programme (fondements, formes de mouvement) — `cudesch-programme#04-planifier`
Q20. [2027] Le programme vise un but, pas une suite d'activités isolées : les formes caractéristiques donnent la direction, les formes d'activité la concrétisent, une activité complexe (randonnée) rassemble les acquis des précédentes — `js-module-bases-sdct#01-bases-du-sport-de-camp-trekking`
Q21. [2027] Les longs temps morts sont repérés et transformés pour que tous restent en mouvement (deux parties en parallèle dans un tournoi, poste d'exercices pour les éliminés) — `js-module-directives-sdct#01-directives-sport-de-camp-trekking` (remarque)

## Critères non officiels
[non officiel] Chaque activité (J+S, AA, AS, repas, transport) porte un identifiant unique ; la forme varie (jour.n, par type), l'unicité compte. Blocs J+S dès 2027 : N18. (revue PC-12)
[non officiel] Une couleur par type d'activité et une légende : conseillé, pas obligatoire. (revue PC-11)
[non officiel] Plusieurs branches ou programmes : un picasso par branche, ou colonnes ou couleurs montrant qui suit quel programme (interbranches : N10). « Camp mixte » désigne dans les équipes plusieurs branches, dans le règlement filles et garçons (N11) ; en 2027 seule disparaît la catégorie J+S enfants + jeunes, pas les camps interbranches. (revue PC-13)
[non officiel] Début et fin du camp : transports et rendez-vous inscrits, comme les traditions du groupe (raid, journée des familles, cérémonies) ; rituels, Loi et Promesse sont officiels (Q6). (revue PC-03, PC-04)
[non officiel] AA (autre activité, = AdA = VC, hors J+S) et AS (activité spirituelle, un type d'AA : mainteneur) figurent au programme sans critères J+S et hors des 4 h J+S. Un espace de parole ou de partage est souvent une AA, AS comprise. (terrain ; revue FO-21)
[non officiel] PF = point fixe (mainteneur, pas « plage fixe ») : séance de maîtrise du soir, quotidienne ; selon les groupes, aussi les moments fixes de la journée (réveil, repas). À légender. (terrain ; principe des points fixes officiel : Q2)
[non officiel] Charge répartie équitablement entre responsables, un expérimenté pouvant en prendre un peu plus : à favoriser, sans imposer. (revue PC-16)
[non officiel] Moments « participant » pour la maîtrise (se détendre, partager) : recommandés. (revue PC-17)
[non officiel] Responsable de jour idéalement sans activité propre, quand c'est possible ; dire « responsable de jour ». (revue FO-12)
[non officiel] Cahier des charges d'une page par poste (responsable de jour, infirmerie, matériel) : pratique de certains groupes. (revue FO-11 ; seules les tâches possibles du responsable du jour sont officielles : `js-sdct-camp#04-repartition-des-taches`)
[non officiel] Quota : la règle J+S est N13-N14 ; le « un responsable pour douze » du rapport de coach n'est officiel que pour le camp au bord de l'eau (un brevet SSS pour 12 participants, `js-sdct-camp#06-formes-de-camp`). Plus de responsables que le minimum : recommandé (Q18). (revue FO-10)
[non officiel] Circuit de relecture : chaque fiche a un auteur et un relecteur, avec un tableau d'état (ok, à revoir, à compléter) ; fréquent. (revue FO-01, FO-04 : l'autorisation officielle a trois états, N12)
[non officiel] Date de rendu des fiches bien avant le camp ; échéancier à deux colonnes (délai officiel de la Sardine, délai du coach plus tôt). (revue FO-02, FO-05)
[non officiel] Préparation de 6 à 10 mois (séances, parfois un week-end) ; pré-camp de montage fréquent, pas obligatoire ; relecture des bilans précédents au démarrage. (revue FO-19, FO-20, FO-17)
[non officiel] Trame cantonale du picasso : jours en colonnes, demi-heures en lignes, informations générales (responsable de camp, RG, coach, genre, lieux, thème, effectif, informations J+S : type, jours J+S, jours de voyage, numéro d'offre), trois priorités rédigées, légende, abréviations. (terrain)

## Selon la branche
Repères des livres de branche du cudesch pour N10 : des recommandations (Q, jamais N).
- Castors : pas de camp — `msds-reglement-de-camp#01-exigences-camp` ; week-end : nuitée facultative, lieu connu, « moins, c'est plus » (du samedi après-midi au petit-déjeuner du dimanche) — `cudesch-branche-castors#15-activites-speciales` ; attention limitée (environ 15 min), besoin de structure et d'autonomie — `cudesch-branche-castors#06-enfants`
- Louveteaux : activités de 3 à 4 h, camp d'une semaine en chalet (tente possible en camp de groupe ou cantonal), programme diversifié dans un thème captivant, crainte de l'éloignement — `cudesch-branche-louveteaux#08-organisation` ; aventures dans la nature à portée simple — `cudesch-branche-louveteaux#40-activites-dans-la-nature`
- Éclais : camp d'été de deux semaines sous tentes, thème et fil rouge, programme séparé si d'autres branches participent, équilibre des relations et méthodes ; limites des activités de patrouille (concept de sécurité) — `cudesch-branche-eclais#20-les-specificites-de-la-branche` ; moments et activités de patrouille plus exigeants dans le programme de camp — `cudesch-branche-eclais#21-la-particularite-des-activites-en`
- Picos : camp organisé par l'Équipe, orienté vers un objectif, souvent itinérant, programme autonome, règles J+S, dossier d'entreprise — `cudesch-branche-picos#43-les-camps` ; activités détaillées et leur durée (exemple du « 15 heures Picos ») — `cudesch-branche-picos#44-les-activites-picos-en-detail`
- Route : projet, expédition, camps en clan, veillée Route (planification complète portée par le clan) — `cudesch-branche-route#20-activites`

## Questions à poser avant de juger
1. Date du camp : avant ou dès le 2027-01-01 (jeu 2026 ou 2027) ? Obligatoire.
2. Camp annoncé J+S ou non ? Sinon, seuls les N `[tous]` s'appliquent.
3. Forme et lieu du camp : sous toit, sous tente, itinérant ; à l'étranger ?
4. Branches concernées et nombre de programmes (un picasso par branche ?).
5. Effectifs : participants et responsables (N13, N14).
6. Durée du camp (N15, N20).
7. Pièces jointes : picasso, programme général, programme détaillé, concept de sécurité. Les demander avant de conclure qu'une pièce manque.

## Pièges
- 6 et 7 semaines ne se contredisent pas (N3). Renvoyer au calendrier de la Sardine en ligne (non ingéré), qui calcule les échéances depuis la date de début, plutôt que recopier des délais. Les dossiers réels annoncent souvent plus tard (terrain).
- Encadrement 2027 (N14) : la taille de groupe subventionnée est fixée à 16+16+16 (`msds-essentiel-msds-js-2026#08-taille-des-groupes`, novembre 2025 : « sans influence sur le minimum de 12 »), puis dite « inchangée » (`msds-essentiel-msds-js-2027#03-fusion-groupes-cibles`) ; le taux d'encadrement minimal d'un moniteur pour 16 participants reste inchangé (conférence formation MSdS 2026, non ingérée ; mainteneur). Le quota 36 / +1 par 12 du guide 2023 est le jeu 2026 : ne pas l'appliquer à un camp 2027.
- Complément de conduite du camp (N13) : la newsletter de la formation d'octobre 2026 (non ingérée) écrit « chef·fe de camp » ; l'aide-mémoire MSdS 2027 et la structure de formation J+S (`js-structure-formation-sdct#01-contenu`) écrivent « Responsable de camp ». Un seul complément en 2027, les deux mots circulent (mainteneur) : écrire « Responsable de camp », accepter l'autre.
- Jour sans activité J+S (N20) : la Sardine et le guide 2023 disent « au plus un » dans un camp de plus de 4 jours ; le module J+S 2027 le dit « possible si le nombre minimum de journées J+S est respecté », sans plafond (`js-module-directives-sdct#01-directives-sport-de-camp-trekking`). Les deux conditions se cumulent (mainteneur) : au plus un jour sans activité J+S, et le minimum de journées J+S tenu ; un deuxième jour est un écart à signaler.
- Temps sportif d'un bloc 2027 : activité purement sportive comptée en entier, pauses, explications, transitions, échauffement et retour au calme compris (tournoi de 2 h = 2 h) ; activité mixte : parties sportives seulement (jeu de piste de 3 h avec 6 × 15 min de marche = 1 h 30 ; 90 min dont 45 min de jeu sportif = 45 min) ; moins de 30 min sportives dans une activité : 0 — `js-module-directives-sdct#01-directives-sport-de-camp-trekking`. Exemple MSdS : 4 h de construction d'une tour = activité J+S active dont 3 h sportives, l'heure de planification non comptée (mail MSdS aux coachs, octobre 2026, non ingéré).
- Cas limites : un camp J+S 2026 reste en général un camp J+S en 2027 ; marge d'interprétation au responsable de camp et au coach ; juger l'esprit (programme varié, actif) avant la lettre (conférence formation MSdS 2026, non ingérée).
- Compter 4 h sans distinguer le jeu : plafond d'AC en 2026, 2 h sportives en 2027 (Selon la date).
- Compter comme sportifs bricolage, montage de tente, chant — `msds-exigences-js-2027-camps#01-contenu`.
- Activités sans identifiant, ou deux activités simultanées d'une même branche sans numéro distinct.
- Réduire le programme détaillé au picasso : un écrit par bloc, jeux et activités du thème compris (N6, N7).
- Compter AS, AA ou des blocs de moins de 30 min dans les 4 h J+S.
- Oublier la validation par l'expert du domaine de sécurité (N9), rarement vue (terrain).
- Jour d'arrivée ou de départ pauvre en activités : N16.
- Camp à l'étranger, camp vaudois de plus de 7 jours (annonce au SPJ 6 semaines avant) : démarches supplémentaires ; le ratio d'encadrement vaudois n'est pas repris ici (mainteneur) — `msds-hering-camps#03-b-annonce-de-camp-programme-general`.
- Canevas : `js-exemple-programme-camp-ete` et les modèles `js-modele-prog-general-sport-jeunes`, `js-modele-prog-general-sport-enfants`, `js-modele-prog-general-enfants-jeunes` sont des PDF d'une page, de 2014 ou non datés ; les trois modèles sont `fidelity: partial` (couleurs de légende, cellules fusionnées, colonnes parasites). Formats reconnus, jamais exigés.

## Trame de conception
1. Fixer date, forme de camp, branches, effectif, durée ; choisir le jeu 2026 ou 2027 ; vérifier N13-N15.
2. Fixer trois priorités au plus, le thème et le fil rouge (Q4, Q10, Q19).
3. Poser les points fixes puis les points culminants (Q2, Q4).
4. Remplir les blocs J+S de chaque jour : durée, part sportive par 15 min (2027), période, forme caractéristique, activité itinérante dans l'offre (N17-N20).
5. Placer AS, AA et moments libres ; vérifier la courbe d'intensité.
6. Numéroter chaque activité de façon unique ; couleur par type, légende ; un picasso par branche ou colonnes lisibles ([non officiel] PC-13).
7. Nommer le responsable de jour et celui de chaque activité ; répartir les tâches (Q7, Q12).
8. Écrire un bloc par activité (modèles et critères : `activite-js`), avec sa variante d'intempéries (N6, Q8).
9. Joindre le concept de sécurité du camp et des activités dangereuses (N8, N9) ; compléter le dossier (N5).
10. Remettre le dossier 4 semaines avant (N4), corriger, obtenir l'autorisation 3 semaines avant (N12) ; échéances exactes : calendrier de la Sardine.

## Annexe : autres livrables de camp
- Circulaire : prix, dates, lieu, responsables, clôture des inscriptions, matériel, fiche médicale, formulaire d'inscription — `js-sdct-camp#14-informations-du-camp` (Q). Soirée d'information aux parents vivement conseillée (acquise selon la check-list A 2026) — `msds-autorisation-de-camp#01-contenu`. Protection des données et droit à l'image à traiter [non officiel, revue LV-03].
- Liste d'équipement des participants — `cudesch-camp-liste-equipement#01-contenu`.
- Feuille d'urgence (`fidelity: partial`) — `cudesch-camp-infos-urgence#01-contenu`.
- Budget : estimé et effectif, imprévus d'environ 5 % (5 à 10 % selon J+S), cuisine de 8 à 12 CHF par jour et personne (variable, datée) — `cudesch-camp-budget#01-budget` ; `js-sdct-camp#13-finances-du-camp`. Déficit présenté pour soutien : [non officiel, revue LV-11].
- Reconnaissance : rapport avec photos et croquis, risques à voir avec le propriétaire (inondation, chutes de pierres, vent) ; sous tentes : `js-sdct-camp#07-lieu-du-camp` ; `cudesch-camp-reco-sous-tentes#01-contenu` ; sous toit : `cudesch-camp-reco-sous-toit#01-contenu`. Bail écrit vivement conseillé, même si l'oral subsiste (check-list A 2026 : « un contrat existe et a été signé ») ; contrat pour toute place — `cudesch-camp-bail-place-tentes#01-contenu` ; `js-sdct-camp#07-lieu-du-camp`. Constructions sur croquis, plan ou photo aérienne — `js-sdct-camp#11-programme-detaille-securite`.
- Délais de la Sardine en ligne (jours avant le début) : J-150 données du camp au coach et ouverture dans la MiData ; J-90 offre J+S dans la BDNS (coach) ; J-77 et J-62 congé jeunesse (initier, confirmer) ; J-49 et J-43 (N3), commandes de cartes et de matériel de prêt au coach à J-43 ; J-30 maîtrise et cuisine dans la MiData, commune informée ; J-28 et J-21 (N4) ; J-14 liste des participants Rega ; J-7 billet CFF ; après le camp : N21 à N23 ; clôture BDNS du camp et comptes sans délai chiffré confirmé — (calendrier de la Sardine en ligne, non ingéré) ; `cudesch-camp-liste-delais#01-contenu` (version 2018, en retrait)
- Voilà : mention seulement, programme peu actif aujourd'hui (revue LV-17) — `msds-hering-camps#02-a-preparation-saison-des-camps`.
- Bilan : évaluation 2 à 4 semaines après le camp, format libre, information facile à retrouver — `js-sdct-camp#22-evaluation-du-camp`.

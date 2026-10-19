---
slug: ua
titre: Unité d'apprentissage (UA, anciennement « point de cours ») d'un cours MSdS / J+S
signaux: [UA, unité d'apprentissage, point de cours, PdC, descriptif d'UA, PATExE, PATEXE, GAG, objectif d'apprentissage, sommaire des UA, programme détaillé, conception de cours, maîtrise de cours, CàF, relire une UA, commentaire de correction d'une UA]
role: [formateur, maitrise-de-cours, caf, expert-js, coach-js]
verbes: [corriger, concevoir]
parametres:
  - {nom: type de cours et branche, obligatoire: true}
  - {nom: date du cours, obligatoire: true}
  - {nom: sommaire des UA du cours, obligatoire: false}
  - {nom: canevas utilisé, obligatoire: false}
canevas: [autre-canevas-ua-top, autre-canevas-point-de-cours-js]
sources: [msds-unite-d-apprentissage, msds-ancre, cofor-administration-cours-federaux, msds-le-cours, msds-modele-de-formation, cofor-checklist-cours-base, js-sdct-bases, cudesch-glossaire, cofor-liste-buts-cours-ru, msds-retour-qualifier-accompagner, autre-canevas-ua-top, autre-canevas-point-de-cours-js, cofor-pano-retour-qualifier]
inclut: []
statut: valide
relu_le: 2026-10-18
---

Périmètre : une UA d'un cours de formation scout (descriptif écrit), et le commentaire qu'on en fait. Le terme courant est **UA** ; « point de cours » (PdC) est l'ancien nom et se reconnaît comme synonyme. La base du référentiel est constituée des brochures MSdS (brochure verte `msds-unite-d-apprentissage`, bleue `msds-le-cours`, orange `msds-retour-qualifier-accompagner`) ; le §3.5 « Écrire une unité d'apprentissage » de la brochure verte fournit la check-list du descriptif (`msds-unite-d-apprentissage#10-ecrire`, p.35). Les canevas Top et J+S cantonal sont des formats acceptés, pas la norme.

**Hors périmètre** (futur référentiel `qualification`) : présence minimale de 80 % (ligne directrice MSdS, `msds-ancre#16-presences-et-qualifications` ; condition de validation de l'absence pour J+S, `cofor-administration-cours-federaux#04-confirmation-finances`), critères éliminatoires, grille et entretien de qualification. Ici on ne vérifie que la place que l'UA laisse à l'observation.

## Non-négociables

Les brochures décrivent des pratiques recommandées (« généralement », « il est recommandé », check-list « non exhaustive ») : en cas de doute, c'est un critère de qualité. Seules les exigences d'administration de cours sont retenues.

Portée : `[tous]` = valable quelle que soit la date du cours.

N1. [tous] Le CàF dispose, à l'annonce de cours, du sommaire des UA (buts, contenus) ou, à défaut, du programme détaillé déjà élaboré — `msds-ancre#06-sommaire-points-de-cours`
N2. [tous] Chaque UA est décrite précisément (méthodes et déroulement) dans le programme détaillé, remis par la direction de cours au CàF 2 semaines avant le début de chaque partie du cours — `msds-ancre#13-programme-detaille`. Les 2 semaines sont le minimum de la ligne directrice MSdS : les documents administratifs du cours (J+S, AC) peuvent fixer un autre délai et la maîtrise de cours peut l'allonger ; vérifier le délai annoncé avant de signaler un retard (mainteneur)
N3. [tous] Les objectifs d'apprentissage de l'UA figurent explicitement dans le descriptif (encart logistique) ou, à défaut, dans le sommaire des UA : ils sont la base de la planification de l'UA et de la vérification des apprentissages — `msds-le-cours#08-objectifs-d-apprentissage p.15`, `msds-unite-d-apprentissage#10-ecrire p.35`. (mainteneur) Exception : une UA de niveau « Vivre » porte un objectif formulé comme vécu, sans « est capable de » (Q16).
N4. [tous] Le contenu, le déroulement et les exercices de l'UA permettent d'atteindre les objectifs annoncés : l'Expérimentation reprend le verbe de l'objectif et l'Évaluation en vérifie l'atteinte. Des objectifs sans déroulement qui y mène, ou un déroulement sans lien avec les objectifs, rendent l'UA non conforme (mainteneur) — `msds-unite-d-apprentissage#05-patexe p.19-20` (Q9, Q11, Q15)

## Selon la date

- Niveaux d'approfondissement (Vivre, Mémoriser/comprendre, Appliquer/analyser, Évaluer/créer) : tableau par contenu et par cours du modèle de formation version 2027 — `msds-modele-de-formation#10-niveaux-d-approfondissement`. Entrée en vigueur le 2027-01-01 (mainteneur). La référence se choisit selon la **date du cours**, pas celle de la relecture : une UA préparée fin 2026 pour un cours de 2027 est jugée sur le modèle 2027 ; c'est le cas courant dès maintenant. Pour un cours qui a lieu avant 2027, le modèle précédent n'est pas dans le corpus : le dire, ne pas affirmer de niveau.
- La check-list du cours de base (contenus, niveaux, n° d'UA) est dérivée du modèle 2027 — `cofor-checklist-cours-base#01-contenu`.
- Les brochures verte, bleue et orange sont de version 2026 ; les termes UA, huit méthodes et dispositifs pédagogiques y sont en vigueur.
- Si le cours ou la date manque, le demander avant de juger le niveau taxonomique.

## Critères de qualité

Structure et descriptif
Q1. Le descriptif contient l'encart logistique (nom, date et horaires, durée, formateurs de référence, besoin en formateurs supplémentaires, objectifs) — `msds-unite-d-apprentissage#10-ecrire p.35`
Q2. Chaque partie porte timing, partie PATExE, déroulement détaillé, méthode d'animation, forme sociale, objectif lié, répartition des responsabilités — `msds-unite-d-apprentissage#10-ecrire p.35`
Q3. La synthèse des tâches liste matériel, supports à préparer et responsabilités de préparation — `msds-unite-d-apprentissage#10-ecrire p.35`
Q4. Le descriptif est lisible par une tierce personne (remplaçant, intervenant externe) qui pourrait animer l'UA ; il sert aussi d'archive pour les éditions suivantes — `msds-unite-d-apprentissage#10-ecrire p.34`
Q5. Format : descriptif commun à toutes les UA du cours, numérique, mise en page aérée, rédaction synthétique — `msds-unite-d-apprentissage#10-ecrire p.34`
Q6. Les liens vers les sources des brochures et manuels scouts ou J+S sont indiqués, et des brochures de formation officielles sont citées quand le contenu s'y rapporte (le cours peut ajouter d'autres éléments) — `msds-unite-d-apprentissage#10-ecrire p.35`

PATExE (structure courante, non imposée)
Q7. L'UA suit en général PATExE : Présentation, Activation, Transmission, Expérimentation, Évaluation — `msds-unite-d-apprentissage#05-patexe p.17`
Q8. L'ordre des phases n'est pas figé : commencer par l'Activation, alterner Transmission et Expérimentation sont admis ; ne pas signaler un ordre non linéaire comme erreur — `msds-unite-d-apprentissage#05-patexe p.17`
Q9. L'Expérimentation correspond au verbe d'action de l'objectif (objectif « analyser » : analyser des cas fournis ; objectif « concevoir » : concevoir de A à Z) — `msds-unite-d-apprentissage#05-patexe p.19`
Q10. La Transmission implique les apprenants et alterne les formats (attention limitée, de l'ordre de 10 à 15 minutes) — `msds-unite-d-apprentissage#05-patexe p.18`
Q11. L'Évaluation vérifie l'atteinte des objectifs (régulation) et peut consolider l'apprentissage — `msds-unite-d-apprentissage#05-patexe p.20`
Q12. La structure **GAG** (Global – Analytique – Global, méthode de formation J+S : essai global d'une technique ou d'un jeu, approfondissement analytique de certains éléments, remise en pratique globale) est une alternative admise à PATExE, adaptée aux UA techniques ou de jeu ; la juger sur ses trois phases, pas sur PATExE — `js-sdct-bases#17-conceptions-possibles p.31`, `cudesch-glossaire#02-abreviations p.4`, exemple de but d'un cours RU `cofor-liste-buts-cours-ru#01-contenu`. Le corpus nomme d'autres modèles voisins de PATExE (Gagné, neuf étapes) sans en faire une structure du MSdS — `msds-unite-d-apprentissage#05-patexe p.17`

Objectifs
Q13. Un objectif d'apprentissage se formule « les apprenants sont capables de » + verbe d'action + contenu, avec l'horizon temporel (« à la fin de l'UA ») ; un verbe observable, pas « comprendre » ou « connaître » — `msds-le-cours#08-objectifs-d-apprentissage p.16-17`
Q14. Le niveau taxonomique attendu se déduit de l'objectif (verbe) et correspond à celui prévu par le modèle de formation pour ce contenu et ce cours ; la taxonomie du modèle de formation fait foi, Bloom sert seulement à expliquer — `msds-le-cours#32-annexe-verbes-d-action`, `msds-modele-de-formation#10-niveaux-d-approfondissement p.16`
Q15. Les objectifs sont réalistes pour la plage disponible : le niveau visé doit pouvoir être atteint dans la durée prévue, avec une Expérimentation de taille correspondante (jugement de plausibilité, à formuler comme question) — `msds-le-cours#08-objectifs-d-apprentissage p.16`
Q16. Niveau « Vivre » : du vécu seul, sans attente d'apprentissage à vérifier ; pas de formulation « est capable de », formulation centrée sur le vécu (« les participants vivent…, échangent sur… ») ; ne pas réclamer d'Évaluation des acquis — `msds-le-cours#32-annexe-verbes-d-action p.64`, `msds-le-cours#09-dispositif-pedagogique p.19` (mainteneur)
Q17. Un objectif complet peut préciser comportement, conditions et critère de performance (Mager) — `msds-le-cours#08-objectifs-d-apprentissage p.18`

Cohérence avec le cours
Q18. Le dispositif pédagogique, quand le cours en a défini un (en situation réelle, itinérance, classe inversée…), est respecté ; une UA n'a en principe qu'un dispositif, les méthodes varient à l'intérieur — `msds-unite-d-apprentissage#04-conception`
Q19. Contenus, objectifs, durée et dispositif viennent de la conception de cours (sommaire des UA) ; l'UA n'a pas à les redire en entier si le sommaire les porte — `msds-unite-d-apprentissage#03-planification p.13`, `msds-le-cours#08-objectifs-d-apprentissage p.15`
Q20. Les conditions cadres et les conditions préalables (sujet, formateurs, apprenants, espace, temps) ont été analysées — `msds-unite-d-apprentissage#03-planification p.14`
Q21. L'UA ménage de la place à l'observation pour les exigences minimales du cours — `msds-unite-d-apprentissage#03-planification p.13`
Q22. Les méthodes sont variées, mais « pas à n'importe quel prix » : adaptées au niveau de maîtrise des apprenants — `msds-unite-d-apprentissage#08-formes-d-enseignement p.27`
Q23. L'UA est relue par une personne extérieure (idéalement expert ou CàF) et les retours sont traités — `msds-unite-d-apprentissage#03-planification p.14`
Q24. L'évaluation de l'UA (apprenants, formateurs, observateurs) alimente l'amélioration du cours et des éditions suivantes — `msds-unite-d-apprentissage#12-evaluer p.37-38`
Q25. Ordre des UA dans le programme du cours : point culminant idéalement présent, même s'il n'est pas toujours facile à placer (mainteneur) — `msds-le-cours#33-annexe-checklist-programme p.65`

Commentaire d'une UA (quand on corrige)
Q26. Le commentaire relève ce qui est positif, de façon concrète (« bien joué » seul est peu convaincant) — `msds-retour-qualifier-accompagner#19-principes-entretien p.43`
Q27. Il nomme des difficultés précises, observables, sans jugement de personne, avec des pistes de solution — `msds-retour-qualifier-accompagner#19-principes-entretien p.43-44`
Q28. Il n'aborde pas trop de points à la fois : on procède par étapes — `msds-retour-qualifier-accompagner#19-principes-entretien p.44`
Q29. Il reste constructif et orienté vers l'avenir ; positif d'abord, puis négatif — `msds-retour-qualifier-accompagner#05-retour p.14-15`

## Critères non officiels

[non officiel] « IFV » : sigle rencontré au cours Top comme structure alternative, abandonné (mainteneur) : ne pas l'enseigner ni le proposer ; s'il apparaît dans un descriptif, demander à l'auteur ce que recouvrent les parties et juger le déroulement. GAG, lui, est sourcé (Q12). (revue CU-03)
[non officiel] Un commentaire est clair et concis (« concis » : aucune source trouvée) ; l'orientation solution et la bienveillance, elles, sont officielles (Q27, Q29). (revue QC-04, QC-02)
[non officiel] Les critères de qualification reprennent le vocabulaire des verbes d'action des UA : l'UA est l'enseignement de ce qui sera observé. (revue CU-12, terrain)
[non officiel] Une compétence se formule en quatre composantes : verbe d'action, objet, contexte, paramètre de qualité (proche de Mager, Q17, qui n'a que trois éléments). (revue CU-20)
[non officiel] Les exercices pratiques (ateliers) d'un cours produisent un livrable réel (circulaire, programme, concept de sécurité) qui sera ensuite noté. (revue CU-21)
[non officiel] La rubrique « Évaluation » de l'UA sert de journal d'amélioration pour l'an prochain ; un bilan des formateurs et des participants de l'édition précédente, des décisions par UA et l'archive de l'ancienne version sont souvent pratiqués. (revue CU-09, CU-10 ; officiel dans le principe, Q24)
[non officiel] Rubriques de façade : « lien avec le thème », « références », « qui », « évaluation » : les signaler quand elles sont vides ou détournées, jamais en non-négociable (le lien au thème est « éventuel » dans la check-list officielle). (terrain)
[non officiel] Dans les canevas Top et J+S cantonal, les rubriques vides sont courantes (références vides dans la moitié des cas, évaluation détournée en to-do) ; ne pas en conclure un défaut du contenu. (terrain)

## Questions à poser avant de juger

1. De quel cours s'agit-il (type, branche, date) ?
2. Le sommaire des UA du cours est-il disponible (durée, niveau, dispositif, objectifs) ?
3. Quel canevas l'équipe utilise-t-elle (Top, J+S cantonal, autre) ?
4. Une exigence minimale du cours est-elle rattachée à cette UA ?
5. L'UA est-elle en préparation (concevoir) ou déjà animée (corriger, avec retours à intégrer) ?

## Pièges

- **PATExE n'est pas « Préparer, Activer, Transmettre, Exercer, Évaluer »** : la brochure verte écrit Présentation, Activation, Transmission, Expérimentation, Évaluation. Ne pas reprendre l'ancienne glose de la revue.
- GAG est une méthode J+S (Q12), pas un sigle interne ; IFV n'est défini nulle part et n'est plus proposé (voir Critères non officiels). Des combinaisons libres de lettres PATExE (« PA », « TExE ») sont fréquentes ; ne pas les corriger si l'ordre se justifie.
- **Demander le sommaire des UA** avant de signaler l'absence de conditions cadres, de niveau taxonomique, de dispositif, de durée ou d'objectifs dans une fiche : le sommaire du cours les porte (`msds-le-cours#08-objectifs-d-apprentissage p.15`). Ne signaler un manque que si ni l'UA ni le sommaire ne le portent.
- Les canevas Top (`autre-canevas-ua-top#01-contenu`) et J+S cantonal (`autre-canevas-point-de-cours-js#01-contenu`) ne demandent ni conditions cadres, ni niveau, ni dispositif ; le J+S cantonal ajoute « Observations pour la qualification » et « Évaluation du point de cours ». Ce sont des formats acceptés ; juger le contenu, pas le formulaire.
- La taxonomie maison à quatre niveaux (0 à 3, équivalents Bloom) ne remplace pas celle du modèle de formation. Traduire en Bloom pour expliquer, sans l'exiger.
- Les équipes citent rarement les brochures MSdS et réinventent leurs critères ; renvoyer aux brochures sans reproche.
- Ne pas confondre le niveau d'approfondissement du contenu (modèle de formation) et le niveau de l'objectif de l'UA : l'objectif détaille le contenu, il ne le change pas.
- Une UA de niveau « Vivre » n'exige pas forcément un descriptif formel avec objectifs Bloom — `msds-le-cours#09-dispositif-pedagogique p.19`.
- Qualification, 80 % de présence et critères éliminatoires : renvoyer au futur référentiel `qualification`. La fiche `cofor-pano-retour-qualifier#01-contenu` montre que, en cours Panorama, la qualification peut être acquise d'office mais que des exigences minimales communiquées au début restent de rigueur.
- Pas de nom de participant ni d'exemple réel dans un commentaire.
- Rubriques de façade vides : un mot au plus, sans les ériger en défaut.
- Hiérarchie des remarques : exigence manquante (N1-N4, d'abord l'écart objectifs ↔ déroulement), information à demander (sommaire), amélioration.

## Trame de conception

1. Partir du sommaire des UA du cours : contenu, objectif, niveau, durée, dispositif — `msds-le-cours#08-objectifs-d-apprentissage p.15`.
2. Analyser sujet, conditions cadres, formateurs, apprenants — `msds-unite-d-apprentissage#03-planification p.14`.
3. Écrire 1 à 3 objectifs d'apprentissage : verbe observable du niveau voulu, réalistes pour la durée (N3, Q13-Q15) ; au niveau « Vivre », un objectif de vécu (Q16).
4. Choisir la structure (PATExE par défaut ; GAG pour une UA technique ou de jeu, Q12), puis une méthode d'animation et une forme sociale par partie (`msds-unite-d-apprentissage#06-formes-sociales`) ; l'Expérimentation reprend le verbe de l'objectif (Q9).
5. Remplir le descriptif selon la check-list (Q1-Q3), dans le canevas du cours (Top, J+S cantonal ou autre) ; matériel, supports, responsabilités, références. Relire chaque partie contre les objectifs : chacun est travaillé puis vérifié quelque part (N4).
6. Prévoir un moment d'observation si une exigence minimale s'y rattache, et une évaluation (Q21, Q24).
7. Faire relire, traiter les retours, animer, évaluer, archiver (Q23, Q24).

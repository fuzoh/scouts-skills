---
slug: concept-de-securite
titre: Concept de sécurité (CdS global de camp, CdS d'activité, CdS de randonnée)
signaux: [concept de sécurité, CdS, analyse des risques, matrice des risques, 3x3, activité à caractère dangereux, réaction en cas d'urgence, ORA, abri de secours, pharmacie, helpline, cellule de crise, tyrolienne, randonnée, baignade]
role: [responsable, responsable de camp, rg, coach-js, formateur]
verbes: [corriger, concevoir, expliquer]
parametres:
  - {nom: type (global de camp | activité | randonnée), obligatoire: true}
  - {nom: date du camp, obligatoire: true}
  - {nom: branche, obligatoire: false}
  - {nom: "domaine de sécurité éventuel (montagne, hiver, eau)", obligatoire: false}
  - {nom: activités dangereuses prévues, obligatoire: false}
canevas: []  # aucun canevas officiel de CdS ; exemple de CdS de randonnée : cudesch-securite#28, fiche d'activité : cudesch-modele-bloc-ac, cudesch-modele-bloc-sc
sources: [msds-exigences-js-2027-camps, autre-canevas-ac-vierge, cudesch-camp-infos-urgence, cudesch-camp-reco-sous-tentes, cudesch-camp-reco-sous-toit, cudesch-cudeschin, cudesch-securite, js-aide-memoire-3x3-en-route, js-aide-memoire-prevention-accidents-sct, js-manuel-sport-de-camp-trekking, js-sdct-camp, js-sdct-eau, js-sdct-hiver, js-sdct-montagne, msds-autorisation-de-camp, msds-hering-camps, msds-reglement-de-camp, msds-thilo]
inclut: []
statut: relu
relu_le: 2026-10-18
---

Un seul référentiel, trois types de livrable choisis par le paramètre `type`, tels que les équipes les distinguent (mainteneur). **CdS global** (ou de camp) : un par camp, rendu au coach avant le camp. **CdS d'activité** : un par activité à risque, ou une section de la fiche d'activité. **CdS de randonnée** : proche du CdS d'activité mais traité à part par les équipes, avec 3x3, carte et dispositif de marche ; toute randonnée en a un. La forme n'est pas imposée : document séparé, annexe ou section de la fiche (`cudesch-securite#23-concept-de-securite-specifique-aux-activites`).

## Non-négociables

Portée : `[G]` CdS global, `[A]` CdS d'activité ou de randonnée, `[G+A]` les deux. Les Q suivent la même convention.

N1. [G] Chaque camp dispose d'un concept de sécurité, établi par écrit. — `msds-reglement-de-camp#01-exigences-camp`, `cudesch-securite#29-concept-de-securite-pour-un-camp`
N2. [G] Le CdS global est remis au coach par écrit avant le camp. — `cudesch-securite#29-concept-de-securite-pour-un-camp`, `js-sdct-camp#11-programme-detaille-securite`
N3. [G] Le CdS global contient les quatre éléments : informations sur le camp, mesures de sécurité générales, préparation à la réaction en cas d'urgence, liste des activités à caractère dangereux. — `cudesch-securite#29-concept-de-securite-pour-un-camp`
N4. [G] La liste des activités à caractère dangereux du camp est présente (elle dit quelles fiches portent un CdS propre). — `cudesch-securite#29-concept-de-securite-pour-un-camp`, `js-sdct-camp#11-programme-detaille-securite`
N5. [G] Les informations de cadre du camp (qui, où, quand, qui joindre) sont présentes, dans le CdS ou dans une annexe qu'il désigne ; le détail attendu est en Q24. — `cudesch-securite#29-concept-de-securite-pour-un-camp` (liste donnée « par exemple » ; allégé, mainteneur). Annexes désignées possibles : feuille d'urgence (`cudesch-camp-infos-urgence#01-contenu`, `fidelity: partial`), reconnaissance du lieu (`cudesch-camp-reco-sous-tentes#01-contenu`, `cudesch-camp-reco-sous-toit#01-contenu`)
N6. [G+A] Chaque mesure répond à un danger concret reconnu au préalable ; le concept ne se réduit pas à une liste de lieux et de numéros. — `cudesch-securite#23-concept-de-securite-specifique-aux-activites`, `js-aide-memoire-prevention-accidents-sct#01-principe-exigences`
N7. [G+A] Le concept répond aux deux questions : quelles mesures contre les dangers reconnus, comment se préparer aux urgences. — `cudesch-securite#23-concept-de-securite-specifique-aux-activites`, `js-manuel-sport-de-camp-trekking#26-encadrer-securite`
N8. [G+A] Les activités à caractère dangereux (randonnées, hiver, eau, corde exigeante, grandes constructions, déplacements sur roues, jeux exigeants) ont chacune un CdS, camp ou non, J+S ou non ; toute randonnée en a un (mainteneur). Les petites activités n'en exigent pas. Constructions : un CdS global pour toutes les constructions de camp suffit en règle générale ; les petites constructions (lavabo) n'en exigent pas ; les mesures de montage, d'utilisation et de tempête d'une grande construction (tour, sarasine) figurent dans ce CdS (aligné sur le cudesch, mainteneur 2026-10-18). — `cudesch-securite#10-quelles-sont-ces-activites-a-caractere`, `cudesch-securite#21-concepts-de-securite`, `cudesch-securite#11-randonnees`
N9. [A] Toute activité à caractère dangereux est précédée d'une reconnaissance du terrain. — `msds-reglement-de-camp#01-exigences-camp`
N10. [A] Activité de corde exigeante (tyrolienne, rappel, pont de corde en hauteur) : une personne disposant d'une grande expérience de l'activité est présente. Ce n'est pas une exigence d'expert J+S. — `cudesch-securite#10-quelles-sont-ces-activites-a-caractere`
N11. [A] Activité sur lac ou rivière : une personne avec module SSS correspondant par tranche de 12 participants ; une personne du camp avec cours de base CPR ou BLS-AED. Exception au seul cours CPR/BLS : baignade en lac sous maître-nageur, jamais en rivière. — `cudesch-securite#13-activites-aquatiques`
N12. [A] Activité dans un domaine de sécurité J+S (montagne, hiver, eau) : planification détaillée avec CdS, lue et autorisée par un expert J+S du domaine, transmise à l'expert par le coach ou par le chef de camp (mainteneur) ; au moins un moniteur avec le complément du domaine ; jeunes de 10 à 20 ans seulement. — `js-aide-memoire-prevention-accidents-sct#01-principe-exigences`, `msds-reglement-de-camp#03-encadrement-autorisation`, `msds-hering-camps#05-d-programme-detaille`
N13. [A] Randonnée dans les Alpes, Préalpes, Jura ou à l'étranger : reconnaissance préalable indispensable, sur le terrain et pas seulement sur carte (mainteneur) ; itinéraire, itinéraires de remplacement et calcul du temps de marche envoyés au coach avec extrait de carte et CdS. — `js-aide-memoire-prevention-accidents-sct#02-montagne`
N14. [G] Les personnes autorisées à conduire en camp sont définies à l'avance. — `msds-reglement-de-camp#02-maitrise-de-camp`
N15. [A] Camp annoncé J+S, marches, trekking ou tours à vélo : itinéraire (extrait de carte), temps de marche, CdS, reconnaissance effectuée, planification selon le 3x3 et programme de mauvais temps sont préparés. — `msds-autorisation-de-camp#01-contenu` (check-list C, que le formulaire qualifie de « pense-bête » ; maintenu en N, mainteneur ; recoupe N9, N13 et Q2, et ajoute le programme de mauvais temps et le temps de marche pour toute randonnée)
N16. [G] Le CdS global nomme le critère d'appel à la cellule de crise, « la maîtrise est dépassée par la situation », et le numéro de la Helpline scoute ; appel obligatoire dès que police ou secours sont intervenus. — `cudesch-securite#37-quand-est-ce-quun-evenement-est` (mainteneur)

## Selon la date

- Camp dès le 01.01.2027 : `msds-exigences-js-2027-camps` ne dit rien du CdS ; les exigences ci-dessus restent celles de `msds-reglement-de-camp`, de `cudesch-securite` et de l'aide-mémoire J+S (édition 10/2025). Le formulaire `msds-autorisation-de-camp` cité est valable jusqu'au 31.12.2026 ; sa version 2027 n'est pas ingérée : ne pas citer ses items pour 2027 sans la lire.
- La brochure `js-sdct-camp` (2014) n'est citée que pour la remise au coach et la liste des activités ; sa partie programme (AC/SC) ne s'applique pas à ce référentiel.
- Le CdS n'est pas lié au type AC/SC ni à l'activité J+S 2027 : même contrôle quelle que soit la date (aucun changement 2027 connu, mainteneur).
- Q7 à Q10 reprennent les rubriques du formulaire d'autorisation 2026 ; les garder pour 2027 et les revérifier quand le formulaire 2027 sera ingéré (mainteneur).

## Critères de qualité

Seuil de lecture. **Conforme** = risques concrets du lieu, de la saison et du groupe, chacun avec une mesure ; préparation à l'urgence applicable par tout responsable ; liste des activités dangereuses avec leur CdS. **À retravailler** = liste de lieux et de numéros sans risque identifié ; risques sans mesure ; clone d'une autre année ou d'un autre camp. Une matrice n'est pas requise pour être conforme.

Q1. [G+A] Les risques sont identifiés concrètement et rattachés à la partie de l'activité ou du camp qui les porte. Un risque général peut rester général ; les risques liés au terrain sont localisés (carte avec les points de danger). — `cudesch-securite#23-concept-de-securite-specifique-aux-activites`
Q2. [G+A] Le 3x3 sert à identifier les dangers (trois facteurs : conditions, terrain, groupe ; trois moments : à la maison, sur place, pendant) ; le CdS répond. — `cudesch-securite#33-la-methode-3-x-3-garder`, `js-aide-memoire-3x3-en-route#01-grille-3x3`, `js-manuel-sport-de-camp-trekking#26-encadrer-securite`
Q3. [G+A] Les mesures couvrent les cinq familles : responsabilités dans la maîtrise, alternatives et critères d'annulation, règles de comportement, équipement, mesures propres à l'activité. — `cudesch-securite#23-concept-de-securite-specifique-aux-activites`
Q4. [G+A] Chaque mesure est assignée à une personne ou un rôle, hors réaction d'urgence. Dans le CdS d'activité, ne pas multiplier les responsables d'une même tâche. — `cudesch-securite#23-concept-de-securite-specifique-aux-activites`
Q5. [G+A] La réaction d'urgence est un schéma applicable par n'importe quel membre de la maîtrise (quoi faire, dans quel ordre, qui appeler), sans noms ; un membre prend la conduite sans s'impliquer dans les secours. — `cudesch-securite#36-agir-en-situation-durgence`
Q6. [G+A] Le matériel d'urgence est prévu : pharmacie (de groupe ou de camp), téléphone chargé avec les numéros des responsables, carte d'urgence de crise ; aide-mémoire J+S en cas d'urgence pour toute activité dangereuse. — `cudesch-securite#23-concept-de-securite-specifique-aux-activites`, `cudesch-securite#36-agir-en-situation-durgence`
Q7. [G] Le CdS décrit accès au lieu, réseau, hôpital, dentiste et pharmacie les plus proches, et un abri de secours disponible, rapidement atteignable, assez grand et sûr. — `cudesch-securite#29-concept-de-securite-pour-un-camp`, `msds-autorisation-de-camp#01-contenu`
Q8. [G] Les mesures générales traitent charte et règles de camp, substances addictives et sanctions, outils, véhicules (conducteurs, assurance de conduite d'un véhicule tiers), tiques, sphère intime, feuilles d'urgence. — `cudesch-securite#29-concept-de-securite-pour-un-camp`, `msds-autorisation-de-camp#01-contenu`
Q9. [G] Hygiène, eau potable et bois en suffisance sont traités ; l'hygiène peut aussi couvrir le volet personnel et réflexif, religieux ou non. — `msds-autorisation-de-camp#01-contenu`
Q10. [G] Les parties les plus exigeantes du camp, les moins captivantes et celles qui risquent de causer peur ou traumatisme ont été identifiées, avec des mesures. — `msds-autorisation-de-camp#01-contenu`
Q11. [G] Une consigne médias (renvoi à la cellule de crise, porte-parole) complète le critère d'appel de N16. — `cudesch-securite#38-contacts-avec-les-medias-en-situation`
Q12. [G+A] Le CdS est connu de toute la maîtrise (équipe cuisine comprise), relu avant la réalisation et reste à portée de main. — `cudesch-securite#22-quest-ce-quun-concept-de-securite`, `js-manuel-sport-de-camp-trekking#26-encadrer-securite`
Q13. [A] Critère d'annulation et alternative fixés avant l'activité et discutés avec le groupe. — `cudesch-securite#23-concept-de-securite-specifique-aux-activites`, `cudesch-securite#28-exemple-concept-de-securite-randonnee`
Q14. [A] Randonnée : points de sortie, de demi-tour et de non-retour, passages clés repérés et reconnus, abris, itinéraire de repli, qui ouvre et ferme la marche, heure limite de demi-retour. — `cudesch-securite#28-exemple-concept-de-securite-randonnee`, `js-sdct-montagne#06-concept-de-securite`, `js-aide-memoire-3x3-en-route#01-grille-3x3`
Q15. [A] Activité de corde : les cinq principes (redondance, quatre yeux, information sur les risques, etc.), règles claires, encadrement étroit, test de l'installation avant usage, corde dédiée. — `cudesch-securite#14-activites-de-corde`
Q16. [G+A] Hiver : cinq règles fondamentales, abri en dur à proximité pour les nuits en tente ou igloo, personne de confiance informée du programme. — `js-aide-memoire-prevention-accidents-sct#03-hiver`, `js-sdct-hiver#13-securite`
Q17. [G+A] Si l'activité est évaluée par classement des risques, utiliser probabilité × ampleur : un risque se définit ainsi, un danger est ce qui peut causer un dommage. — `js-manuel-sport-de-camp-trekking#26-encadrer-securite`, `js-sdct-eau#03-concept-de-securite`
Q18. [G+A] Les activités à risque accru intègrent leur CdS à leur fiche ou le joignent ; la fiche dit où le trouver. — `cudesch-securite#23-concept-de-securite-specifique-aux-activites`, `js-manuel-sport-de-camp-trekking#26-encadrer-securite`, `autre-canevas-ac-vierge#01-contenu`
Q19. [G+A] L'évaluation de l'activité ou du camp reprend la sécurité, en particulier les situations critiques. — `cudesch-securite#34-evaluer-les-activites-a-caractere-dangereux`
Q20. [G+A] Règle de décision générale : en cas de doute, renoncer ou transmettre la responsabilité à une personne compétente ; en cas d'incertitude sur la nécessité d'un CdS, demander au RG ou au coach. — `cudesch-securite#10-quelles-sont-ces-activites-a-caractere`
Q21. [G+A] Le schéma de réaction suit Observer, Réfléchir, Agir (ORA, « feu de signalisation »). — `msds-thilo#05-premiers-secours`, `cudesch-securite#36-agir-en-situation-durgence`
Q22. [A] Le CdS de randonnée (N8) : hors domaine de sécurité il peut rester succinct, dans un domaine ou pour une excursion de montagne difficile il est détaillé. Il décrit les endroits clés et la tactique pour les franchir. — `js-sdct-montagne#06-concept-de-securite`
Q23. [A] Randonnée : plan d'urgence nommant qui alerte, qui soigne, qui encadre les autres ; une pharmacie par groupe ; une personne extérieure (coach) informée de l'itinéraire et de la liste des participants. — `js-sdct-montagne#06-concept-de-securite`, `js-sdct-hiver#13-securite`
Q24. [G] Les informations de cadre (N5) détaillent organisateur, lieu et date, responsable principal et adjoints avec leurs numéros, téléphone d'urgence pour les parents et sources de danger propres aux environs du terrain (cours d'eau, falaise, tiques, feu de forêt). — `cudesch-securite#29-concept-de-securite-pour-un-camp`
Q25. [G] Le CdS global passe en revue les dangers qui ne tiennent à aucune activité : intempéries et orages (foudre, crues), interdictions de feu et risque d'incendie de forêt, substances inflammables et feux d'artifice, animaux de pâturage et sauvages ; seuls ceux qui s'appliquent au lieu et à la saison. — `cudesch-securite#16-autres-dangers`, `cudesch-securite#17-intemperies-et-orages`, `cudesch-securite#18-feu-et-incendie-de-foret`, `cudesch-securite#19-substances-facilement-inflammables-et-feux-dartifice`, `cudesch-securite#20-animaux-de-ferme-et-animaux-sauvages`
Q26. [G+A] Le CdS est adapté pendant la réalisation : une nouvelle évaluation sur place est prévue si la situation change, et la direction est claire (vue d'ensemble, règles claires et appliquées, doutes exprimés dans la maîtrise). — `cudesch-securite#31-realisation-et-evaluation`, `cudesch-securite#32-direction-claire`
Q27. [G+A] Une version courte du CdS (dangers, mesures, préparation à l'urgence) tient à portée de main, avec le schéma d'annonce (où, qui, quoi, quand, combien, autres) et les numéros d'urgence (112, 117, 118, 144, 145, 1414, Helpline scoute : 0800 22 36 39). — `cudesch-cudeschin#08-securite`, `cudesch-cudeschin#10-agir-en-cas-d-urgence`

## Critères non officiels

Jamais bloquants ; à formuler comme conseils ou pratiques.

[non officiel] Le 3x3 « à la maison » est de préférence un tableau de questions auxquelles le CdS répond ; y inscrire directement les mesures est moins lisible mais admis. (revue CS-02, mainteneur)
[non officiel] Les risques sont classés en catégories (terrain, météo, groupe, atypiques) : exemple inspiré du 3x3, classement libre ; ce qui compte est la couverture des risques plausibles, sans lister l'inapplicable ni l'improbable. (revue RG-01)
[non officiel] Règle « risque récurrent au CdS global, risque spécifique au CdS d'activité » : approche générale, très pratiquée. (revue RG-04, terrain)
[non officiel] Fiches plastifiées ORA, 4H, ABCDE distribuées aux responsables : conseillé, selon l'expérience de l'équipe. (revue RG-08)
[non officiel] Annexes typiques et utiles, non exigées : ORA, protocole du patient, pharmacie, Helpline, aide à la décision, « Crise : que faire ? », feuille d'urgence. Ce sont des concepts à couvrir quelque part dans le dossier, pas des documents à exiger. (revue RG-07, terrain)
[non officiel] Signature du CdS par chaque responsable : pratiquée par certains groupes, pas obligatoire ; l'essentiel est que toute l'équipe l'ait vu (copie en voiture et sous la tente). (revue RG-16, RG-18)
[non officiel] Avertissement en tête du CdS pour les activités à risque élevé : activité à risque, personnes compétentes seulement, référent nommé et doubleur. (terrain)
[non officiel] Activité à risque élevé : essais progressifs, liberté de participer, fatigue des responsables prise en compte. (terrain)
[non officiel] Tyrolienne ou activité sur l'eau : CdS d'activité avec matrice des risques recommandé ; randonnée : CdS avec 3x3. (revue CS-09, mainteneur)
[non officiel] Matrice en deux temps (initiale, mesures, finale), trois zones, mesures déplaçant le risque en diagonale, risque résiduel ; zones de tolérance selon l'expérience des responsables. Outil recommandé pour les activités à risque, jamais obligatoire. (terrain)
[non officiel] Le CdS d'activité n'a pas toujours besoin d'une procédure d'urgence propre si le CdS global suffit. (revue CS-03)
[non officiel] Fiche d'activité : mini-analyse des risques (« risque -> mesure ») sans répéter le CdS global, avec renvoi au CdS séparé si nécessaire. (trame cantonale, non officielle)
[non officiel] Randonnée : points numérotés sur la carte reportés dans le profil (coordonnées ou lieux-dits univoques) ; points de profil placés pour qu'aucune cuvette ni bosse ne soit gommée. (revue TK-01, TK-02)
[non officiel] Responsabilités nommées dans tout le CdS sauf la réaction d'urgence ; rubriques d'un CdS d'activité à risque : n° et titre, date, responsables, groupe, lieu, type et domaine, mesures, critère d'annulation, alternative, règles, matériel, gestion de crise (trame cantonale, non officielle).
[non officiel] Un QR code ou un GPS d'itinéraire vers l'hôpital ou la pharmacie peut être suggéré comme outil pratique, jamais exigé. (revue RG-17, mainteneur)

## Pièces d'une randonnée (type = randonnée)

- Carte avec itinéraire, points de danger, de pause, de sortie, de non-retour ; dispositif de marche avec temps calculé et pauses. — `msds-hering-camps#05-d-programme-detaille`, `js-aide-memoire-prevention-accidents-sct#02-montagne`
- CdS de randonnée : 3x3 (identification), puis mesures et urgence ; le 3x3 identifie, le CdS répond.
- Le CdS de randonnée règle : rôles dans la maîtrise (pilote, lampe à l'arrière), règles de comportement, points de sortie et critères de demi-tour, équipement, passages clés ; carte actuelle (1:25 000), papier en secours ; personne extérieure informée du trajet et de l'heure de retour. — `cudesch-securite#11-randonnees`
- Le dispositif de marche accompagne le CdS ; il ne le remplace pas et n'est pas évalué ici (voir `activite-js`).

## Domaines de sécurité (lecture par un expert)

Pour `type = activité` dans un domaine, le CdS est le document que l'expert J+S lit et autorise ; la relecture ne se fait pas en vérifiant la forme mais le contenu suivant.
- **Montagne** : randonnées T1 à T3 admises avec l'expérience requise ; T3 : reconnaissance supplémentaire recommandée ; nuitée au-dessus de la limite de la forêt = domaine. Lire : passages clés, point de non-retour, heure de demi-tour, abris, 3x3 à trois composantes. — `js-aide-memoire-prevention-accidents-sct#02-montagne`, `js-sdct-montagne#06-concept-de-securite`, `cudesch-securite#10-quelles-sont-ces-activites-a-caractere`, `cudesch-securite#11-randonnees` (module montagne pour T3 avec nuitée au-dessus de la limite de la forêt, aussi pour une activité purement scoute)
- **Hiver** : terrain exclu d'avalanche, cinq règles, camp d'hiver dans un bâtiment à accès garanti. Lire : hébergement de secours, personne de contact, échappatoires, plan de marche. — `js-aide-memoire-prevention-accidents-sct#03-hiver`, `js-sdct-hiver#13-securite`, `cudesch-securite#12-activites-hivernales` (module hiver : camp à emplacement retiré sans accès garanti l'hiver, bivouac dans la neige sans maison de camp, grande randonnée exigeante en raquettes ; protection contre le froid, l'humidité et le soleil)
- **Eau** : gilet de flottaison ou de sauvetage selon l'engin ; activité dans ou sur l'eau avec compétences de surveillance ou personne qualifiée. Lire : perception du risque selon les participants, matrice recommandée, exemple coup de soleil. — `js-aide-memoire-prevention-accidents-sct#04-eau`, `js-sdct-eau#03-concept-de-securite`, `cudesch-securite#13-activites-aquatiques` (module SSS lac ou rivière par tranche de 12 participants ; module J+S eau pour bateaux ouverts, radeaux, natation ou trekking en rivière ; la responsabilité reste à la maîtrise même en piscine surveillée)
- Au bord de l'eau ou le long d'un cours d'eau : pas de formation « eau » exigée, mais le groupe n'entre que là où c'est approprié. — `js-aide-memoire-prevention-accidents-sct#04-eau`
- **Grandes constructions** (sarasine, tour) : pas de domaine J+S ; un CdS global pour toutes les constructions suffit en règle générale, un CdS séparé par construction n'est pas exigé (N8) ; mesures au montage et au démontage (distance, assurage en hauteur, outils), à l'utilisation (règles, contrôle quotidien) et par tempête. — `cudesch-securite#15-grandes-constructions-de-pionnier`
- Un camp qui ne comprend aucune activité de domaine est jugé sans expert ; la matrice n'y est pas requise.
- Reconnaissance : sur le terrain, pas seulement sur carte (N13).

## Exemples officiels

Exemples du cudesch, un par type d'activité ; *concevoir* s'en inspire pour la structure, *expliquer* y renvoie, jamais exigés (le contenu de l'exemple n'est pas un critère).
- Camp sous tente : CdS global complet, des informations de camp à la liste des activités dangereuses. — `cudesch-securite#30-exemple-de-concept-de-securite-pour`
- Pont de corde : activité de corde, responsables expérimentés, quatre yeux, test avant usage. — `cudesch-securite#24-exemple-concept-de-securite-pour-un`
- Grand jeu : critères d'annulation, alternative, postes et premiers secours. — `cudesch-securite#25-exemple-concept-de-securite-grand-jeu`
- Sarasine : montage, utilisation et contrôle quotidien d'une grande construction. — `cudesch-securite#26-exemple-concept-de-securite-constructions-de`
- Baignade : encadrement formé SSS, orage, alternative en piscine. — `cudesch-securite#27-exemple-concept-de-securite-activite-baignade`
- Randonnée : encadrement par patrouille, annulation, itinéraire de repli. — `cudesch-securite#28-exemple-concept-de-securite-randonnee`

## Questions à poser avant de juger

1. Quel `type` : global de camp, activité, randonnée ? Quelle date de camp ?
2. Y a-t-il des annexes, un CdS séparé renvoyé par la fiche, une carte ? Les demander avant de conclure à l'absence.
3. Quelles activités à caractère dangereux sont au programme, et lesquelles tombent dans un domaine de sécurité ?
4. Pour la randonnée : cotation, nuitée en altitude, dispositif de marche joint ?

## Pièges

- **Extraction** : une matrice en image, des QR codes, cartes et schémas disparaissent ; cases à cocher (« CdS oui/non », « supportable ? ») perdues en docx et pdf. Ne pas conclure à l'absence ; demander. Les annexes sont souvent des fichiers séparés ; les demander avant de juger. L'ORA du manuel J+S est en image (`js-manuel-sport-de-camp-trekking#27-gestion-securite`) : citer `msds-thilo#05-premiers-secours`.
- **3x3** : lignes « à la maison » non remplies, c'est un défaut (si aucune réponse ni mesure) ; lignes « dans la région » et « pendant », ce sont des questions à poser plus tard, légitimes. Ne pas exiger de résultats d'observation sur place.
- **Liste prise pour analyse** : numéros, hôpital, pharmacie et règles de vie ne répondent à aucun danger. La pharmacie n'est pas un CdS (`cudesch-securite#23-concept-de-securite-specifique-aux-activites`).
- **Clones** : titre « raids » dans un CdS « marches », année précédente, responsables d'un autre camp. Vérifier lieu, dates, effectifs et programme.
- **Gravité** : vocabulaire libre (faible à catastrophique, mineure à majeure…) ; juger la cohérence interne de l'échelle, pas l'étiquette.
- **Variante, remplacement, annulation, point de non-retour** : quatre notions distinctes.
- **Corde** : « personne expérimentée », pas « expert J+S » ; l'expert J+S ne relit que montagne, hiver, eau.
- **Pas exigé** : la matrice, la signature, les QR codes, les annexes en tant que documents.
- **Constructions** : petite construction (lavabo) = pas de CdS spécifique ; toutes les autres = un CdS global des constructions, pas un CdS par construction (N8). Ne pas exiger un CdS d'activité par tour ou sarasine.
- **Données personnelles** : ne jamais citer ni recopier numéros ou noms d'un CdS réel.
- **Base juridique** : le devoir de diligence (planifier soigneusement) fonde l'exigence du CdS ; contexte à rappeler, pas un critère à vérifier (`cudesch-securite#05-devoir-de-diligence`).
- **Inapplicable** : ne pas demander de lister des risques absents du lieu ou de la saison.

## Trame de conception

Procéder dans l'ordre. **Global** : (1) informations de camp, N5 et Q24 ; (2) dangers du terrain et de la saison, localisés (carte) ; (3) mesures générales, Q8 ; (4) préparation à l'urgence : schéma sans noms, numéros, abri, pharmacie, feuilles d'urgence, crise avec critère d'appel et Helpline (N16, Q5-Q7, Q11) ; (5) liste des activités dangereuses et renvoi à leurs CdS (N4) ; dangers hors activité (Q25). **Activité** : (1) type et domaine, cas éventuel d'expert (N12) ; (2) 3x3 pour identifier ; (3) risques, éventuellement classés ; (4) mesures par famille avec responsables (Q3, Q4) ; (5) annulation, alternative, point de non-retour (Q13-Q14) ; (6) urgence propre seulement si le global ne suffit pas. Relire avec toute la maîtrise (Q12) ; prévoir version courte et adaptation sur place (Q26-Q27).

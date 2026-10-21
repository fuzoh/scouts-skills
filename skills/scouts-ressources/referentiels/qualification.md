---
slug: qualification
titre: Système de qualification d'un cours MSdS / J+S (exigences minimales, indicateurs, grille, concept RQA)
signaux: [qualification, système de qualification, qualif, grille de qualification, grille d'évaluation, exigences minimales, exigence minimale, indicateurs, critères d'évaluation, sphères, sphère de compétences, barème, pondération, seuil de réussite, critères éliminatoires, concept RQA, RQA, RQE, fiche de suivi, consignation des observations, attestation de cours, réussi / non réussi, qualification séquencée, qualification en continu, qualification d'office]
role: [formateur, maitrise-de-cours, caf, expert-js]
verbes: [corriger, concevoir, expliquer]
parametres:
  - {nom: type de cours, obligatoire: true}
  - {nom: date du cours, obligatoire: true}
  - {nom: qualification formelle ou acquise d'office, obligatoire: false}
  - {nom: qualification séquencée ou en continu, obligatoire: false}
  - {nom: objectifs de formation retenus par l'équipe, obligatoire: false}
canevas: []
sources: [msds-modele-de-formation, msds-retour-qualifier-accompagner, msds-le-cours, msds-ancre, cofor-administration-cours-federaux, cofor-pano-retour-qualifier, js-communication, js-manuel-experts, autre-conception-qualification-top]
inclut: []
statut: valide
relu_le: 2026-10-21
---

Périmètre : le **système de qualification** d'un cours de formation scout, c'est-à-dire l'instrument écrit avec lequel l'équipe de cours décide « cours réussi » ou « cours non réussi » : exigences minimales et leurs indicateurs, grille d'évaluation, modalités du processus (qui observe, comment on consigne, quand on discute et on s'entretient, remédiations), et le concept RQA (retour, qualification, accompagnement) qui les décrit. Il se corrige (une grille ou un concept joint), se conçoit (à partir des objectifs du cours) et s'explique. La base officielle est la brochure orange `msds-retour-qualifier-accompagner` et le modèle de formation ; J+S ajoute la transparence et le vocabulaire critères / indicateurs / standards. La méthode de construction en huit étapes (objectifs, sphères, critères, indicateurs, barème, pondération, seuil, mise en page) vient du cours Top : elle est non officielle et organise la trame.

**Hors périmètre** : l'UA qui crée la situation d'observation (référentiel `ua`), la conduite de l'entretien et le retour oral (savoir sur le RQA), la décision sur un apprenant réel (elle appartient à l'équipe de cours), le recours (procédure cofor, nommée en Q).

## Non-négociables
Portée : `[tous]` = quelle que soit la date du cours ; `[formel]` = cours qui délivre une qualification ou une reconnaissance (base, RU, Top, modules J+S) ; `[office]` = cours où la qualification est acquise d'office (certains cours Panorama).
N1. [formel] Les exigences minimales sont fixées par la maîtrise **avant** le cours, clairement, et tout le processus de retour, de qualification et d'accompagnement repose sur elles — `msds-modele-de-formation#04-direction-et-encadrement` ; `msds-retour-qualifier-accompagner#06-qualification`.
N2. [tous] Les exigences minimales découlent des objectifs de formation du cours visé, dans la version du modèle applicable à sa date ; des exigences reprises d'une édition précédente sont vérifiées contre cette version ; pour un cours Panorama à qualification d'office, elles peuvent aussi porter sur la participation active et le vivre-ensemble, seuls ou avec les objectifs de formation (N8) — `msds-retour-qualifier-accompagner#06-qualification` ; `msds-retour-qualifier-accompagner#10-exigences-minimales` ; `msds-modele-de-formation#04-direction-et-encadrement` ; `cofor-pano-retour-qualifier#01-contenu`.
N3. [tous] Chaque exigence minimale porte des indicateurs observables, compréhensibles par toute l'équipe et pertinents, en général deux à quatre ; une exigence sans indicateur n'est pas évaluable — `msds-retour-qualifier-accompagner#06-qualification`.
N4. [tous] Chaque exigence minimale est associée à une situation d'observation du cours, et les contenus correspondants sont enseignés avant d'être évalués ; pour les exigences de participation active et de vivre-ensemble d'un Panorama à qualification d'office, l'observation peut relever de la vie du cours plutôt que d'une UA particulière — `msds-retour-qualifier-accompagner#06-qualification` ; `msds-retour-qualifier-accompagner#12-programme-et-inscription` ; `cofor-pano-retour-qualifier#01-contenu`.
N5. [tous] Les exigences minimales sont mises à disposition par écrit ; elles sont communiquées aux apprenants au début du cours avec leurs indicateurs, les critères d'évaluation, les personnes concernées et les conséquences possibles du processus — `msds-retour-qualifier-accompagner#06-qualification` ; `msds-retour-qualifier-accompagner#14-pendant-le-cours` ; `js-communication#37-qualifier` ; `js-manuel-experts#11-evaluer-qualifier`.
N6. [formel] La décision « réussi / non réussi » se prend sur la base des exigences minimales, **chacune satisfaite individuellement** : une faiblesse dans un domaine ne se compense pas par un très bon travail ailleurs ; la maîtrise décide en commun, dernier mot à la direction de cours — `msds-retour-qualifier-accompagner#15-discussion-de-qualification` ; `msds-modele-de-formation#04-direction-et-encadrement`. Conséquence pour l'instrument (mainteneur) : une moyenne, une pondération ou un seuil global ne peut pas rendre « réussi » un apprenant dont une exigence minimale n'est pas remplie ; l'agrégation sert à nuancer, pas à compenser.
N7. [formel] Pour les cours fédéraux, une absence autorisée suppose une présence à au moins 80 % de chaque partie et à toutes les parties définies comme fondamentales par la direction ; pour tout cours J+S, la présence effective respecte la durée minimale J+S malgré l'absence — `cofor-administration-cours-federaux#04-confirmation-finances` ; `msds-ancre#16-presences-et-qualifications`.
N8. [office] Même quand la qualification est acquise d'office, la maîtrise définit des exigences minimales de réussite (objectifs de formation et/ou participation active et vivre-ensemble) et les communique à tous au début du cours ; observations, retours et accompagnement restent dus — `cofor-pano-retour-qualifier#01-contenu`.
N9. [tous] Les exigences minimales portent sur ce qui peut évoluer pendant le cours (aptitudes, compétences, connaissances), jamais sur des traits stables de personnalité ; un trait ne s'observe qu'à travers des comportements, et l'observation se distingue de l'interprétation — `msds-retour-qualifier-accompagner#09-avant-le-cours` ; `msds-retour-qualifier-accompagner#04-observer`.

## Selon la date

Demander la date du cours. Le modèle de formation 2027 est en vigueur le 01.01.2027 : la numérotation et la formulation des objectifs de formation changent, donc les exigences minimales qui en découlent (N2). La brochure orange disponible est une version de travail de 2026 : son applicabilité historique n'est pas certifiée par le registre. Le modèle antérieur à 2027 est absent du corpus ; demander le descriptif applicable pour vérifier un ancien cours.

| | Cours avant le 01.01.2027 | Cours dès le 01.01.2027 |
|---|---|---|
| Objectifs de base | modèle de formation précédent, objectifs numérotés de l'ancien descriptif | modèle de formation 2027 (`savoirs` du cours visé) |
| Vocabulaire | participant·e, point de cours, RQE (retour, qualifier, encourager) acceptés | apprenant·e, UA, RQA (accompagner) ; les deux se lisent, aucun n'est corrigé |
| Grille héritée | admise si elle cite le modèle en vigueur à la date du cours | une grille sur les anciens numéros d'objectifs est à faire migrer (N2) |

## Critères de qualité

Concept et exigences minimales
Q1. Le processus RQA est décrit dans un concept écrit, discuté par toute l'équipe avant le cours, avec les tâches réparties : exigences minimales, consignation, moments de discussion, entretiens, remédiations, situations d'observation, consignes données aux apprenants — `msds-retour-qualifier-accompagner#09-avant-le-cours`.
Q2. Le nombre d'exigences minimales reste raisonnable : moins de situations d'observation explicites, moins de pression sur les apprenants, moins de charge pour l'équipe — `msds-retour-qualifier-accompagner#06-qualification`.
Q3. Chaque exigence minimale est formulée clairement, sans ambiguïté, avec une attente réaliste et un niveau taxonomique identifié — `msds-retour-qualifier-accompagner#06-qualification`.
Q4. Les objectifs de formation sont pondérés en équipe avant d'en déduire les exigences (fiches et pastilles, travail préparatoire individuel, petits groupes par thème, retour sur les cours précédents) ; tous les objectifs ne donnent pas une exigence — `msds-retour-qualifier-accompagner#10-exigences-minimales` ; `msds-retour-qualifier-accompagner#06-qualification`.
Q5. Les indicateurs répondent aux questions de la brochure : ce qu'une personne extérieure verrait, ce qui doit au minimum être présent, ce qui distingue rempli de non rempli, ce qui est reproductible et non dû au hasard, ce qui se compte ou se mesure, ce que signifient « complet » ou « connaît » — `msds-retour-qualifier-accompagner#10-exigences-minimales`.
Q6. Même quand l'association cantonale impose le système, l'équipe discute chaque critère pour en avoir une compréhension commune avant le cours — `msds-retour-qualifier-accompagner#06-qualification`.

Grille et consignation
Q7. La grille d'évaluation reprend les exigences minimales en points décrits (savoirs, savoir-faire, savoir-être), avec une échelle d'atteinte (par exemple atteint / partiellement atteint / à améliorer), une grille par exigence minimale ; elle rend transparent ce qu'il faut pour réussir — `msds-retour-qualifier-accompagner#10-exigences-minimales`.
Q8. Le mode de consignation est choisi avant le cours (fiche de suivi, dossiers, affiche, cahier, tableau numérique, outil en ligne), avec ses limites connues ; chaque observation est neutre, datée ou rattachée à une UA, avec identification de son auteur ; les notes collectives affichées pour l'équipe restent inaccessibles aux apprenants, et les observations pertinentes sont sélectionnées pour le retour — `msds-retour-qualifier-accompagner#11-consignation-des-observations`.
Q9. Au moins deux formateurs observent chaque apprenant, en combinant observations occasionnelles et systématiques décidées avant le cours ; les intuitions sont signalées comme telles — `msds-retour-qualifier-accompagner#03-observations` ; `msds-retour-qualifier-accompagner#04-observer`.
Q10. Transparence au sens J+S : objectifs, critères, indicateurs et, quand c'est possible, standards connus d'avance ; en formation de moniteurs, les critères de base sont les compétences personnelle, sociale, méthodologique et professionnelle ; là où un standard est impossible (qualité d'une leçon, empathie), la part de subjectivité est assumée et dite — `js-communication#38-processus-de-qualification`.

Programme et organisation
Q11. Le choix entre qualification séquencée et en continu est explicite, avec ses conséquences sur le programme (longues réunions à mi-cours et en fin de cours, ou plusieurs courtes réunions et retours brefs) — `msds-retour-qualifier-accompagner#06-qualification`.
Q12. Le programme prévoit les créneaux du processus : discussions d'équipe (dix minutes par apprenant font quatre heures pour vingt-quatre), retours, saisie des observations, remédiations avant l'entretien intermédiaire ou final, avec une nouvelle plage d'enseignement avant toute remédiation — `msds-retour-qualifier-accompagner#12-programme-et-inscription` ; `msds-retour-qualifier-accompagner#15-discussion-de-qualification`.
Q13. Les discussions de qualification sont préparées et animées : rôles (animation, procès-verbal, temps, responsable des exigences minimales, climat), méthode de décision aussi objective que possible, cas difficiles en équipe complète seulement, droit de veto des experts — `msds-retour-qualifier-accompagner#15-discussion-de-qualification`.
Q14. Un apprenant qui risque l'échec reçoit un entretien intermédiaire structuré, avec remédiation fixée ensemble ; l'instance recommandante est informée — `msds-retour-qualifier-accompagner#15-discussion-de-qualification` ; `msds-retour-qualifier-accompagner#17-entretien-intermediaire`.
Q15. L'équipe est formée au RQA avant ou pendant le cours (exigences minimales, observation, entretiens, mauvaises nouvelles) — `msds-retour-qualifier-accompagner#13-former-l-equipe`.
Q16. Le système de qualification fait partie de la conception du cours (dernière étape du processus en sept étapes) et passe par les contrôles qualité : comparaison avec les éditions précédentes, relecture croisée, regard du CàF, cohérence avec le modèle de formation et les cadres de référence J+S — `msds-le-cours#10-systeme-de-qualification`.

Après le cours
Q17. Le processus RQA est évalué après le cours (préparation de l'équipe, observation, outils, exigences minimales, discussions, entretiens), avec les apprenants aussi ; les décisions prises ne sont pas rouvertes — `msds-retour-qualifier-accompagner#26-apres-le-cours`.
Q18. La procédure est documentée et conservable : un recours écrit à la CoFor ne porte que sur la procédure, jamais sur la décision ; pour un cours J+S, recours possible auprès de J+S via le secrétariat général ; les données liées aux qualifications sont conservées au moins quatre mois après la fin du cours, mises à disposition de l'instance de recours en cas de recours, puis détruites à la fin de ce délai selon l'Ancre — `cofor-administration-cours-federaux#05-recours-crise-combinaisons` ; `msds-ancre#17-buts-retour-archivage`.
Q19. Les décisions, recommandations et retours sont transmis à l'association cantonale, la qualification saisie dans MiData (cours réussi coché, non réussi laissé vide), la reconnaissance J+S confirmée par la BDNS — `msds-retour-qualifier-accompagner#26-apres-le-cours` ; `msds-ancre#16-presences-et-qualifications`.

Information et présence
Q20. Il est utile de présenter dès le début du cours les moments, le contenu, la forme et la durée des entretiens ; ces détails d'organisation complètent la transparence exigée en N5 — `msds-retour-qualifier-accompagner#14-pendant-le-cours`.
Q21. L'Ancre conseille une présence à au moins 80 % du cours ; ce conseil général se distingue de l'obligation portant sur chaque partie des cours fédéraux et de la durée minimale J+S (N7) — `msds-ancre#16-presences-et-qualifications`.

## Critères non officiels
Origine : support du cours Top `autre-conception-qualification-top#01-contenu`, grilles de cours Top et RU vues par le mainteneur (non ingérées), mainteneur.
[non officiel] La construction suit huit étapes dans l'ordre : objectifs → sphères → critères → indicateurs → barème → pondération → seuil de réussite → mise en page ; chaque étape se vérifie contre la précédente (cours Top).
[non officiel] Un objectif de formation trop large est reformulé ou découpé pour devenir évaluable (« planifier, réaliser et évaluer une randonnée » devient trois objectifs de qualification), en gardant le renvoi au numéro de l'objectif d'origine (cours Top).
[non officiel] Les **sphères** regroupent les objectifs par thème général du cours (but du cours, module, exercice pratique, regroupement de contenus) ; le poids des sphères les unes par rapport aux autres est explicité et cohérent avec l'importance que le modèle de formation donne à ces objectifs (cours Top, grille Top).
[non officiel] Un **critère** dit ce que l'équipe attend de l'apprenant pour qualifier l'objectif ; un **indicateur** dit ce qu'on observe pour conclure que le critère est rempli. Un critère sans indicateur se juge à l'impression ; un indicateur sans critère ne se rattache à aucun objectif (cours Top).
[non officiel] La précision des critères et des indicateurs est adaptée au barème : un barème binaire (OK/KO) exige des indicateurs tranchés, une échelle à cinq niveaux exige que chaque niveau soit défini par écrit ; une case vide signifie « non observé », jamais zéro (grilles Top et RU).
[non officiel] La pondération (fractions, nombres, pour cent) est écrite dans la grille et justifiée en une ligne ; les seuils de réussite (par objectif, par sphère, pour le cours) sont réalistes et explicités avant le cours ; un seuil par sphère ne remplace pas l'examen de chaque exigence minimale (N6) (cours Top, mainteneur).
[non officiel] Le support est agréable et pratique pour l'équipe, lisible et compréhensible pour l'équipe et les apprenants, avec des zones de commentaires et une zone de synthèse ; l'équipe décide avant le cours ce qui est affiché et ce qui est remis à l'apprenant (cours Top).
[non officiel] Le support est compréhensible par une personne externe à la maîtrise (CàF, recours) et facilite la préparation du retour (grille Top).
[non officiel] Les **critères éliminatoires** (présence, règles du cours et charte J+S, plagiat, délais, attitude passive, mise en danger) sont listés d'avance, connus des apprenants, et leur activation est justifiée par écrit (quand l'avertissement a été donné, quels faits) ; sauf infraction aux règles du cours, une élimination ne vient qu'après avertissement et objectifs d'amélioration fixés ensemble. Seules la présence (N7) et les règles du cours ont une base officielle ; le reste est une pratique de cours (grilles Top et RU, mainteneur).
[non officiel] Un ajustement discrétionnaire de l'équipe (« joker » d'un demi-point sur une sphère) est au plus unique, écrit et motivé, et ne sert jamais à contourner une exigence minimale non remplie (grille RU, mainteneur).
[non officiel] Pour l'exercice de conception du cours Top, le rendu demandé comprend une sphère entièrement détaillée (objectifs, critères, indicateurs, barème, pondération, seuil) et une page de synthèse qui porte la pondération des sphères et le seuil de réussite du cours ; un système opérationnel doit permettre d'évaluer toutes ses exigences minimales (cours Top, mainteneur).
[non officiel] Une grille construite dans un tableur sépare les feuilles de saisie (une par sphère) de la feuille de synthèse, et isole les colonnes techniques hors de la zone d'impression (grilles Top et RU ; détail dans le savoir sur la construction de la grille).

## Questions à poser avant de juger
1. De quel cours s'agit-il (type, branche, date) ? Le jeu d'objectifs est-il celui du modèle de formation en vigueur à cette date ?
2. La qualification est-elle formelle ou acquise d'office ? Séquencée ou en continu ?
3. Quels objectifs de formation l'équipe a-t-elle retenus, et comment les a-t-elle pondérés ?
4. Quelle situation (UA, exercice pratique ou vie du cours pour les exigences de participation et de vivre-ensemble d'un Panorama à qualification d'office) permet d'observer chaque exigence minimale ?
5. Le concept RQA (qui observe, consignation, moments de discussion, entretiens, remédiations) existe-t-il à côté de la grille ?
6. Le système est-il imposé par l'association cantonale ou propre à l'équipe ?

## Pièges
- **Compensation.** Une moyenne de sphère à 80 % peut masquer une exigence minimale non remplie ; la brochure interdit la compensation entre domaines (N6). Lire la grille exigence par exigence avant de lire les totaux. Une sphère entière peut être l'exigence minimale si l'équipe l'a décidé et écrit ainsi ; sinon chaque exigence listée compte seule.
- **Objectifs non observables.** « Connaissent », « comprennent », « sont sensibilisés » ne suffisent pas seuls : vérifier les indicateurs observables (Q5), les préciser ou reformuler si nécessaire. Des indicateurs suffisants permettent de conserver le verbe de l'objectif officiel.
- **Traits de personnalité.** Une rubrique « posture » ou « attitude » (fidèle, serviable, image d'exemple) qui note la personne plutôt que des comportements datés sort du cadre (N9). La garder comme support d'accompagnement, sans la faire peser sur la décision, ou la réécrire en comportements observables.
- **Ancien modèle.** Des objectifs numérotés d'un descriptif antérieur sur un cours 2027 : signaler la migration à faire (N2), sans juger la grille inutilisable.
- **D'office n'est pas sans RQA.** Un cours Panorama sans grille reste tenu aux exigences minimales communiquées et aux retours (N8).
- **80 %.** L'Ancre conseille 80 % du cours (Q21) ; seules les directives des cours fédéraux imposent 80 % de chaque partie et la présence aux parties fondamentales (N7). Pour tout cours J+S, la durée minimale de présence effective reste exigée. Une absence autorisée reste comptabilisée ; une remédiation ne dispense pas des exigences de présence applicables.
- **Standards impossibles.** Toute compétence ne se mesure pas (Q10) : la part de subjectivité se dit à l'avance, elle ne se cache pas derrière une note.
- **Photographie du cours.** La qualification juge le travail fourni pendant le cours, pas la personne ni son parcours ; une rubrique « potentiel » appartient à l'accompagnement.
- **Vocabulaire.** « Sphère », « barème », « pondération », « critère éliminatoire », « joker » ne sont pas des termes des brochures : les reconnaître sans les exiger. RQE / RQA, participant / apprenant, point de cours / UA : les deux se lisent.
- **Critères éliminatoires.** Hors présence et règles du cours, aucune source ne les fonde : les accepter comme pratique annoncée d'avance, ne jamais les présenter comme une règle MSdS ou J+S.
- **Excel ne décide pas.** Une formule qui écrit « Réussi » est un indicateur de synthèse ; la décision est celle de l'équipe en discussion, dernier mot à la direction (N6).
- **Recours.** La CoFor vérifie la procédure, pas la décision : un concept écrit, des observations datées et signées, des avertissements tracés protègent l'équipe et l'apprenant (Q18).
- Pas de nom d'apprenant ni de cas réel dans un retour sur une grille ; les exemples de la grille (« Toto Tutu ») restent des exemples.

## Trame de conception
1. Cadre : type de cours, date, modèle de formation applicable, qualification formelle ou d'office, séquencée ou en continu (Q11), système cantonal imposé ou non (Q6).
2. Objectifs retenus : pondération en équipe (Q4), choix d'un nombre raisonnable (Q2), reformulation ou découpage pour les rendre évaluables*, renvoi au numéro d'origine, niveau taxonomique (Q3).
3. Regroupement en sphères* : thème, but, module ou exercice pratique ; poids relatif des sphères et justification*.
4. Exigences minimales : une phrase chacune (N1, N2), rattachée à sa situation d'observation et, pour les contenus à enseigner, à l'UA qui précède l'évaluation ; participation et vivre-ensemble en Panorama à qualification d'office peuvent s'observer dans la vie du cours (N4).
5. Indicateurs : généralement deux à quatre par exigence (N3), passés aux questions de la brochure (Q5) ; critères intermédiaires si le barème le demande*.
6. Grille : échelle d'atteinte dont chaque niveau est défini (Q7) ; barème*, pondération* et seuils* écrits avec leur justification, sans compensation d'une exigence minimale (N6).
7. Modalités : qui observe qui (Q9), consignation (Q8), moments et rôles des discussions (Q12, Q13), entretiens (moments, forme, durée), remédiations et plages d'enseignement avant (Q12), ce qui est communiqué au début du cours et sous quelle forme (N5).
8. Présence et critères éliminatoires* : règle de présence (N7), liste annoncée, avertissement et justification écrite*.
9. Page de synthèse* : pondération des sphères, seuil du cours, zones de commentaires, décision et signature ; attestation* si l'équipe en remet une.
10. Avant le cours : formation de l'équipe (Q15), contrôle qualité et regard du CàF (Q16) ; après : évaluation du processus (Q17), transmission et saisie (Q19), archivage (Q18).

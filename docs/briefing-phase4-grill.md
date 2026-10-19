# Briefing Phase 4 — grill sur l'organisation des skills (2026-10-17)

Entrées : `GOALS.md`, `idées.md`, `docs/canevas-inventaire.md`, `docs/taxonomie.md`, `ancien skills/`, revue externe (arbitrages en tête de `DECISIONS.md`).

## Tour 1 — réponses du mainteneur (verbatim condensé)

- **Idée générale** : un système polyvalent ; les équipes de formation, les maîtrises et les responsables d'activités ont un set de skills qui permet de travailler sur à peu près tous les éléments importants du scoutisme.
- **Deux types de skills se dessinent** : (1) des skills axés sur l'**accès aux données**, pour qu'un agent trouve les ressources et base son travail sur les documents ; (2) des skills axés sur le **travail / les process** : correction d'activité, écriture de point de cours, recherche, planification, conception de cours, d'UA, de système de qualification… « Je ne sais pas trop comment organiser tout cela, mais plusieurs types de skills se dessinent. Il faudrait explorer les ressources pour comprendre sur quoi ces skills seraient utiles. »
- **cudesch** : intégrer les contenus du cudesch (à obtenir sur le web), centraux dans la méthodologie scoute.
- **Parties hors sources** : certains skills doivent intégrer des éléments qui ne viennent pas des sources (ex. check-list de correction), que le mainteneur veut pouvoir adapter.
- **Au-delà du corpus** : les skills de correction/travail doivent pouvoir sortir des ressources scoutes, typiquement vérifier des théories avant de les expliquer dans un cours.
- **Axe de découpage (tâche vs rôle vs domaine)** : pas tranché. « Il faut réfléchir aux usages que pourraient en avoir les membres du scoutisme pour déduire la meilleure approche. »
- **Points d'entrée par public** : pas convaincu. Le prompt de l'utilisateur devrait suffire à savoir quel niveau de ressources est impliqué ; souvent c'est un mix.
- **Trois modes par skill (corriger / concevoir / expliquer)** : « pourquoi pas, à réfléchir si c'est le mieux ».
- **Plateformes** : « il faudrait que ça marche partout ». Le mainteneur testera des zips avec un prompt de test.
- **Autoportance** : ok. « On doit aussi pouvoir avoir un skill qui en invoque un autre. »
- **Structure des retours** : oui à une méthode commune, moins formelle que proposé, pour que la correction soit faite de la même manière entre documents. **Plusieurs niveaux de correction** : parfois juste un avis global ; éviter la correction trop pointilleuse et verbeuse.

## Demande
Plusieurs sous-agents imaginent des découpages/types de skills différents ; on pioche ensuite les bonnes idées.

## Travail lancé après le tour 1 (2026-10-17)

- Trois propositions d'organisation écrites par sous-agents, à piocher : `docs/propositions/orga-A-usages.md` (9 skills : une bibliothèque `corpus-scout` + 8 ateliers par livrable, socle méthode injecté par build), `orga-B-couches.md` (7 skills : couche sources `scout-sources`/`scout-verifier` + 5 process ; méthode et canevas = modules copiés), `orga-C-minimal.md` (un seul skill `scout` à 4 verbes, canevas dans `canevas/`, packs par domaine, échelle de bascule en 4 crans avant un skill dédié).
- Faits : `docs/contraintes-plateformes.md` (claude.ai, Gemini et ChatGPT acceptent des skills SKILL.md natifs ; pack aplati nécessaire seulement pour Claude Project et custom GPT ; description ≤ 1024 car., corps < 500 lignes, pas d'invocation entre skills dans la spec), `docs/propositions/cudesch-ecart.md` (le cudesch est numérique et public sur cudesch.scout.ch/fr, 12 livres ; aucune brochure de chapitre dans le corpus ; 30 manquants), `docs/canevas-inventaire.md` (26 canevas, 14 avec liste explicite d'exigences).
- Agent Herdr `cudesch` (workspace w8, branche `cudesch` depuis `85ded71`) : ingère et indexe le cudesch, consigne reçue de prendre le cudesch numérique comme version de référence (PDF 2018 en `history`). Rapport attendu dans `docs/cudesch-rapport.md` sur sa branche ; à fusionner dans `main` (il ne touche ni scripts, ni ROADMAP/DECISIONS/METHODE).
- Phase 3b livrée et commitée (`85ded71`) : voir ROADMAP.

## Synthèse des propositions

**Convergences (A, B, C indépendamment)**
- Canevas = données de premier rang, un fichier par livrable, critères pondérés et cités par `id`, ou étiquetés maison ; variantes datées (camp 2026 / 2027) dans le canevas.
- Méthode de correction commune, non déclenchable : trois niveaux, bloquants toujours affichés, trois catégories de remarques.
- Pas de point d'entrée par public : le livrable commande le routage ; sans livrable → recherche dans le corpus.
- Invocation entre skills par le nom quand possible, mais `build` copie toujours les dépendances (la spec ne garantit rien).
- Hors corpus : bloc séparé, citation `[web]`, une prescription J+S/MSdS prime sur le web.
- Pilote : bloc J+S (AC/SC) + UA, avec un cas daté 2027.

**Divergence** : nombre de skills. A = 9, B = 7, C = 1. Argument de C : autoportance → chaque skill embarque le corpus (7-9 copies de 5 Mo) ; prompts mixtes → changement de skill. Argument de A/B : une description par livrable déclenche plus sûrement, packs plus petits.

## Tour 2 — questions et réponses (2026-10-17)

Format : question, puis ➡️ recommandation. « Oui » accepte la recommandation.

1. **Canevas comme données de premier rang** : dossier `canevas/<slug>.md` à la racine, validé par `just check`. Frontmatter : slug, signaux de détection, rôle, verbes, paramètres (date, branche, variante), `sources:` en `id#section`, `inclut:` (sous-canevas). Corps : non-négociables N1..Nk chacun cité, règles selon la date, critères de qualité cités, critères maison `[maison]`, pièges, trame de conception. `check` refuse un non-négociable sans citation et signale les canevas touchés quand une source change de version. ➡️ Oui.
2. **Nombre de skills pour le pilote** : partir de C, un seul skill `scout` (chercher, expliquer, corriger, concevoir) avec catalogue de canevas dans son corps, et une échelle de bascule : canevas → canevas avec procédure → non-négociables recopiés dans le corps du skill → skill dédié. Un atelier dédié (à la A/B) n'est créé que si le pilote montre que `scout` rate le canevas ou se déclenche mal. ➡️ Oui pour le pilote ; repli = découpage par livrable de A, sans jeter les canevas.
3. **Méthode et niveaux** : *avis* (≤ 8 lignes : verdict, non-négociables en échec, deux leviers), *revue* par défaut (≤ 40 lignes : tableau N1..Nk ✓/✗/?, 3 à 5 priorités classées exigence non satisfaite / information manquante / amélioration, format constat → règle citée → correction), *détaillé* sur demande. Non-négociable en échec visible à tous les niveaux. Ligne de plan affichée avant la réponse (canevas détectés, verbes, paramètres, règles datées), corrigeable d'un mot. Ton factuel, sans flatterie. ➡️ Oui, revue par défaut, avis sur mot-clé.
4. **Sortie du corpus** : hiérarchie prescription datée > recommandation > exemple > web (`[web] titre, url, consulté le`) > connaissance du modèle « non vérifié ». Déclencheur obligatoire : toute théorie pédagogique/psychologique d'un document à corriger absente du corpus. Bloc « Hors corpus » séparé, jamais `id@version`. Sans web : « non vérifié, à contrôler ». ➡️ Oui.
5. **Parties adaptables** : `references/maison.md` (ton, niveau par défaut, longueur, critères globaux) et section `[maison]` de chaque canevas ; étiquette `[maison]` dans la sortie, jamais non-négociable. ➡️ Oui.
6. **Packs** : (a) zip skill agentskills.io avec corpus complet pour Claude Code, claude.ai Skills, Gemini Skills, ChatGPT Skills ; (b) pack aplati (instructions courtes + fichiers, canevas en premier, chaque section précédée de sa citation) pour Claude Project et custom GPT, découpé par domaine `camp` (≈ 1,6 Mo) et `formation` (≈ 2,8 Mo), catalogue des sections absentes ; `build --check-limits`. Le mainteneur teste zips et packs avec un prompt de test fourni. ➡️ Oui.
7. **Pilote** : `scout` avec trois canevas `bloc-js` (remplace AC et SC), `ua` (remplace UA), `programme-camp` (cas 2027). Jeu d'essai : 12-15 documents réels (dont un daté 2026 et un 2027), 5 prompts mixtes, 3 questions de théorie dont un neuromythe. Contre-épreuve : retirer un ou deux non-négociables connus par document. Mesures : rappel des non-négociables retirés, citations vérifiables par script, zéro règle inventée, longueur par niveau, stabilité sur trois passages, comparaison aux anciens prompts. Question ouverte : le mainteneur a-t-il des documents réels ? ➡️ Oui au périmètre ; sinon cas fabriqués depuis les exemples J+S du corpus.
8. **Préalables corpus** : ingérer le modèle de descriptif d'activité J+S (jsle.ch/fA22) et la liste de contrôle de l'autorisation de camp (p.2 du formulaire MSdS) ; `verified` ciblé sur les sections citées par les trois canevas. ➡️ Oui.
9. **cudesch numérique comme référence** : une source `cudesch-<livre>` par livre, version courante = site, PDF 2018 en `history`, PDF pfadi.swiss ingéré seulement sans équivalent numérique. Consigne déjà envoyée à l'agent Herdr (réversible). ➡️ Oui.
10. **Applicabilité, restes** : (a) six sources datées `2027-01-01` par déduction (cinq check-lists cofor, exigences J+S 2027 camps) : garder avec mention « déduite » ; (b) Ancre, Pilote, Ticket : `nature: prescription` sans date ; (c) charte de cours J+S : `exemple` ; (d) le reste sans nature. ➡️ Oui à (a)-(d).

**Réponses du mainteneur (verbatim condensé)**
1. « Je ne suis pas sûr que canevas soit le bon terme. Ce qu'on appelle des canevas aux scouts, ce sont des documents vierges prêts à être complétés, comme un template. Il faudra que je t'en montre. » Fond accepté, nom à changer → Q11.
2. ok. 3. ok. 4. ok.
5. « Bonne idée, je ne sais pas si maison est le bon terme. » Fond accepté, nom à changer → Q13.
6. ok. 7. ok.
8. « C'est une idée, il faudra relire. Voir aussi ce que j'avais fait dans les anciennes Gems Gemini. Attention : en 2027 on ne parle plus d'AC/SC mais d'activité J+S avec des parties sportives ou non. » → Q14, Q19.
9. « Voir ce que l'agent cudesch (worktree séparé) trouvera. » En attente.
10. ok.

## Faits vérifiés avant le tour 3 (corpus, 2026-10-17)

- **« canevas » est pris** : `msds-le-cours` (§ thème et fil rouge, § évaluer) et `msds-unite-d-apprentissage` (§ évaluer) emploient « canevas » pour le modèle vierge d'UA à remplir. Nos fichiers de critères prennent un autre nom.
- **Vocabulaire 2027** : `js-manuel-sport-de-camp-trekking` (édition du 16.10.2026) ne contient aucun « AC » ni « SC ». Seul `js-sdct-camp` (2014) les utilise encore. `msds-exigences-js-2027-camps` et `msds-essentiel-msds-js-2027` §02 parlent d'« activité J+S » (≥ 30 min, deux périodes par jour, « actif et axé sur le mouvement »), de « formes caractéristiques » et « formes d'activité », et d'une « activité sportive » comptée dès 30 min par tranches de 15 min, séparément par activité.
- **Anciens prompts Gemini** (`ancien skills/`) : trois prompts seuls, pas de fichiers joints dans le dépôt. Critères non sourcés qui en viennent : originalité, variantes, activité de remplacement, domaines AC (plein air, sécurité, nature, pionnier, campement, prévention) et SC (itinérant, sports, jeux).
- Agent Herdr `cudesch` (pane w8:p1) : toujours en cours, rien d'écrit dans son worktree au moment du tour 3.

## Tour 3 — questions et réponses (2026-10-17)

11. **Nom des fichiers de critères** : `référentiel`, dossier `referentiels/<slug>.md` (« grille » écarté : grille horaire et grille d'observation sont des livrables). ➡️ ok.
12. **Canevas réels du mainteneur** : déposés dans `documents/`, ingérés comme sources `nature: exemple` ; chaque référentiel pointe son canevas officiel par `id` ; *concevoir* produit dans la structure du canevas. ➡️ « Oui, dans une prochaine phase ; je déposerai plusieurs types, des vides et des remplis, pour qu'une analyse puisse être menée. » Fichiers joints des anciens Gems : pas de réponse, à confirmer.
13. **Étiquette des critères non officiels** : `[non officiel]` dans la sortie, section `## Critères non officiels` dans chaque référentiel, fichier global `references/reglages.md` (ton, niveau par défaut, longueur). ➡️ ok.
14. **Référentiel `activite-js`** (remplace `bloc-js`) : corps 2027 (activité J+S, part sportive comptée, formes caractéristiques et d'activité, deux périodes), jeu 2026 court (AC/SC et domaines, `js-sdct-camp`) ; anciens critères en `[non officiel]` ; date du camp = paramètre obligatoire. ➡️ « Oui, on vise le plus à jour. »
15. **Situations sans livrable** : pas de cinquième verbe ; règle dans `SKILL.md` : protection, accident, crise → renvoi aux humains d'abord (helpline, cellule de crise, coach, RG) avec références, puis l'information. Simulation d'entretien hors pilote. ➡️ ok.
16. **Format d'un référentiel** : frontmatter `slug, titre, signaux, role, verbes, parametres, canevas (id), sources (id#section), inclut` ; corps `## Non-négociables` (N1..Nk, condition en texte, citation), `## Selon la date`, `## Critères de qualité` (Q1..Qn), `## Critères non officiels`, `## Pièges`, `## Trame de conception` ; pas de `type` ni `si:` structuré. ➡️ « Égal, à adapter au mieux selon les besoins. » Format libre, décision déléguée.
17. **`SKILL.md` de `scout`** : nom `scout`, description de la proposition C, corps ≤ 150 lignes (quatre verbes, chargement en quatre pas, catalogue des référentiels, niveaux, citation, hors corpus, situations), squelettes `references/corriger.md`, `concevoir.md`, `chercher.md`. ➡️ ok.
18. **Jeu d'essai** : `pilote/cas/<nn>-<slug>.md`, `pilote/attendus.yaml`, `pilote/rapport.md` ; cas joués en Claude Code par l'agent, cinq cas rejoués par le mainteneur sur claude.ai et Gemini. ➡️ ok. Documents réels : pas de réponse explicite ; cas fabriqués depuis `js-exemple-*` par défaut.
19. **Ordre des travaux** : (1) `check` étendu aux référentiels ; (2) `build claude-code` + `just install` ; (3) zips claude.ai et Gemini ; (4) pilote évalué ; (5) pack aplati `camp` pour GPT et Claude Project. Préalables corpus de Q8 relus par le mainteneur avant ingestion. ➡️ ok. **« Avant d'avancer plus, il faut que je collecte des canevas pour continuer l'analyse. »**

## État du grill et reprise

Acquis : Q2-Q7, Q10, Q11, Q13-Q15, Q17-Q19 ; Q1 et Q5 acquis sous leurs nouveaux noms ; Q16 délégué. En attente : Q9 (rapport de l'agent `cudesch`), Q12 (dépôt des canevas). Décisions consignées dans `DECISIONS.md` (entrée « Organisation des skills »).

**Bloqué sur le mainteneur** (le grill reprend au tour 4 quand ces entrées existent) :
1. Canevas réels dans `documents/` : plusieurs types (UA, activité J+S / bloc, programme de camp, concept de sécurité, programme trimestriel…), vides **et** remplis, nommés avec leur type et leur origine (cofor, MSdS, groupe). Analyse prévue : structure, champs, écarts avec les listes des sources, choix du canevas de référence par référentiel.
2. Fichiers joints des anciens Gems Gemini, s'il y en avait (au-delà des trois prompts).
3. Documents réels pour le jeu d'essai, dans `documents/pilote/` : 5 activités J+S ou blocs, 4 UA, 3 programmes de camp, dont un camp 2026 et un 2027. Sinon cas fabriqués.
4. Relecture de la liste d'ingestion de Q8 (modèle de descriptif J+S jsle.ch/fA22, liste de contrôle de l'autorisation de camp) et de `docs/propositions/cudesch-ecart.md` (lot 2 PDF).
5. Rapport de l'agent `cudesch` (`docs/cudesch-rapport.md` sur la branche `cudesch`) à fusionner, puis réponse à Q9.

**Tour 4 prévu** : analyse des canevas déposés → canevas de référence par référentiel ; sources cudesch retenues pour `activite-js`, `ua`, `programme-camp` ; contenu de `reglages.md` ; puis rédaction de `docs/skills-design.md` et début de l'ordre des travaux (Q19).

## Tour 4 — questions et réponses (2026-10-18)

Périmètre réduit : sources cudesch par référentiel, `reglages.md`, format définitif à partir des brouillons de `referentiels/`. Faits préalables : cartographie cudesch × référentiels par sous-agent (sections pertinentes non citées, comparaison des canevas, modèles de programme) ; `cudesch-modele-bloc-ac` et `autre-canevas-ac-vierge` sont une copie quasi verbatim ; aucun modèle de programme de camp dans le cudesch (les « 3 modèles » du rapport sont `js-modele-prog-general-*`) ; le cudesch n'a rien pour `ua`.

20. **Sections canoniques** : Périmètre, Non-négociables, Selon la date, Critères de qualité, Critères non officiels, Questions à poser avant de juger, Pièges, Trame de conception ; sections libres entre non officiels et questions ; `Retour au rédacteur` retiré (méthode commune) ; annexe de renvois gardée courte. ➡️ ok.
21. **Portée des N** : `Nk. [portée] …`, étiquettes déclarées en tête de section ; tous les N dans Non-négociables ; Selon la date = tableau des différences. ➡️ ok.
22. **Numéros stables** dès `valide` (trous, pas de réemploi). ➡️ ok.
23. **Traçabilité** : (a) marques courtes `(mainteneur)`, `(revue XX-nn)`, `(terrain)` sans date ; (b) étiquette `[non officiel]` en sortie sur la part non sourcée d'un critère officiel. ➡️ **(a) seulement** ; une nuance du mainteneur dans un critère officiel est sa lecture du critère, énoncée avec lui sans étiquette (Q32).
24. **Frontmatter** : `statut: brouillon | relu | valide`, `relu_le`, `parametres` en objets `{nom, obligatoire}`, `sources` = ids cités vérifié par `check`. ➡️ ok.
25. **Canevas = formats reconnus**, trame = structure de sortie de *concevoir*, plus de canevas de référence. ➡️ ok.
26. **`inclut:`** : inclus chargé en entier seulement si la pièce est jointe ou demandée, un niveau. ➡️ ok.
27. **`check`** : citations, N cité, `sources` = cités, `inclut`/`canevas` existants, 4 000 / 6 000 mots, référentiels listés à `--new-version`. ➡️ ok.
28. **`reglages.md`** dans `skills/scout/references/`. ➡️ ok.
29. **Contenu de `reglages.md`** : niveau et longueurs, priorités et dosage, ton, hors corpus, paramètres bloquants, critères globaux `[non officiel]`, étiquettes ; invariants hors fichier. ➡️ ok.
30. **Forme et priorité** : ≤ 60 lignes, une ligne par réglage ; conversation > réglages > `SKILL.md` ; pas de surcharge par référentiel. ➡️ ok.
31. **Grade de preuve du cudesch** : jamais seul sous un N sauf `concept-de-securite` ; ailleurs Q ou seconde citation. ➡️ ok.
32. Lecture de Q23 confirmée : pas de scission des nuances vers « non officiels ». ➡️ ok.
33. **`activite-js`** : cudeschin §3 et securite §10 en secondes citations ; Q `cudesch-programme#09`, appui `cudeschin#01` ; `cudesch-planification-activite` en canevas. ➡️ ok.
34. **`concept-de-securite`** : section « Exemples officiels » (#24-#28, #30) ; sections par type #11-#13, #15 ; Q dangers hors activité #16-#20, #31-#32, cudeschin §8 et §10 ; annexes citées sous N5 ; base juridique en piège ; smt, prévention PSA, constructions écartés. ➡️ ok.
35. **`programme-camp`** : canevas = `js-exemple-programme-camp-ete` + trois `js-modele-prog-general-*` ; cudeschin §3 ; Q `cudesch-programme#04` ; `etre-responsable#25` sur N11 ; renvois camp-* ; section « Selon la branche ». ➡️ ok.
36. **`ua`** : pas de cudesch (AAC écarté). ➡️ ok.
37. **Mise en œuvre** : quatre sous-agents, `statut: relu`, puis `docs/skills-design.md`, `reglages.md`, DECISIONS, ROADMAP ; `check` ensuite selon Q19. ➡️ ok.

## État du grill après le tour 4

Frontière vide : Q1-Q37 acquis (Q1, Q5, Q12 sous leurs formes amendées ; Q9 réglé par le rapport cudesch ; Q16 fixé par Q20-Q27). Spécification : `docs/skills-design.md`. Prochaines étapes hors grill : `check` étendu aux référentiels, `SKILL.md` de `scout`, build et pilote (Q19).

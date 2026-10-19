# Briefing : premiers référentiels (brouillons)

Rédigé le 2026-10-18 pour les sous-agents qui écrivent `referentiels/<slug>.md`. Contexte : DECISIONS « Organisation des skills » (2026-10-17) et « Terrain : réponses du mainteneur » ; METHODE § Skills. Les référentiels sont des **brouillons** tant que le tour 4 du grill et `docs/skills-design.md` ne sont pas faits ; ils seront validés par `check` plus tard.

## Ce qu'est un référentiel

Un fichier par livrable, données de premier rang, lu par le skill `scout` pour corriger ou concevoir ce livrable. Il ne copie jamais une section de source : il la cite. Tout en français, vouvoiement neutre, pas de flatterie.

Format (Q16 du grill, format libre mais on part de là) :

```
---
slug: activite-js
titre: Activité J+S (AC / SC jusqu'en 2026)
signaux: [mots ou rubriques qui trahissent ce livrable dans une demande]
role: [responsable, coach-js, formateur]
verbes: [corriger, concevoir]
parametres: [date du camp (obligatoire), branche, type 2026 (AC/SC) ou activité J+S 2027]
canevas: [ids de sources nature: exemple]
sources: [ids des sources citées]
inclut: []           # autres référentiels composés (ex. concept-de-securite)
statut: brouillon 2026-10-18
---
## Non-négociables
N1. <condition en une phrase> — `id#NN-slug` (ou `id#NN-slug p.N`)
## Selon la date
## Critères de qualité
Q1. …
## Critères non officiels
[non officiel] …  (origine : revue G-xx, terrain)
## Pièges
## Trame de conception
```

Règles :
- **Citation** : `id#NN-slug` où `NN-slug.md` est un fichier de `sources/<id>/` listé dans `sources/<id>/index.md`. Vérifier que le fichier existe. Ne jamais citer `docs/terrain/*` ni `documents/` comme source ; les écrire « (terrain) » ou « (revue AC-03) ».
- **Non-négociable** = exigence officielle dont l'absence rend le livrable non conforme (règlement, directive, check-list d'autorisation, exigences J+S). Toujours cité. En cas de doute : critère de qualité, pas non-négociable.
- **Critère de qualité** (Q) = officiel ou recommandé par une source, cité quand possible.
- **[non officiel]** = critères G de `docs/revue-criteres-cantonaux.md` et pratiques déduites de `docs/terrain/`. Jamais non-négociables. Reprendre les nuances du mainteneur (« conseillé », « souvent pratiqué », « pas obligatoire ») dans la formulation.
- Les critères **R** de la revue n'entrent nulle part ; les **O** entrent en N ou en Q selon leur force, avec la source indiquée dans la colonne « source officielle » (la vérifier dans `sources/<id>/index.md` pour trouver le `NN-slug` exact ; si la colonne dit « aucune trouvée » mais que la décision est O, chercher la source ; introuvable → [non officiel] avec mention « O selon le mainteneur, source à trouver »).
- **Selon la date** : jeu 2027 (`msds-exigences-js-2027-camps`, `js-manuel-sport-de-camp-trekking` 2026 : activité J+S, part sportive par tranches de 15 min, formes caractéristiques, plus d'AC/SC ni de domaines) vs jeu 2026 (`js-sdct-camp` : AC/SC, domaines). Le référentiel choisit selon la date du camp.
- **Vocabulaire** : UA (pas « point de cours »), AS (activité spirituelle), AA = AdA = VC (autre activité, hors J+S), PF = point fixe (séance de maîtrise au camp), responsable de jour (pas « chef »). Huit méthodes scoutes (profil du scoutisme), pas sept. Voir `docs/terrain/lexique-terrain.md`.
- **Canevas** : seuls les modèles vierges ingérés (`autre-canevas-*`, `cudesch-modele-bloc-*`) sont des canevas citables. Les canevas de l'association cantonale décrits dans `docs/terrain/canevas-cantonaux.md` ne sont **pas ingérés** (décision du mainteneur, 2026-10-18) : on en déduit les rubriques et règles, décrites en « Trame de conception » et « Critères non officiels », avec la mention « (trame cantonale, non officielle) ».
- Longueur : viser 120-200 lignes. Pas de tableau de plus de 6 colonnes. Pas d'exemple réel ni de nom.
- Ne pas toucher `sources/`, `docs/terrain/`, `DECISIONS.md`, `ROADMAP.md`. Écrire seulement `referentiels/<slug>.md`.

## Entrées par référentiel

| slug | revue (sections) | terrain | sources à lire en priorité |
|---|---|---|---|
| `activite-js` | 1 AC, 2 SC, 4 TK (randonnée), 9 RL, 5 QC (pour la manière de commenter) | `activites-js.md`, `canevas-cantonaux.md` §2-5, `lexique-terrain.md` | `msds-exigences-js-2027-camps`, `js-manuel-sport-de-camp-trekking`, `js-sdct-camp`, `msds-hering-camps` (D), `msds-autorisation-de-camp`, `cudesch-modele-bloc-ac/sc`, `autre-canevas-ac/sc-vierge`, `js-aide-memoire-3x3-en-route` |
| `concept-de-securite` | 3 CS, 7 RG, 4 TK (partie sécurité) | `securite.md` (§1, §3, §4, §6 réponses), `canevas-cantonaux.md` §2 (CdS) | `cudesch-securite`, `js-manuel-sport-de-camp-trekking` (sécurité, matrice), `msds-reglement-de-camp`, `msds-autorisation-de-camp`, `js-aide-memoire-prevention-accidents-sct`, `js-securite-l-essentiel`, `js-sdct-montagne/eau/hiver` (domaines) |
| `programme-camp` | 6 PC, 8 LV, 10 FO | `camps.md`, `canevas-cantonaux.md` §2 (picasso, programme annuel), `lexique-terrain.md` | `msds-hering-camps`, `js-sdct-camp`, `msds-reglement-de-camp`, `msds-autorisation-de-camp`, `msds-exigences-js-2027-camps`, `js-guide-offres-sct` si présent |
| `ua` | 11 CU, 5 QC | `cours-ua.md`, `lexique-terrain.md` (formation) | `msds-unite-d-apprentissage`, `msds-le-cours`, `msds-retour-qualifier-accompagner`, `msds-modele-de-formation`, `cofor-checklist-cours-base` (§3.5), `autre-canevas-ua-top`, `autre-canevas-point-de-cours-js`, `cofor-pano-retour-qualifier` |

Réponses du mainteneur à intégrer (2026-10-18) :
- Sécurité : la matrice des risques n'est **pas obligatoire** (outil, surtout pour les activités à risque) ; un CdS global sans matrice mais avec risques concrets et mesures est conforme ; randonnée → CdS avec 3x3, tyrolienne ou eau → CdS avec matrice (pratique recommandée) ; règle « risque récurrent → CdS global, spécifique → CdS d'activité » = approche générale ; réaction d'urgence sans noms (applicable par tout responsable), le reste du CdS avec responsables nommés ; CdS d'activité pas toujours besoin d'une procédure d'urgence si le global suffit ; corde : personne expérimentée, pas d'expert J+S ; annexes typiques (ORA, crise, pharmacie, Helpline) : concepts à couvrir, pas documents à exiger ; le 3x3 identifie, le CdS répond ; ne pas lister l'inapplicable.
- Activités : remplacement = autre activité de même type, temps de sport équivalent ; variante = même activité adaptée ; courbe d'intensité (généralisation des trois parties) ; objectifs atteignables, taxonomie MSdS ; mini-analyse de risques dans la fiche, CdS joint si nécessaire, sans redire le CdS global ; commentaires : dosage, 2-3 points importants plutôt que 30.
- Programme : plusieurs branches ou programmes doivent être lisibles ; identifiant unique par activité ; couleurs conseillées ; quota responsables/participants J+S à retrouver dans les sources (faible, on recommande plus) ; PF = séance de maîtrise.
- UA : terme « UA » ; se baser sur les brochures MSdS ; PATExE courant, IFV et GAG = structures alternatives admises ; 80 % de présence (exigence J+S à sourcer) ; critères éliminatoires avec avertissement = pratique courante.

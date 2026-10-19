# Taxonomie

Vocabulaire contrôlé des champs `audience` et `themes` de `source.yaml`. Ajouter un terme ici avant de l'utiliser dans un yaml. `scripts/inventory` refuse un terme absent.

## audience

| valeur | qui |
|---|---|
| `responsable` | responsable d'unité ou de groupe, planifie et mène des activités |
| `formateur` | membre d'une équipe de cours MSdS (base, RU, pano, module) |
| `expert-js` | expert J+S, qualifie et accompagne en cours |
| `coach-js` | coach J+S d'un groupe, valide les camps et activités |
| `cadre-cantonal` | responsable cantonal de formation ou de programme |

## themes

| valeur | couvre |
|---|---|
| `formation` | conception et conduite des cours, UA, qualification, retour |
| `programme` | profil du scoutisme, méthodes, branches, progression |
| `camp` | sport de camp/trekking, préparation, vie de camp |
| `securite` | sécurité, activités à risque, eau, neige, montagne |
| `prevention` | prévention des abus, PSA, règles de comportement |
| `inclusion` | diversité, inclusion, handicap |
| `sport` | bases de la technique sportive, Physis, Psyché, apprentissage dans le sport |
| `administration` | autorisation, financement, administration de cours, budgets |
| `organisation` | structure MSdS, organigramme, rôles |

Règle : au plus trois thèmes par source. Si un document en couvre plus, c'est un manuel ; les thèmes fins se portent dans `concepts`.

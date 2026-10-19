# Liens à ingérer

Pages web repérées, classées le 2026-10-17 (statut HTTP, rendu, sous-pages, documents). Chaque ligne « à parcourir » passe par `discover` puis triage humain (voir `METHODE.md`, Sources web).

## Traité le 2026-10-17

| url | résultat |
|---|---|
| https://pfadi.swiss/fr/formation-encadrement/cudesch/ | `discover --depth 2` → `build/pfadi.yaml` (377 pages, 481 fichiers, tout le site fr/de/it). Pages non ingérées (présentation) ; fichiers servis par `ingest --match` |
| https://hering.scout.ch/fr | `msds-hering-camps`, 9 pages (SPA, `convert --render`) |
| https://cudeschin.pbs.ch/ | `cudesch-cudeschin`, 18 articles en français via locale `fr-CH` ; routes `#!/article/NN` non crawlables, manifeste écrit à la main |
| mobilesport, article éthique | `js-ethique-proximite-soutien` |

## À parcourir (Phase 2)

| url | nature | plan |
|---|---|---|
| https://pfadi.swiss/fr/publications-telechargements/downloads/ | catalogue chargé en JS | `discover --depth 1 --render` → `build/pfadi-downloads.yaml`, puis `ingest --match` (en cours en fin de session du 2026-10-17) |

## Catalogue seulement (`extraction: catalogue`)

| url | nature | plan |
|---|---|---|
| https://communagir.org/outils-animation/ | WordPress, sitemap, 78 fiches d'outils d'animation, Québec, fr | catalogue depuis le sitemap et les pages (robots autorise les bots IA) |
| https://www.liberatingstructures.com/ | Squarespace, 33 structures, anglais, robots.txt bloque les bots IA | catalogue depuis les titres du sitemap et la mémoire de l'agent, sans téléchargement des pages |

## Reporté

| url | nature | raison |
|---|---|---|
| https://tool.jeunesseetsport.ch/?lang=fr&org=jugendundsport | SPA, ~250 séquences d'apprentissage, toutes fédérations | tri par pertinence scoute trop lourd pour la Phase 2 ; revoir quand les skills J+S existent |

## Écarté

| url | raison |
|---|---|
| https://www.apps.baspo.admin.ch/ndbjs/orgcheck/fragebogen/default.asp?spr=f&check=&grp=&org=leiter | questionnaire interactif, pas scrappable ; seul le texte d'intro est capturable |

# Skills scoutisme suisse

Fabrique de skills pour responsables, formateurs et experts J+S du scoutisme suisse, à partir des ressources officielles (MSdS, cofor, J+S, cudesch). Tout en français.

Lire `METHODE.md` avant de toucher `sources/`, `skills-src/`, `skills/` ou `scripts/` : pipeline, statuts, identifiants, arborescence.

- `ROADMAP.md` : état du projet et prochaine action. Mettre à jour en fin de session.
- `DECISIONS.md` : ajouter une entrée pour toute décision structurante.
- `sources/_template.yaml` : schéma du registre ; `docs/taxonomie.md` : valeurs autorisées pour `audience` et `themes`.
- `INVENTORY.md` et `skills/` sont générés, ne pas les éditer : écrire dans `skills-src/`, `referentiels/` ou les sources, puis `just skills` et commiter `skills/` avec le changement.
- Locaux, jamais versionnés : `sources/*/original/`, `pilote/cas/`, `documents/`. Rien de nominatif (groupe, lieu, année d'un camp réel, personne) dans un fichier versionné.
- Commits en conventional commits (`feat(skills):`, `fix(contenu):`, `docs:`…) : release-please en tire versions et CHANGELOG.
- `documents/` est une boîte d'entrée locale : ingérer puis vider, ne jamais y travailler.
- Un skill ne copie jamais une section de source ; il la référence par `id`.

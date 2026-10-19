# Contribuer

Merci de votre intérêt. Pour signaler une erreur ou proposer une idée sans toucher au code, ouvrez une [issue](https://github.com/fuzoh/scouts-skills/issues/new/choose) : c'est la voie la plus simple. Ce qui suit concerne les modifications du dépôt.

## Avant de commencer

- Lire [`METHODE.md`](METHODE.md) : pipeline des sources, statuts, identifiants, arborescence, commandes.
- Outils : [uv](https://docs.astral.sh/uv/) (Python 3.14) et [just](https://just.systems/). `uv sync` installe tout ; `just` liste les recettes.
- Aucune donnée personnelle dans un fichier versionné : pas de nom de personne, de groupe, de lieu ou d'année qui identifie un camp ou un cours réel, pas d'identifiant ni de mot de passe. Les exemples sont fictifs.

## Structure

| dossier | rôle | édité à la main |
|---|---|---|
| `skills-src/<skill>/` | sources d'écriture des skills (`SKILL.md`, `references/`, savoirs, référentiels dérivés de `scouts`) | oui |
| `skills/<skill>/` | packs générés par `just skills`, installés par `npx skills add` | **non** |
| `referentiels/` | un référentiel par livrable, citations `id#NN-slug` vérifiées | oui |
| `sources/<id>/` | registre (`source.yaml`), texte converti, index, sections | registre et index oui, texte converti non |
| `scripts/`, `tests/` | outillage (CLI typer) et tests | oui |
| `site/` | pages du site GitHub Pages | oui |

Les originaux des sources (`sources/*/original/`) ne sont pas versionnés : `url`, `file_url` et `sha256` du registre permettent de les retrouver. Ajouter ou mettre à jour une source se fait en local avec l'original (`just ingest`, voir METHODE), puis on commite le registre et le texte converti.

## Modifier un skill, un savoir ou un référentiel

1. Modifier `skills-src/`, `referentiels/` ou `GLOSSARY.md`. Un référentiel de `referentiels/` modifié doit être reporté dans son dossier dérivé de `skills-src/scouts/referentiels/`.
2. `just check` (registre, référentiels, limites de `scouts`) et `just test`.
3. `just skills` : régénère `skills/` et les zips de `dist/`.
4. Commiter le changement **et** `skills/` dans le même commit. La CI refuse un `skills/` qui ne correspond pas au build.

## Commits

[Conventional commits](https://www.conventionalcommits.org/fr/) en français. [release-please](https://github.com/googleapis/release-please) en tire les versions et le `CHANGELOG.md` :

| type | effet | exemple |
|---|---|---|
| `feat` | version mineure (0.x.0) | `feat(contenu): savoir sur les camps à l'étranger` |
| `fix` | version corrective (0.0.x) | `fix(contenu): délai d'annonce du camp à 6 semaines` |
| `docs`, `refactor`, `perf` | listés dans le changelog, pas de version seuls | `docs: méthode de veille` |
| `test`, `build`, `ci`, `chore`, `style` | cachés | `ci: cache uv` |

Tout changement qui modifie ce que le skill répond (savoir, référentiel, réglage, section de source, glossaire) est un `feat` ou un `fix`, jamais un `docs` : sinon aucune version n'est publiée. Portées courantes : `contenu`, `skills`, `referentiels`, `sources`, `scripts`, `build`, `site`, `veille`.

## Pull requests

- Une PR par sujet, titre au format conventional commit.
- Dire ce qui change pour l'utilisateur du skill et, pour une règle, la source officielle (`id#NN-slug` ou lien).
- `just check`, `just test` et `just skills` passés.

## Publication

À chaque push sur `main`, release-please tient à jour une PR de release (version, `CHANGELOG.md`, lignes de version des packs). La fusionner crée le tag et la release GitHub ; la CI y joint `scouts.zip` et `scouts-ressources.zip`.

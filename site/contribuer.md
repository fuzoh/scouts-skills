---
title: Contribuer
order: 8
description: "Structure du dépôt scouts-skills, méthode de travail, commandes et règles pour proposer une modification."
---

Cette page s'adresse aux personnes qui veulent modifier le contenu ou le code. Pour un simple retour, [une issue suffit](signaler.md).

Les règles complètes sont dans [METHODE.md](https://github.com/fuzoh/scouts-skills/blob/main/METHODE.md) (pipeline, statuts, identifiants) et [CONTRIBUTING.md](https://github.com/fuzoh/scouts-skills/blob/main/CONTRIBUTING.md). Lisez-les avant une première modification.

## Structure du dépôt

| Dossier | Contenu |
|---|---|
| `skills-src/` | Sources d'écriture des deux skills : `SKILL.md`, méthodes, réglages, savoirs. C'est ici qu'on modifie un skill. |
| `skills/` | Packs générés par `just skills` et commités, installés par `npx skills add`. Jamais édités à la main. |
| `referentiels/` | Un référentiel par type de document (activité J+S, UA, programme de camp, concept de sécurité) : exigences officielles citées, critères de qualité, pièges, trame. |
| `sources/<id>/` | Registre (`source.yaml`), texte converti et sections de chaque document officiel. |
| `scripts/` | Outils en Python (CLI `typer`, lancés par `uv`) : ingestion, conversion, découpage, contrôles, build, site. |
| `site/` | Pages de ce site, en markdown. |
| `docs/` | Documentation de conception. |

Les originaux (PDF, Word…) ne sont pas dans le dépôt : `sources/*/original/` est ignoré par git. Le registre garde l'adresse (`url`, `file_url`) et l'empreinte (`sha256`) de chaque original.

## Principes

- Un skill ne copie jamais une section de source : il la cite par son identifiant.
- Le registre est la vérité : tout ce qui en dérive est régénéré, jamais édité à la main.
- Rien de nominatif dans un fichier versionné : ni groupe, ni lieu, ni année d'un camp réel, ni personne.
- Tout est en français.

## Commandes

Prérequis : [uv](https://docs.astral.sh/uv/) et [just](https://just.systems/).

```sh
uv sync             # installer les dépendances
just check          # valider le registre, les référentiels et les limites de scouts
just test           # lancer les tests
just skills         # reconstruire skills/ et les zips dans dist/
uv run site --out build/site   # générer ce site en local
```

Après une modification de `skills-src/`, de `referentiels/` ou des sources, lancez `just skills` et commitez `skills/` avec le changement. La CI échoue si `skills/` n'est pas à jour.

## Ajouter une source

Suivez le pipeline de METHODE.md : `ingest`, triage, `convert`, `index`, `split`, puis `just check`. L'original reste sur votre machine. Vérifiez les droits de diffusion avant d'ajouter un document. Retirez tout identifiant d'accès par le champ `redactions` du registre, jamais à la main.

## Commits et pull requests

- Messages en [conventional commits](https://www.conventionalcommits.org/fr/v1.0.0/), en français : `feat(skills): …`, `fix(contenu): …`, `docs: …`. Les versions et le journal des modifications en sont tirés automatiquement.
- Une pull request par sujet, avec `just check` et `just test` verts.
- Décrivez ce qui change pour les utilisateur·ices du skill.

## Licences

Code sous licence MIT. Contenu propre (skills, référentiels, savoirs, site, documentation) sous licence CC BY-SA 4.0. Textes officiels : droits à leurs auteurs, voir [Sources et auteurs](sources.md). En contribuant, vous acceptez de publier votre contribution sous ces licences.

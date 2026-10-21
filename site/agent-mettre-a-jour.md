---
title: Mettre à jour les skills
order: 29
menu: Mettre à jour
parcours: agent
description: "Savoir quand une nouvelle version des skills scouts sort, connaître sa version installée et la mettre à jour dans un agent."
---

Les skills évoluent : corrections de contenu, nouvelles sources, règles qui changent (par exemple au 01.01.2027). Une version installée ne se met pas à jour toute seule : lancez la commande qui correspond à votre mode d'installation. Les commandes ne sont testées que sous Linux ; sous Mac et Windows, elles n'ont pas été essayées.

## Savoir quand une version sort

- La page [Nouveautés](nouveautes.md) liste chaque version et ce qu'elle change.
- Les versions sont aussi publiées sur la page [Releases](https://github.com/fuzoh/scouts-skills/releases) du dépôt. Avec un compte GitHub : **Watch > Custom > Releases** pour recevoir un e-mail à chaque version. Sans compte : le flux [releases.atom](https://github.com/fuzoh/scouts-skills/releases.atom) dans un lecteur de flux RSS.

## Connaître sa version

Demandez à l'agent : « Quelle est la version du skill scouts ? ». Ou lisez la ligne `version` dans `SKILL.md` (bloc `metadata` en tête du fichier) ou dans `MANIFEST.md`. Comparez-la à la dernière version de la page [Nouveautés](nouveautes.md).

## Mettre à jour

Installés avec `npx skills add fuzoh/scouts-skills` :

```sh
npx skills update          # tous les skills installés (l'outil demande la portée)
npx skills update scouts   # un seul skill (ou scouts-ressources)
npx skills update -g       # seulement les skills installés pour votre compte
```

Installés depuis un zip de release : relancez la même commande `npx skills add <adresse du zip>` (voir [Installer avec un agent](agent-installer.md#depuis-un-zip-de-release)).

Installés avec Pi comme paquet :

```sh
pi update git:github.com/fuzoh/scouts-skills
```

Copiés à la main depuis un clone du dépôt :

```sh
cd scouts-skills
git pull
cp -R skills/scouts skills/scouts-ressources ~/.claude/skills/   # même dossier qu'à l'installation
```

Selon l'agent, ouvrez une nouvelle session pour que la nouvelle version soit prise en compte.

## Après la mise à jour

Une réponse vous paraît fausse ou a changé à tort ? [Signalez-la](signaler.md) en indiquant la version.

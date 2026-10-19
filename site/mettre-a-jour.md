---
title: Mettre à jour les skills
order: 4
menu: Mettre à jour
description: "Savoir quand une nouvelle version des skills scouts sort, connaître sa version installée et la mettre à jour, sur le web ou dans un agent."
---

Les skills évoluent : corrections de contenu, nouvelles sources, règles qui changent (par exemple au 01.01.2027). Une version installée ne se met pas à jour toute seule, sauf indication contraire ci-dessous.

## Savoir quand une version sort

- La page [Nouveautés](nouveautes.md) liste chaque version et ce qu'elle change.
- Les versions sont aussi publiées sur la page [Releases](https://github.com/fuzoh/scouts-skills/releases) du dépôt. Avec un compte GitHub : **Watch > Custom > Releases** pour recevoir un e-mail à chaque version. Sans compte : le flux [releases.atom](https://github.com/fuzoh/scouts-skills/releases.atom) dans un lecteur de flux RSS.

## Connaître sa version

Demandez à l'assistant : « Quelle est la version du skill scouts ? ». Ou lisez la ligne `version` dans `SKILL.md` (bloc `metadata` en tête du fichier) ou dans `MANIFEST.md`. Comparez-la à la dernière version de la page [Nouveautés](nouveautes.md).

## Sur une plateforme web (claude.ai, ChatGPT, Gemini)

Le skill importé est une copie figée du zip.

1. Téléchargez le nouveau zip : [scouts.zip](https://github.com/fuzoh/scouts-skills/releases/latest/download/scouts.zip) ou [scouts-ressources.zip](https://github.com/fuzoh/scouts-skills/releases/latest/download/scouts-ressources.zip). Ces liens donnent toujours la dernière version.
2. Supprimez l'ancien skill dans les réglages de la plateforme, à l'endroit où vous l'aviez ajouté (voir [Installer sur une plateforme web](installer-web.md)).
3. Importez le nouveau zip de la même manière que la première fois.
4. Vérifiez la version en la demandant à l'assistant.

Supprimer d'abord l'ancien skill évite d'avoir deux versions actives en même temps.

## Dans un agent (Claude Code, Codex, Pi…)

Installé avec `npx skills add fuzoh/scouts-skills` :

```sh
npx skills update          # tous les skills installés (l'outil demande la portée)
npx skills update scouts   # un seul skill
npx skills update -g       # seulement les skills installés pour votre compte
```

Installé depuis un zip de release : relancez la même commande `npx skills add <adresse du zip>` (voir [Installer avec un agent](installer-agent.md#depuis-un-zip-de-release)).

Installé avec Pi comme paquet :

```sh
pi update git:github.com/fuzoh/scouts-skills
```

Copié à la main depuis un clone du dépôt :

```sh
cd scouts-skills
git pull
cp -R skills/scouts ~/.claude/skills/   # même dossier qu'à l'installation
```

Selon l'agent, ouvrez une nouvelle session pour que la nouvelle version soit prise en compte.

## Après la mise à jour

Une réponse vous paraît fausse ou a changé à tort ? [Signalez-la](signaler.md) en indiquant la version.

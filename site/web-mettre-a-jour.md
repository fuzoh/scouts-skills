---
title: Mettre à jour le skill
order: 16
menu: Mettre à jour
parcours: web
description: "Savoir quand une nouvelle version du skill scouts sort, connaître sa version installée et la mettre à jour sur claude.ai, ChatGPT ou Gemini."
---

Le skill évolue : corrections de contenu, nouvelles sources, règles qui changent (par exemple au 01.01.2027). Le skill importé est une copie figée du zip : il ne se met pas à jour tout seul.

## Savoir quand une version sort

- La page [Nouveautés](nouveautes.md) liste chaque version et ce qu'elle change.
- Les versions sont aussi publiées sur la page [Releases](https://github.com/fuzoh/scouts-skills/releases) du dépôt. Avec un compte GitHub : **Watch > Custom > Releases** pour recevoir un e-mail à chaque version. Sans compte : le flux [releases.atom](https://github.com/fuzoh/scouts-skills/releases.atom) dans un lecteur de flux RSS.

## Connaître sa version

Demandez à l'assistant : « Quelle est la version du skill scouts ? ». Comparez-la à la dernière version de la page [Nouveautés](nouveautes.md).

## Mettre à jour

1. Téléchargez le nouveau zip : [scouts.zip](https://github.com/fuzoh/scouts-skills/releases/latest/download/scouts.zip). Ce lien donne toujours la dernière version.
2. Supprimez l'ancien skill dans les réglages de la plateforme, à l'endroit où vous l'aviez ajouté (voir [Installer sur une IA web](web-installer.md)).
3. Importez le nouveau zip de la même manière que la première fois.
4. Vérifiez la version en la demandant à l'assistant.

Supprimer d'abord l'ancien skill évite d'avoir deux versions actives en même temps.

## Après la mise à jour

Une réponse vous paraît fausse ou a changé à tort ? [Signalez-la](signaler.md) en indiquant la version.

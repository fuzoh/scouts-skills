---
title: Citer les sources
order: 22
menu: Citer les sources
parcours: agent
description: "Obtenir le texte officiel exact et sa référence avec le skill scouts-ressources."
---

[Utiliser les skills](agent-utiliser.md) > Citer les sources

Le skill `scouts` donne des réponses courtes, sans références précises. Il termine par les titres des documents à lire. Quand il vous faut la règle exacte et l'endroit où elle est écrite, prenez `scouts-ressources`.

## Quand prendre `scouts-ressources`

- Préparer une UA ou un cours, avec le texte officiel sous les yeux.
- Trancher un désaccord : « où est-ce écrit ? »
- Citer une règle dans un dossier, un retour de qualification ou un courriel.
- Vérifier une réponse de `scouts` qui vous surprend.

`scouts-ressources` embarque le corpus officiel, section par section : manuels, règlements, check-lists et brochures du MSdS, de la cofor, de J+S et du cudesch. La liste complète figure dans [Sources et auteurs](sources.md).

## Exemples de demandes

- « Cite-moi la règle exacte sur les cartes à renvoyer après le camp. »
- « Quel est le nombre minimum de participants pour un camp J+S ? Donne la source. »
- « Que dit le texte officiel sur le rôle du coach dans l'autorisation de camp ? »
- « Relis cette UA et cite la règle pour chaque correction. »

## Lire une citation

Chaque règle porte une référence de la forme `identifiant#section`, par exemple `msds-hering-camps#08-g-cloture-du-camp`. La première fois, le titre du document est aussi donné en clair.

- L'identifiant (avant `#`) désigne un document. Retrouvez-le, avec son titre, sa version et un lien vers l'original, dans [Sources et auteurs](sources.md).
- La partie après `#` désigne la section du document.
- `p.N` indique la page, quand elle est connue.

Une règle sans citation n'est pas une règle : si vous en voyez une, [signalez-la](signaler.md).

## Limites

- `scouts-ressources` est gros (environ 2 000 fichiers). Il fonctionne avec les agents en ligne de commande. Sur les plateformes web, seul ChatGPT l'accepte ; il est trop lourd pour claude.ai et Gemini.
- Certaines sections ont perdu des cases ou des schémas à la conversion. Le skill les marque `[fidélité partielle]` et n'en tire pas de conclusion.
- La citation ne remplace pas la lecture du document officiel, surtout s'il a changé depuis la dernière version du skill.

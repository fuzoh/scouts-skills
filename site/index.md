---
title: Assistants du scoutisme suisse
order: 1
menu: Accueil
description: "Deux skills pour assistants IA, fondés sur les ressources officielles du scoutisme suisse (MSdS, cofor, J+S, cudesch)."
---

Ce site présente deux *skills*. Un skill est un petit dossier d'instructions et de fichiers que vous ajoutez à un assistant IA (Claude, Codex, Pi, Gemini…). L'assistant le consulte quand votre question parle de scoutisme.

Ces skills s'appuient sur les ressources officielles du scoutisme suisse : Mouvement Scout de Suisse (MSdS), commission formation (cofor), Jeunesse+Sport (J+S) et cudesch.

## Pour qui

- Les responsables d'unité, de camp et de groupe.
- Les formateur·ices et les directions de cours.
- Les coachs J+S, les expert·es J+S et les CàF.

## Ce qu'ils font

- Répondre à une question de règle, de délai ou de chiffre.
- Expliquer une notion : PATExE, 3x3, formes caractéristiques, activité J+S 2027, qualification…
- Relire et corriger un document : activité J+S, unité d'apprentissage (UA), programme de camp ou picasso, concept de sécurité.
- Aider à concevoir un de ces documents.
- Guider une personne qui débute : thèmes, lectures, exemples de demandes.

Des exemples concrets se trouvent dans [Utiliser les skills](utiliser.md).

## Deux skills : lequel choisir

| | `scouts` | `scouts-ressources` |
|---|---|---|
| Pour qui | Tout le monde, usage courant | Formateur·ices, approfondissement |
| Contenu | Savoirs résumés, critères de relecture, guide | Les mêmes critères et tout le corpus officiel, section par section |
| Réponses | Courtes, sans références de page | Chaque règle citée avec sa source exacte |
| Taille | Environ 40 fichiers, 0,2 Mo | Environ 2 000 fichiers, 8,7 Mo |
| Agents en ligne de commande | Tous ceux qui prennent en charge les skills (Claude Code, Codex, Pi…) | Tous ceux qui prennent en charge les skills (Claude Code, Codex, Pi…) |
| Plateformes web | claude.ai, Gemini (testés) | ChatGPT seulement (testé) ; trop lourd pour claude.ai et Gemini |

Prenez `scouts` par défaut. Prenez `scouts-ressources` quand vous avez besoin du texte officiel exact : préparer un cours, trancher un désaccord, citer une règle dans un document. Voir [Citer les sources](citer-les-sources.md).

## Limites

- **Ce n'est pas un document officiel.** Ni le MSdS ni J+S ne publient ces skills. En cas de doute, le texte officiel et les personnes responsables (coach J+S, CàF, association cantonale) font foi.
- **Vérifiez toujours.** Un assistant IA peut se tromper, même avec de bonnes sources. Relisez chaque règle importante dans le document officiel avant de vous y fier.
- **Règles 2027 par défaut.** Les skills appliquent les règles J+S en vigueur dès le 01.01.2027 (activité J+S ; les AC et SC n'existent plus). Pour un camp ou un cours de 2026, précisez la date dans votre demande.
- **Pas de données personnelles.** Retirez les noms, adresses et numéros des documents que vous faites relire.

## Commencer

1. Installez un skill : [sur une plateforme web](installer-web.md) (claude.ai, ChatGPT, Gemini) ou [avec un agent](installer-agent.md) (Claude Code, Codex, Pi…).
2. Lisez [Utiliser les skills](utiliser.md) pour des exemples de demandes.
3. Une réponse fausse ? [Signalez-la](signaler.md).
4. Les documents utilisés et leurs auteurs : [Sources et auteurs](sources.md).
5. Pour aller plus loin : [Contribuer](contribuer.md).

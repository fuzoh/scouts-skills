---
title: Personnaliser les skills
order: 24
menu: Personnaliser
parcours: agent
description: "Faire tenir compte aux skills scouts de votre groupe, de votre association cantonale ou de votre cours : réglages, règles locales, contacts et documents propres, dans un dossier scouts-perso."
---

Les skills connaissent les documents officiels du MSdS, de J+S et du cudesch. Ils ne connaissent ni les directives de votre association cantonale, ni les habitudes de votre groupe, ni le dossier de votre cours. La personnalisation les leur apprend : vous parlez à l'agent, il range ce que vous lui dites dans un dossier `scouts-perso/` et le relit à chaque question.

Elle marche avec `scouts` comme avec `scouts-ressources`, **dans un agent seulement** (Claude Code, Codex, Antigravity…), parce qu'il faut un dossier qui reste d'une conversation à l'autre. Dans le navigateur (claude.ai, ChatGPT, Gemini), l'assistant vous renvoie à cette page. Essayé sous Linux seulement : Mac et Windows ne sont pas testés.

## Commencer

Ouvrez votre agent dans le dossier de travail habituel (votre projet de camp, de cours…) et demandez :

> Personnalise le skill scouts pour mon groupe.

L'agent crée `scouts-perso/` à la racine du dossier, puis vous pose quelques questions, trois au plus à la fois :

1. votre rôle et la branche ;
2. vos réglages : tutoiement, niveau de retour par défaut, longueur ;
3. les règles propres à votre groupe, à votre association cantonale ou à votre cours ;
4. les contacts utiles : coach J+S, CàF, Helpline ou cellule de crise cantonale, responsable de groupe.

Vous pouvez répondre à certaines questions seulement, et compléter plus tard (« Retiens que notre maîtrise veut le programme 6 semaines avant le camp. »).

Pour les mêmes réglages dans tous vos projets, demandez un dossier global : l'agent le crée dans votre dossier personnel (`~/scouts-perso/`). Un dossier de projet remplace alors entièrement le dossier global, sans mélange.

## Ajouter un document

> Ajoute ce document à mes documents scouts : directives-camps.pdf

Formats acceptés : PDF, Word (docx), PowerPoint (pptx), Excel (xlsx), texte et markdown. L'agent range le document dans `ac/` (association cantonale), `groupe/` ou `cours/`, le découpe en fiches courtes par titre, garde une copie de l'original et ajoute une ligne à l'index. Il ne l'ajoute pas deux fois.

- Avec `scouts-ressources` et [`uv`](https://docs.astral.sh/uv/) installé, l'agent lance un petit script de conversion fourni avec le skill : c'est plus rapide et plus fidèle pour un gros PDF.
- Sans `uv`, ou avec `scouts`, l'agent lit le document lui-même et écrit les fiches. Le résultat est le même, en plus lent.

N'y mettez jamais de liste de participant·es, de fiche médicale ni de document sur des personnes : l'agent refuse.

## Ce que l'assistant en fait

- Vos **réglages** remplacent ceux du skill. Une consigne donnée dans la conversation reste prioritaire.
- Vos **règles locales** s'ajoutent aux règles officielles ou les durcissent (un délai plus long, une exigence de plus). Elles n'assouplissent jamais une règle officielle, de sécurité ou d'urgence : en cas de conflit, l'assistant donne les deux et suit la plus prudente.
- Ce qui vient de votre dossier est étiqueté `[perso]` dans les réponses.
- Vos **contacts** servent à vous orienter (urgence, « à qui demander »), toujours après les numéros officiels. Ce sont les seuls noms réels que l'assistant écrit ; il n'en met jamais dans une correction ni dans un brouillon.

## Le dossier `scouts-perso/`

```text
scouts-perso/
  README.md     profil, réglages, règles locales, contacts, index des fiches
  ac/           documents de l'association cantonale, en fiches
  groupe/       documents du groupe
  cours/        documents d'un cours
  originaux/    copies des fichiers ajoutés
```

`README.md` est lu à chaque question : l'agent le garde court (2 000 tokens environ). Vous pouvez l'ouvrir et le modifier vous-même ; c'est un simple fichier texte.

Le dossier vit **à côté** du skill, jamais dedans : une mise à jour du skill ([Mettre à jour](agent-mettre-a-jour.md)) ne le touche pas.

## Confidentialité

Le dossier contient des noms et des numéros de téléphone. Si votre projet est un dépôt git, l'agent propose d'ajouter `scouts-perso/` au fichier `.gitignore` pour qu'il ne soit jamais publié. Acceptez, surtout si le dépôt est public.

Le contenu de votre dossier est envoyé à l'assistant IA avec vos questions, comme un document joint : ne mettez rien que vous ne joindriez pas à une conversation.

## Partager avec une équipe

Le dossier perso ne sert qu'à vous, dans votre agent. Pour donner les mêmes règles et documents à toute une équipe, ou les utiliser dans le navigateur, [construisez votre version](agent-construire.md) : un skill sous votre nom, en zip ou pour un agent.

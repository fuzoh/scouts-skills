---
title: Signaler une erreur, suggérer, commenter
order: 7
menu: Signaler une erreur
description: "Signaler une réponse fausse, proposer une amélioration ou décrire un problème d'installation, sans connaissances techniques."
---

Vos retours améliorent les skills. Ils passent par des *issues* GitHub : de courts formulaires en ligne, publics, que le mainteneur reçoit et suit. Pas besoin d'être développeur·euse.

**Ne collez jamais de données personnelles** : pas de noms, d'adresses, de numéros de téléphone, de dates de naissance ni d'informations médicales. Les issues sont publiques et visibles par tout le monde.

## 1. Créer un compte GitHub (une seule fois)

1. Allez sur [github.com/signup](https://github.com/signup).
2. Saisissez une adresse e-mail, un mot de passe et un nom d'utilisateur. Le nom d'utilisateur sera visible publiquement : un pseudonyme convient.
3. Confirmez avec le code reçu par e-mail.
4. Si GitHub vous propose un abonnement, choisissez l'offre gratuite (*Free*).

## 2. Choisir le bon formulaire

| Vous voulez… | Formulaire |
|---|---|
| Signaler une réponse fausse : règle, chiffre, délai, source mal citée | [Erreur de contenu](https://github.com/fuzoh/scouts-skills/issues/new?template=erreur-contenu.yml) |
| Proposer une amélioration, un document à ajouter, une question mal traitée | [Suggestion](https://github.com/fuzoh/scouts-skills/issues/new?template=suggestion.yml) |
| Décrire un problème pour installer ou déclencher un skill | [Problème d'installation](https://github.com/fuzoh/scouts-skills/issues/new?template=installation.yml) |

Remplissez les champs, puis cliquez sur **Create** (ou **Submit new issue**).

## 3. Quoi joindre

- **Votre demande** (le prompt), copiée telle quelle, données personnelles retirées.
- **La réponse** du skill, ou le passage en cause.
- **La version du skill** : demandez « Quelle est la version du skill scouts ? », ou lisez la ligne `version` du fichier `SKILL.md`.
- **La plateforme** : claude.ai, ChatGPT, Gemini, Claude Code, Codex, Pi…
- **Le skill** utilisé : `scouts` ou `scouts-ressources`.
- Pour une erreur de contenu : ce qui serait juste et, si possible, le document officiel qui le dit (titre, page).

Un document que vous faisiez relire ne doit pas être joint s'il contient des données réelles. Décrivez plutôt le passage en cause.

## 4. Commenter une issue existante

Votre problème est peut-être déjà signalé.

1. Ouvrez la [liste des issues](https://github.com/fuzoh/scouts-skills/issues).
2. Cherchez avec quelques mots-clés dans la barre de recherche.
3. Ouvrez l'issue, écrivez votre commentaire en bas de la page, puis cliquez sur **Comment**.

Pour simplement dire « moi aussi », ajoutez une réaction « pouce levé » sur le premier message plutôt qu'un commentaire.

## Et ensuite

Le mainteneur répond dans l'issue. Vous recevez un e-mail à chaque réponse. Une correction est publiée dans une nouvelle version du skill : [mettez à jour](installer-agent.md#methode-universelle-npx-skills) ou téléchargez le nouveau zip.

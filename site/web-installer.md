---
title: Installer sur une IA web
order: 10
menu: Installer
parcours: web
description: "Ajouter le skill scouts à claude.ai, ChatGPT ou Gemini, à partir d'un fichier zip."
---

Sur une plateforme web (App Gemini, Claude.ai, ChatGPT), vous ajoutez un skill en téléversant un fichier zip. Aucune installation sur votre ordinateur n'est nécessaire.

## Télécharger le zip

[scouts.zip](https://github.com/fuzoh/scouts-skills/releases/latest/download/scouts.zip) : le skill `scouts` (environ 100 Ko). Ne le décompressez pas : la plateforme attend le fichier tel quel. Ce lien donne toujours la dernière version.

## claude.ai

Disponible sur les plans Free, Pro, Max, Team et Enterprise.

1. Activez l'exécution de code. Plans Free, Pro et Max : **Settings > Capabilities**, option **Code execution and file creation**. Plans Team et Enterprise : voir plus bas.
2. Ouvrez **Customize > Skills**.
3. Cliquez sur **+**, puis **Create skill**, puis **Upload a skill**.
4. Choisissez `scouts.zip`.
5. Le skill apparaît dans votre liste. Vérifiez qu'il est activé.

Les libellés sont ceux de l'interface en anglais ; ils peuvent différer si votre interface est traduite.

Plans Team et Enterprise : les skills sont activés par défaut sur Team. Sur Enterprise, un·e *owner* de l'organisation doit activer **Code execution and file creation** et **Skills** dans les réglages de l'organisation. Si le bouton d'ajout n'apparaît pas, contactez l'owner de votre organisation.

Ensuite, posez simplement votre question : le skill se déclenche seul quand elle parle de scoutisme.

État des essais : testé et fonctionnel.

Source : [aide de Claude, « Use skills in Claude »](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## ChatGPT

ChatGPT propose des skills sur certains plans d'organisation (Business, Enterprise, Education).

Le skill `scouts` fonctionne. Utilisez le menu « Plugins », puis « Skills », puis « Add » pour importer `scouts.zip`.

Source : [aide d'OpenAI, « Skills in ChatGPT »](https://help.openai.com/en/articles/20001066-skills-in-chatgpt).

## Gemini

L'application Gemini propose des skills, appelés « compétences » en français.

Conditions : avoir au moins 18 ans, être connecté·e, activer **Conserver l'activité**. L'import d'un zip se fait seulement dans l'application web, sur gemini.google.com.

1. Ouvrez le menu, puis **Personnaliser**, puis **Compétences** (en anglais : **Customize > Skills**).
2. Cliquez sur **Créer**, puis **Importer**.
3. Choisissez `scouts.zip`, puis **Ouvrir**.
4. Relisez la compétence, puis cliquez sur **Créer**.

Le total des fichiers importés ne doit pas dépasser 100 Mo.

État des essais : fonctionnel.

Sources : [aide de Gemini, compétences](https://support.google.com/gemini?p=b_ws_skills&hl=fr), [limites des fichiers](https://support.google.com/gemini/answer/14903178?hl=fr), [Gems](https://support.google.com/gemini/answer/15146780?hl=fr).

## Mistral Le Chat, Microsoft Copilot

Pas testé. À vous de voir si l'import d'un zip est possible.

## Vérifier la version

Demandez à l'assistant : « Quelle est la version du skill scouts ? ». Indiquez cette version quand vous [signalez une erreur](signaler.md). Pour passer à une nouvelle version, voir [Mettre à jour les skills](web-mettre-a-jour.md).

## Et ensuite

Voir [Utiliser le skill](web-utiliser.md) pour des exemples de demandes.

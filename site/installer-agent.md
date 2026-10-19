---
title: Installer avec un agent
order: 2
description: "Installer les skills scouts et scouts-ressources dans Claude Code, Codex, Pi ou un autre agent, avec npx skills ou à la main."
---

Cette page s'adresse aux personnes qui utilisent un agent en ligne de commande : Claude Code, Codex, Pi ou un autre outil compatible avec le format [Agent Skills](https://agentskills.io). Pour claude.ai, ChatGPT ou Gemini dans le navigateur, voir [Installer sur une plateforme web](installer-web.md).

Les deux skills se trouvent dans le dossier `skills/` du dépôt [fuzoh/scouts-skills](https://github.com/fuzoh/scouts-skills) : `skills/scouts` et `skills/scouts-ressources`. Pour choisir, voir l'[accueil](index.md#deux-skills-lequel-choisir).

## Méthode universelle : `npx skills`

L'outil [`skills`](https://github.com/vercel-labs/skills) installe un skill pour un ou plusieurs agents. Il demande Node.js (commande `npx`).

Voir les skills du dépôt sans rien installer :

```sh
npx skills add fuzoh/scouts-skills --list
```

Installer `scouts` dans le projet courant (l'outil demande pour quels agents) :

```sh
npx skills add fuzoh/scouts-skills --skill scouts
```

Options utiles :

| Option | Effet |
|---|---|
| `-g` | Installation pour votre compte (tous vos projets) au lieu du projet courant. |
| `-a claude-code`, `-a codex`, `-a pi` | Agent visé ; répéter l'option pour plusieurs agents, `-a '*'` pour tous. |
| `-y` | Pas de question de confirmation. |
| `--copy` | Copie les fichiers au lieu de créer des liens symboliques. |

Exemples :

```sh
# scouts pour Claude Code, pour tous vos projets
npx skills add fuzoh/scouts-skills --skill scouts -g -a claude-code

# scouts-ressources pour Codex et Pi, dans le projet courant
npx skills add fuzoh/scouts-skills --skill scouts-ressources -a codex -a pi
```

Où vont les fichiers :

| Agent | Projet | Compte (`-g`) |
|---|---|---|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex, Pi | `.agents/skills/` | `~/.agents/skills/` |

Quand plusieurs agents sont choisis, le skill est copié une fois dans `.agents/skills/` et Claude Code reçoit un lien symbolique vers cette copie.

Autres commandes :

```sh
npx skills list            # skills installés dans le projet (ajouter -g pour le compte)
npx skills update          # mettre à jour les skills installés (-g ou -p pour choisir la portée)
npx skills remove scouts   # retirer un skill
```

Essayer `scouts` sans l'installer : `npx skills use fuzoh/scouts-skills --skill scouts` affiche un prompt prêt à coller dans un agent.

### Depuis un zip de release

Chaque version publie deux zips :

- `https://github.com/fuzoh/scouts-skills/releases/latest/download/scouts.zip`
- `https://github.com/fuzoh/scouts-skills/releases/latest/download/scouts-ressources.zip`

`npx skills add` accepte ces adresses. Par défaut, l'outil refuse une archive de plus de 1 000 fichiers. Le zip de `scouts-ressources` en contient environ 2 000 : relevez la limite avec la variable d'environnement `SKILLS_EXTRACT_MAX_FILES`.

```sh
npx skills add https://github.com/fuzoh/scouts-skills/releases/latest/download/scouts.zip

SKILLS_EXTRACT_MAX_FILES=2000 npx skills add \
  https://github.com/fuzoh/scouts-skills/releases/latest/download/scouts-ressources.zip
```

Installer depuis le dépôt (`fuzoh/scouts-skills`) n'est pas concerné par cette limite.

## Claude Code

Avec `npx skills` : `-a claude-code` (voir plus haut).

À la main : copiez le dossier du skill dans `~/.claude/skills/` (tous vos projets) ou dans `.claude/skills/` à la racine d'un projet. Le fichier `SKILL.md` doit se trouver directement dans `~/.claude/skills/scouts/`.

```sh
git clone https://github.com/fuzoh/scouts-skills.git
mkdir -p ~/.claude/skills
cp -R scouts-skills/skills/scouts ~/.claude/skills/
```

Claude Code prend en compte un nouveau skill pendant la session. Si le dossier `skills/` n'existait pas au démarrage, lancez `/reload-skills`. Pour appeler le skill explicitement : `/scouts`. Sinon, il se déclenche seul quand votre demande parle de scoutisme. Source : [documentation Claude Code](https://code.claude.com/docs/en/skills).

## Codex

Codex lit les skills dans `~/.agents/skills/` (votre compte) et dans `.agents/skills/` (un projet, du dossier courant jusqu'à la racine du dépôt). Avec `npx skills` : `-a codex`. À la main : copiez `skills/scouts` dans l'un de ces dossiers.

Pour appeler le skill : tapez `$` puis son nom, ou `/skills`. Si un skill installé n'apparaît pas, redémarrez Codex. Source : [documentation Codex](https://learn.chatgpt.com/docs/build-skills).

## Pi

Pi peut installer tout le dépôt comme paquet :

```sh
pi install git:github.com/fuzoh/scouts-skills
```

Pi trouve alors `scouts` et `scouts-ressources` dans le dossier `skills/` du dépôt. Ajoutez `-l` pour une installation limitée au projet courant. Mise à jour : `pi update git:github.com/fuzoh/scouts-skills` (ou `pi update --extensions` pour tous vos paquets ; `pi update` seul met à jour Pi lui-même).

Pi lit aussi `~/.agents/skills/` et `.agents/skills/` : `npx skills add … -a pi` ou une copie à la main fonctionnent également. Pour appeler le skill explicitement : `/skill:scouts`. Sources : [skills](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md) et [paquets](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/packages.md) de Pi.

## Autres agents

Cursor, GitHub Copilot (CLI, VS Code), OpenCode, Gemini CLI et d'autres lisent `.agents/skills/`. Utilisez `npx skills add` avec l'option `-a` de votre agent ; la liste des noms se trouve dans le [README de `skills`](https://github.com/vercel-labs/skills#supported-agents).

## Vérifier la version installée

Demandez à l'assistant : « Quelle est la version du skill scouts ? ». Ou lisez la ligne `version` dans `SKILL.md` (bloc `metadata` en tête du fichier) ou dans `MANIFEST.md`. Indiquez cette version quand vous [signalez une erreur](signaler.md). Pour passer à une nouvelle version, voir [Mettre à jour les skills](mettre-a-jour.md).

## Ce qui a été testé

Essais du 19.10.2026 avec `skills` 1.7.2 et Pi 1.3.0, depuis une copie locale du dépôt :

- `npx skills add <dépôt> --list` trouve `scouts` et `scouts-ressources`, et rien d'autre.
- Installation dans un projet (`-a claude-code -a codex -a pi`) et pour le compte (`-g`) : fichiers aux emplacements du tableau ci-dessus.
- Zip de `scouts` : installé. Zip de `scouts-ressources` : refusé (1 954 fichiers, maximum 1 000), puis installé avec `SKILLS_EXTRACT_MAX_FILES=2000`.
- `pi install <dépôt>` : Pi trouve les deux skills (`/skill:scouts`, `/skill:scouts-ressources`).

Depuis GitHub, après publication (19.10.2026, `skills` 1.7.2, version 0.2.0 des skills) :

- `npx skills add fuzoh/scouts-skills --list` trouve les deux skills.
- `--skill scouts -a claude-code -a codex` et `--skill scouts-ressources -a pi` : installés dans `.agents/skills/`, lien symbolique dans `.claude/skills/` ; contenu identique au dépôt.
- `npx skills update -p` : « All project skills are up to date ».
- Zips de la dernière release avec `-g -a claude-code` : les deux installés (`scouts-ressources` avec `SKILLS_EXTRACT_MAX_FILES=2000`).

Non testé : `pi install git:…` et `pi update` depuis GitHub ; une vraie mise à jour d'une version à la suivante ; l'utilisation réelle des skills dans Codex et Pi.

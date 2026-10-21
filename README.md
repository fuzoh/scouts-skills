# scouts-skills

Deux skills d'assistant IA pour les responsables, formateur·ices, coachs et experts J+S du scoutisme suisse. Ils s'appuient sur les ressources officielles : MSdS, commission formation, Jeunesse+Sport et cudesch. Tout est en français.

Version actuelle : 0.6.0 <!-- x-release-please-version -->

- **`scouts`** (principal) : répond à une question de règle, de délai ou de chiffre, explique une notion, corrige ou conçoit un document (activité J+S, unité d'apprentissage, programme de camp, concept de sécurité) et guide qui débute. Léger, sans corpus.
- **`scouts-ressources`** : la même méthode, avec le corpus officiel embarqué. Il cite le texte exact, section par section. Pour qui veut la source.

Ces skills ne sont pas des documents officiels. Vérifiez toujours une règle importante dans la source qu'ils indiquent.

## Installer

Mode d'emploi complet : **https://fuzoh.github.io/scouts-skills/**

- **claude.ai** : télécharger [`scouts.zip`](https://github.com/fuzoh/scouts-skills/releases/latest/download/scouts.zip), puis l'importer dans *Customize > Skills*.
- **Agent en ligne de commande** (Claude Code, Codex, Pi…) : `npx skills add fuzoh/scouts-skills --skill scouts`
- Version avec corpus : [`scouts-ressources.zip`](https://github.com/fuzoh/scouts-skills/releases/latest/download/scouts-ressources.zip), ou `--skill scouts-ressources`.

### Faire installer par l'agent

Dans un agent en ligne de commande, il suffit de demander :

> Installe-moi les skills scouts dans le projet actuel, suis : https://github.com/fuzoh/scouts-skills

### Instructions pour un agent qui installe

Utiliser [`npx skills`](https://github.com/vercel-labs/skills) (Node.js requis), sans mode interactif :

```sh
npx skills add fuzoh/scouts-skills --skill scouts -a <agent> -y
```

- `<agent>` : l'agent qui exécute la commande (`claude-code`, `codex`, `pi`, `cursor`, `opencode`, `gemini-cli`, `github-copilot`…). Répéter `-a` pour plusieurs agents. Liste complète dans le [README de `skills`](https://github.com/vercel-labs/skills#supported-agents).
- Skill par défaut : `scouts`. Installer `scouts-ressources` (`--skill scouts-ressources`) seulement si l'utilisateur veut le corpus ou les citations exactes ; `--skill scouts --skill scouts-ressources` pour les deux.
- Portée par défaut : le projet courant (`.claude/skills/` pour Claude Code, `.agents/skills/` pour les autres). Ajouter `-g` seulement si l'utilisateur demande une installation pour tous ses projets.
- La commande crée aussi `skills-lock.json` à la racine du projet ; le laisser.
- Ensuite, dire à l'utilisateur comment appeler le skill (`/scouts` dans Claude Code, `$scouts` dans Codex, `/skill:scouts` dans Pi ; sinon il se déclenche seul quand on parle de scoutisme) et qu'une nouvelle session peut être nécessaire pour qu'il apparaisse.
- Mise à jour : `npx skills update scouts -y`.

## Personnaliser, construire sa version

Dans un agent, les skills se personnalisent avec un dossier `scouts-perso/` : réglages, règles locales, contacts et documents du groupe, de l'association cantonale ou du cours ([Personnaliser](https://fuzoh.github.io/scouts-skills/agent-personnaliser.html)). Ce dossier peut aussi servir à construire une version dérivée, sous un autre nom, pour un agent ou en zip pour le navigateur ([Construire sa version](https://fuzoh.github.io/scouts-skills/agent-construire.html)) :

> Fais-moi une version des skills scouts avec mes documents, suis : https://github.com/fuzoh/scouts-skills

### Instructions pour un agent qui construit une version

1. Vérifier `git --version` et `uv --version`. Sans `uv`, donner à l'utilisateur la commande d'installation de https://docs.astral.sh/uv/getting-started/installation/ et attendre. `just` est facultatif : utiliser les commandes `uv run`.
2. Trouver le dossier perso : `scouts-perso/` du projet courant, sinon `~/scouts-perso/`. Aucun : le créer d'abord avec l'utilisateur en suivant `skills/scouts/references/personnaliser.md` de ce dépôt. Chaque ligne de la table « Fiches » doit avoir son « sert à » (pas de `À COMPLÉTER`).
3. Demander un suffixe court (`monac`, `cours-base` : minuscules, chiffres, tirets). Les skills s'appelleront `scouts-<suffixe>` et `scouts-ressources-<suffixe>`, à côté des officiels.
4. Cloner hors du projet de l'utilisateur, sauf s'il indique un autre endroit : `git clone https://github.com/fuzoh/scouts-skills ~/scouts-skills` (déjà cloné : `git -C ~/scouts-skills pull`).
5. Construire, depuis le clone : `uv run build all --perso <chemin absolu du dossier perso> --suffixe <suffixe> --zip`. Un refus nomme sa cause (réglage inconnu, `À COMPLÉTER`, plus de 100 fichiers, fiche trop longue) : corriger le dossier perso avec l'utilisateur, puis relancer.
6. Installer dans l'agent courant, dans le projet courant sauf demande contraire (`-g`) : `npx skills add ~/scouts-skills/build/scouts-<suffixe> -a <agent> -y`. `scouts-ressources-<suffixe>` seulement si l'utilisateur veut le corpus.
7. Donner à l'utilisateur le chemin des zips pour le navigateur (`~/scouts-skills/dist/scouts-<suffixe>.zip` ; `scouts-ressources-<suffixe>.zip` pour ChatGPT seulement) et lui rappeler qu'ils contiennent ses fiches et ses contacts.
8. Ne jamais commiter ni pousser `scouts-perso/`, `build/` ou `dist/`. Mise à jour : `git -C ~/scouts-skills pull`, puis les pas 5 et 6.

Pour ajouter des sources officielles au corpus (fork), voir la page [Construire sa version](https://fuzoh.github.io/scouts-skills/agent-construire.html) et `CONTRIBUTING.md`.

## Signaler une erreur, proposer une amélioration

Ouvrez une [issue](https://github.com/fuzoh/scouts-skills/issues/new/choose) : un formulaire guide la démarche. N'y collez jamais de données personnelles.

## Intentions

- Rendre les ressources du scoutisme suisse faciles à trouver, à citer et à appliquer, pour les groupes comme pour les équipes de formation.
- Partir des documents officiels, convertis en markdown, indexés et cités, plutôt que de la mémoire d'un modèle.
- Garder des skills autoportants, compatibles avec les agents en ligne de commande et avec les applications web.
- Tenir le tout à jour avec des outils rejouables quand une source change.

## Contribuer

Ce dépôt est aussi la fabrique des skills : collecte des sources, conversion, index, référentiels et build. Voir [`CONTRIBUTING.md`](CONTRIBUTING.md) et [`METHODE.md`](METHODE.md).

## Licences

- Code : [MIT](LICENSE).
- Contenu propre (skills, référentiels, savoirs, site, documentation) : [CC BY-SA 4.0](LICENSE-CONTENT).
- Textes officiels (sections de `sources/`, `corpus/` de `scouts-ressources`) : droits réservés à leurs auteurs. Voir la [liste des sources](https://fuzoh.github.io/scouts-skills/sources.html).

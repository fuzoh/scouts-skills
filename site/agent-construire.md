---
title: Construire sa version des skills
order: 26
menu: Construire sa version
parcours: agent
description: "Construire depuis un clone ou un fork votre propre version des skills scouts, avec les documents de votre association cantonale, de votre groupe ou de votre cours, pour un agent ou pour le navigateur."
---

[Personnaliser](agent-personnaliser.md) suffit pour vous seul·e, dans votre agent. Construire sa version va plus loin : vous fabriquez un skill complet qui embarque vos documents et vos règles, sous un nom à vous (`scouts-monac`, `scouts-cours-base`…). Vous pouvez ensuite l'installer dans un agent, ou en faire un zip à importer dans claude.ai, ChatGPT ou Gemini, par exemple pour toute une équipe de cours.

Deux chemins :

- **Avec un dossier perso** (le cas courant) : vos documents restent dans un dossier `scouts-perso/`, le dépôt officiel est seulement cloné. Rien n'est publié.
- **Avec vos propres sources officielles** : un fork du dépôt, où vous ajoutez des documents au corpus par le même pipeline que le mainteneur. Plus long, réservé à qui veut maintenir une version suivie.

Les commandes sont testées sous Linux. Sous Mac et Windows, elles n'ont pas été essayées.

## Le plus simple : le demander à l'agent

Dans Claude Code, Codex ou un autre agent :

> Fais-moi une version des skills scouts avec mes documents, suis : https://github.com/fuzoh/scouts-skills

L'agent lit les instructions du dépôt, vérifie les outils, prépare votre dossier perso si vous n'en avez pas encore, vous demande un nom court, construit les skills et les installe. La suite de cette page décrit ce qu'il fait.

## Prérequis

- [`git`](https://git-scm.com/downloads) et [`uv`](https://docs.astral.sh/uv/getting-started/installation/) (qui installe Python tout seul).
- [`just`](https://just.systems) est facultatif : chaque recette `just` a son équivalent `uv run`.
- Un dossier `scouts-perso/` rempli, voir [Personnaliser](agent-personnaliser.md). Chaque ligne de sa table « Fiches » doit avoir son « sert à » : la construction refuse une ligne `À COMPLÉTER`.

## Avec un dossier perso

```sh
git clone https://github.com/fuzoh/scouts-skills
cd scouts-skills
just perso ~/scouts-perso monac
# sans just : uv run build all --perso ~/scouts-perso --suffixe monac --zip
```

`monac` est le suffixe de votre version : minuscules, chiffres et tirets. Il donne deux skills, `scouts-monac` et `scouts-ressources-monac`, qui s'installent **à côté** des skills officiels sans les écraser.

La construction :

- remplace les réglages du skill par ceux de votre `README.md` ;
- copie vos règles locales, contacts et index dans `references/perso.md` ;
- copie vos fiches dans `perso/`, mais jamais les fichiers originaux ;
- vérifie que `scouts-monac` reste importable dans le navigateur : 100 fichiers au plus, fiches pas trop longues. Si vos fiches font dépasser la limite, la construction s'arrête et dit pourquoi.

Résultat :

| Fichier | Usage |
|---|---|
| `build/scouts-monac/`, `build/scouts-ressources-monac/` | à installer dans un agent |
| `dist/scouts-monac.zip` | à importer dans claude.ai, ChatGPT ou Gemini ([Installer dans le navigateur](web-installer.md)) |
| `dist/scouts-ressources-monac.zip` | ChatGPT seulement (trop lourd ailleurs) |

`build/` et `dist/` ne sont jamais versionnés : vos documents ne quittent pas votre ordinateur.

### Installer

```sh
npx skills add ./build/scouts-monac -a claude-code -y        # projet courant
npx skills add ./build/scouts-monac -a claude-code -y -g     # tous vos projets
uv run build install --skill scouts --suffixe monac          # ou : lien dans ~/.claude/skills/
```

Remplacez `claude-code` par votre agent (`codex`, `pi`…). Distribuez le zip à votre équipe pour un usage dans le navigateur.

### Mettre à jour

Quand une nouvelle version officielle sort ([Nouveautés](nouveautes.md)), ou quand votre dossier perso change :

```sh
git pull
just perso ~/scouts-perso monac
```

Puis réinstallez (`npx skills add …` à nouveau) ou réimportez le zip. Avec `build install`, le lien suit la nouvelle construction tout seul.

## Avec vos propres sources officielles (fork)

Pour ajouter au corpus des documents officiels que le dépôt n'a pas, et les faire relire, citer et découper comme les autres.

1. **Fork** du dépôt sur GitHub. Un fork d'un dépôt public est public : pour des documents internes, créez plutôt un dépôt privé et poussez-y un clone.
2. **Désactivez les workflows** du fork (*Settings > Actions*, ou supprimez `release-please.yml`, `pages.yml` et `veille.yml` de `.github/workflows/`) : ils publient des versions, un site et des issues au nom du dépôt.
3. **Ajoutez vos sources** : `ingest` → `convert` → `index` → `split`, puis les référentiels ou savoirs qui les citent. La méthode est dans `METHODE.md` et la page [Contribuer](contribuer.md). Les originaux (`sources/*/original/`) restent hors git.
4. **Construisez** sous votre nom : `uv run build all --suffixe monac --zip` écrit `skills/scouts-monac/` et `skills/scouts-ressources-monac/`. Commitez-les pour que `npx skills add <vous>/<dépôt> --skill scouts-monac` fonctionne. Ajoutez `--perso` si vous voulez aussi un dossier perso, mais alors la sortie va dans `build/`, jamais dans le dépôt.
5. **Suivez l'amont** :

   ```sh
   git remote add upstream https://github.com/fuzoh/scouts-skills
   git fetch upstream
   git merge upstream/main
   ```

   Relancez ensuite la construction. Une correction utile à tous mérite une [issue](signaler.md) ou une pull request sur le dépôt officiel.

## Prudence

- Un dossier perso contient des noms et des numéros : ne le commitez jamais dans un dépôt public. Vérifiez que `scouts-perso/` est dans le `.gitignore` de vos projets.
- Un zip construit avec `--perso` contient vos fiches et vos contacts : partagez-le seulement avec les personnes concernées.
- Ce que vous ajoutez n'est pas relu par le mainteneur : les réponses `[perso]` engagent votre version, pas les skills officiels.

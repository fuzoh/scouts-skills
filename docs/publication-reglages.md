# Réglages GitHub après le premier push

Actions manuelles pour le mainteneur, à faire une fois le dépôt `fuzoh/scouts-skills` créé et poussé (les workflows et formulaires sont dans `.github/`). Dans l'ordre.

## 1. Pousser le code et le tag

```bash
git remote add origin git@github.com:fuzoh/scouts-skills.git
git push -u origin main
git push origin v0.2.0   # indispensable : release-please retrouve la dernière version par ce tag
```

Sans le tag `v0.2.0` sur GitHub, release-please ne trouve aucune release précédente et reprend tout l'historique (il faudrait alors `"bootstrap-sha"` dans `release-please-config.json`, SHA du commit initial, voir `git rev-list --max-parents=0 HEAD`). Avec le tag, `bootstrap-sha` est inutile : release-please cherche d'abord une release GitHub, puis se rabat sur le tag `v<version du manifeste>`.

## 2. Autoriser les workflows à ouvrir des PR

Settings > Actions > General > Workflow permissions : cocher **Allow GitHub Actions to create and approve pull requests**. Les permissions par défaut peuvent rester en lecture : chaque workflow déclare les siennes.

## 3. Secret `RELEASE_PLEASE_TOKEN`

Un jeton personnel (et non `GITHUB_TOKEN`) fait que le PR de release et le tag déclenchent la CI.

1. GitHub > Settings (du compte) > Developer settings > Personal access tokens > Fine-grained tokens > Generate new token.
2. Resource owner : `fuzoh`. Repository access : **Only select repositories** > `scouts-skills`. Expiration : à choisir (le jeton expire, prévoir le renouvellement).
3. Permissions du dépôt : **Contents : Read and write**, **Pull requests : Read and write**, **Issues : Read and write** (release-please pose des étiquettes `autorelease: …` sur les PR) ; Metadata : Read-only s'ajoute seul.
4. Enregistrer le secret :

```bash
gh secret set RELEASE_PLEASE_TOKEN --repo fuzoh/scouts-skills
```

Source : le README de `googleapis/release-please-action` n'énumère pas les permissions du jeton ; il demande `contents`, `issues` et `pull-requests` en écriture pour `GITHUB_TOKEN`, d'où cette liste équivalente.

## 4. GitHub Pages

Settings > Pages > Build and deployment > Source : **GitHub Actions**. Le workflow `pages.yml` publie ensuite `build/site/` à chaque nouveau tag `v*`, donc à chaque release (le site affiche toujours une version publiée). Environments > github-pages > Deployment branches and tags : ajouter la règle de tag `v*` à côté de `main` (fait le 2026-10-19), sinon le déploiement depuis un tag est refusé. Déploiement manuel : Actions > Site > Run workflow, en choisissant le tag. Adresse : `https://fuzoh.github.io/scouts-skills/`.

## 5. Étiquettes

Les formulaires d'issue n'ajoutent que des étiquettes qui existent déjà ; les créer :

```bash
gh label create contenu      --repo fuzoh/scouts-skills --color d73a4a --description "Règle, chiffre ou délai faux dans un skill"
gh label create suggestion   --repo fuzoh/scouts-skills --color a2eeef --description "Idée d'amélioration"
gh label create installation --repo fuzoh/scouts-skills --color fbca04 --description "Problème d'installation d'un skill"
gh label create veille       --repo fuzoh/scouts-skills --color 0e8a16 --description "Contrôle mensuel des liens des sources"
```

release-please crée lui-même `autorelease: pending` et `autorelease: tagged`.

## 6. Protection de la branche `main` (facultatif)

Settings > Rules > Rulesets > New branch ruleset, cible `main` :

- Require a pull request before merging (le mainteneur peut se laisser un contournement) ;
- Require status checks to pass : **Tests, validation et skills/ à jour** (job `verifier` de `ci.yml`) ;
- Block force pushes.

Le PR de release est ouvert avec le jeton personnel, donc la CI s'y exécute : l'attendre avant de fusionner.

## 7. Publier la release `v0.2.0`

Le PR de release suivant (par exemple `0.3.0`) créera tag, release et zips tout seul. Pour avoir dès maintenant une release `v0.2.0` avec ses zips (lien stable `https://github.com/fuzoh/scouts-skills/releases/latest/download/scouts.zip`) :

```bash
uv run light index && uv run build all --zip
gh release create v0.2.0 --repo fuzoh/scouts-skills --verify-tag --title v0.2.0 \
  --notes "Première version publique des skills scouts et scouts-ressources (voir CHANGELOG.md)." \
  dist/scouts.zip dist/scouts-ressources.zip
```

La release doit être publiée par ce chemin manuel : le job `upload` de `release-please.yml` ne se lance que lorsque release-please vient de la créer.

## 8. Vérifications après le premier push

- Actions > CI : vert sur `main` ; artefacts `scouts.zip` et `scouts-ressources.zip` présents (7 jours).
- Actions > Release : le job `release-please` ouvre un PR « chore(main): release … » dès qu'un commit `feat` ou `fix` suit `v0.2.0`. Dans ses journaux, pas d'avertissement « No entries modified » pour `uv.lock`.
- Le PR de release modifie `pyproject.toml`, `uv.lock`, `README.md`, `skills/*/SKILL.md` et `skills/*/MANIFEST.md` ; sa CI doit rester verte (`uv sync --locked` et `skills/` à jour). Si `uv.lock` n'est pas touché, retirer `--locked` de `ci.yml` ou lancer `uv lock` dans le PR.
- Après la fusion du PR de release : le job `upload` joint les deux zips à la release.

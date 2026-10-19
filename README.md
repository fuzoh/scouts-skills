# scouts-skills

Deux skills d'assistant IA pour les responsables, formateur·ices, coachs et experts J+S du scoutisme suisse. Ils s'appuient sur les ressources officielles : MSdS, commission formation, Jeunesse+Sport et cudesch. Tout est en français.

Version actuelle : 0.4.0 <!-- x-release-please-version -->

- **`scouts`** (principal) : répond à une question de règle, de délai ou de chiffre, explique une notion, corrige ou conçoit un document (activité J+S, unité d'apprentissage, programme de camp, concept de sécurité) et guide qui débute. Léger, sans corpus.
- **`scouts-ressources`** : la même méthode, avec le corpus officiel embarqué. Il cite le texte exact, section par section. Pour qui veut la source.

Ces skills ne sont pas des documents officiels. Vérifiez toujours une règle importante dans la source qu'ils indiquent.

## Installer

Mode d'emploi complet : **https://fuzoh.github.io/scouts-skills/**

- **claude.ai** : télécharger [`scouts.zip`](https://github.com/fuzoh/scouts-skills/releases/latest/download/scouts.zip), puis l'importer dans *Customize > Skills*.
- **Agent en ligne de commande** (Claude Code, Codex, Pi…) : `npx skills add fuzoh/scouts-skills --skill scouts`
- Version avec corpus : [`scouts-ressources.zip`](https://github.com/fuzoh/scouts-skills/releases/latest/download/scouts-ressources.zip), ou `--skill scouts-ressources`.

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

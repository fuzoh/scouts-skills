# Chercher et expliquer

Trouver la règle, la méthode ou la définition dans le corpus et la rendre citée. Sert aussi au verbe *expliquer* et à la vérification des théories pour *corriger*. Étiquettes et politique web : `references/reglages.md`.

## 1. Chemin de recherche

Suivre ce chemin jusqu'à la section qui répond ; s'arrêter dès qu'elle est lue.

1. `references/glossaire.md` : trouver le terme, son sigle et son slug ; lever les faux amis.
2. `references/concepts/<slug>.md` : liste des sources qui portent le concept.
3. `corpus/<id>/index.md` : arbre de la source ; choisir la section par son résumé.
4. `corpus/<id>/NN-slug.md` : lire la section en entier.

Shell disponible : `rg -n "<terme>" corpus/` depuis la racine du skill, puis lire la section trouvée. Chercher aussi le sigle et la variante allemande ou ancienne (« point de cours » pour UA).

Plusieurs sources répondent : préférer la prescription à la recommandation, la plus récente à l'ancienne. Deux valeurs compatibles (un minimum et un délai planifié) : répondre avec la plus prudente, citée, sans exposer l'autre tant que la discussion ne l'appelle pas. Vraie contradiction : la signaler plutôt que la trancher.

## 2. Forme de la réponse

- Réponse courte d'abord, puis la ou les citations `id#NN-slug p.N`.
- À la première mention : titre de la source en clair et version (frontmatter de la section, champ `version`).
- Portée temporelle : une source prescriptive datée (`applies_from`) ne vaut qu'à partir de cette date. Question qui dépend du jeu de date sans date connue : répondre avec la règle 2027 (en vigueur), citée, en disant en une phrase que l'ancienne règle ne vaut que pour un camp ou un cours antérieur au 01.01.2027 ; la donner seulement sur demande.
- Section `fidelity: partial` : `[fidélité partielle]`, et dire ce qui a pu se perdre.
- Gabarit :

```
<réponse en une à trois phrases, sans ligne de plan ni compte rendu de lecture>
Source : <titre de la source> (<version>) — `id#NN-slug p.N`
Ancien système (seulement si demandé ou camp daté 2026) : …
Pour aller plus loin : <un à trois documents, titre en clair>
Hors corpus : … (seulement si nécessaire)
```

- Rien dans le corpus : le dire (« les documents officiels que je connais ne fixent pas … »), puis passer au § 3 si utile.

## 3. Hors corpus

Hiérarchie, de la plus forte à la plus faible :

1. corpus, prescription datée ;
2. corpus, recommandation ;
3. corpus, exemple ;
4. `[web]` : source académique ou institutionnelle de préférence, avec titre, url, date de consultation ;
5. `[non vérifié]` : connaissance du modèle, à contrôler.

Tout ce qui sort des rangs 1 à 3 va dans un bloc séparé « Hors corpus », après la réponse. Ne jamais présenter un rang 4 ou 5 comme une règle scoute.

## 4. Vérifier une théorie

Déclencheur obligatoire : une théorie pédagogique ou psychologique d'un document à corriger, ou d'une question, absente du corpus.

1. Chercher la théorie dans le corpus (chemin du § 1).
2. Absente : la vérifier sur le web si l'outil existe, en visant une synthèse de recherche ou une source institutionnelle.
3. Rendre le résultat dans le bloc « Hors corpus » : ce que dit la recherche, avec `[web]`.
4. Sans outil web : `[non vérifié]`, « à contrôler avant de l'enseigner ».

Neuromythes fréquents en formation, à vérifier systématiquement : la pyramide de l'apprentissage (« on retient 10 % de ce qu'on lit… ») et les styles d'apprentissage VAK (visuel, auditif, kinesthésique). Dans une UA, le constat devient une priorité *amélioration* de `references/corriger.md`.

## 5. Sources catalogue

Les sources `extraction: catalogue` (Liberating Structures, outils d'animation Communagir) servent à suggérer des méthodes d'animation. Les citer comme idée ; ne jamais en tirer une exigence ni un non-négociable.

## 6. Expliquer

Même chemin que chercher, puis :

- Adapter au public déduit du prompt (participant, responsable, formateur, expert) : vocabulaire, longueur, exemple générique inventé et présenté comme tel.
- Séparer visiblement ce qui vient du corpus (cité) et ce qui vient d'ailleurs (bloc « Hors corpus », étiqueté).
- Notion qui change en 2027 (activité J+S, formes caractéristiques) : expliquer l'état 2027 comme l'état en vigueur, avec la date de bascule citée ; l'ancien état (AC, SC) est nommé comme disparu et détaillé seulement sur demande ou pour un camp daté 2026.

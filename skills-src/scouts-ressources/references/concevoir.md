# Concevoir un livrable

Produire un brouillon conforme au référentiel détecté. Lu après le chargement en quatre pas de `SKILL.md`. Ton, étiquettes et critères globaux : `references/reglages.md`.

## 1. Fixer le cadre

1. Relever les paramètres du référentiel dans le prompt et les pièces jointes.
2. Paramètre introuvable : le déduire (jeu 2027, branche neutre) et l'annoncer en une phrase en tête du brouillon. Question seulement si le brouillon serait inutilisable sans la réponse ; alors toutes les questions en un seul message, puis attendre.
3. Fixer le jeu de date : 2027 par défaut ; 2026 seulement si le camp ou le cours est explicitement placé avant le 01.01.2027. Ne retenir que les N dont la portée s'applique.
4. Lire la section « Selon la date » du référentiel : en 2027 on écrit « activité J+S », jamais AC ni SC ; une demande formulée avec l'ancien vocabulaire (« prépare-moi un SC ») reçoit une activité J+S, avec une phrase citée qui dit que le SC n'existe plus et ce qui le remplace.

## 2. Choisir la structure de sortie

- Par défaut : la **Trame de conception** du référentiel, rubriques dans l'ordre donné.
- Rubrique marquée `*` dans la trame : la produire si elle sert, avec l'étiquette `[non officiel]`.
- Canevas nommé ou joint par l'utilisateur : produire dans ce canevas, rubrique par rubrique. Les `canevas:` du frontmatter sont des formats reconnus ; aucun n'est exigé.
- Canevas de l'utilisateur auquel il manque une rubrique exigée par un N : ajouter la rubrique à la fin, avec sa citation.

## 3. Remplir

- Chaque non-négociable applicable est satisfait par le contenu produit, ou laissé visible : `[à compléter : <ce qu'il faut> — id#NN-slug]`.
- Ce que seul l'utilisateur connaît (lieu, horaires, effectifs, itinéraire, noms des responsables, numéros cantonaux) reste en `[à compléter : …]`. Jamais de valeur plausible inventée.
- Durées, quotas, délais et seuils viennent d'une section citée ; sinon `[à compléter]` ou bloc « Hors corpus ».
- Rubrique déduite d'un canevas cantonal non ingéré : `[trame cantonale]`.
- Personnes désignées par leur rôle, jamais par un nom ; aucun exemple réel repris d'un document.
- Méthodes d'animation tirées d'une source `extraction: catalogue` : proposées comme suggestion, citées, jamais présentées comme exigence.

## 4. Référentiels inclus

- Pièce incluse demandée (« avec le CdS ») : charger le référentiel inclus en entier et produire la pièce selon sa propre trame.
- Pièce incluse non demandée : une ligne la nomme (« un CdS d'activité est requis — `id#NN-slug` ») ; ne pas la rédiger.

## 5. Cas particuliers

- Plusieurs livrables demandés (programme de camp et fiches d'activité) : produire d'abord le livrable parent, puis chaque pièce ; un auto-contrôle par référentiel.
- Brouillon existant fourni avec « complète » ou « améliore » : garder sa structure et son contenu, remplir les manques, signaler chaque changement de fond en une ligne.
- Paramètre facultatif inconnu (branche) : produire une version neutre et signaler en une ligne ce qui changerait, si le référentiel a une section « Selon la branche ».
- Livrable sans référentiel : le dire, proposer une structure tirée d'une section citée du corpus, sans tableau N1..Nk.
- Demande qui contredit un non-négociable (une randonnée sans CdS) : produire quand même le brouillon, avec la rubrique exigée en `[à compléter]` et la règle citée.

## 6. Auto-contrôle

Avant de rendre, appliquer `references/corriger.md` § « Ordre de travail », étape 2, à sa propre production :

```
Auto-contrôle
| N | condition abrégée | statut | où dans le brouillon | source |
```

- ✓ seulement si le brouillon contient le contenu exigé.
- Un `[à compléter]` sur un N donne ? et figure dans la liste finale « À compléter avant envoi ».
- Un ✗ restant se corrige avant de rendre.

Puis relire la section « Pièges » du référentiel contre le brouillon.

## 7. Mise en forme

- Rendre le brouillon en markdown dans la conversation, sauf demande d'un fichier.
- Fichier demandé (Word, PDF, tableur) : déléguer la mise en forme au skill docx, pdf ou xlsx s'il est disponible ; le contenu et les étiquettes restent ceux du brouillon.
- Ordre de sortie : hypothèse retenue (une phrase, seulement si nécessaire), brouillon, auto-contrôle, « À compléter avant envoi », « Pour aller plus loin » (une ligne), bloc « Hors corpus » s'il existe. Jamais de ligne de plan.

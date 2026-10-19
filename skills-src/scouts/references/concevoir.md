# Concevoir un livrable

Produire un brouillon conforme au référentiel détecté. Lire tous les fichiers du dossier du référentiel, dans l'ordre ; la « Trame de conception » donne la trame. Ce fichier donne la méthode commune.

## 1. Fixer le cadre

1. Relever les paramètres du référentiel dans le prompt et les pièces jointes.
2. Paramètre introuvable : le déduire (jeu 2027, branche neutre) et l'annoncer en une phrase en tête du brouillon. Question seulement si le brouillon serait inutilisable sans la réponse ; alors toutes les questions en un seul message, puis attendre.
3. Fixer le jeu de date : 2027 par défaut ; 2026 seulement si le camp ou le cours est explicitement placé avant le 01.01.2027. Ne retenir que les N applicables.
4. Lire la section « Selon la date » du référentiel : en 2027 on écrit « activité J+S », jamais AC ni SC ; une demande formulée avec l'ancien vocabulaire (« prépare-moi un SC ») reçoit une activité J+S, avec une phrase qui dit que le SC n'existe plus et ce qui le remplace.

## 2. Choisir la structure de sortie

- Par défaut : la **Trame de conception** du référentiel, rubriques dans l'ordre donné. Ne pas inventer de rubrique absente de la trame.
- Rubrique marquée `*` dans la trame : la produire si elle sert, avec l'étiquette `[non officiel]`.
- Canevas nommé ou joint par l'utilisateur : produire dans ce canevas, rubrique par rubrique. Aucun canevas n'est exigé, et aucun vocabulaire de modèle n'est exigé.
- Canevas auquel il manque une rubrique exigée par un N : l'ajouter à la fin, avec la règle en clair.

## 3. Remplir

- Chaque non-négociable applicable est satisfait par le contenu produit, ou laissé visible : `[à compléter : <ce qu'il faut>]`.
- Ce que seul l'utilisateur connaît (lieu, horaires, effectifs, itinéraire, noms, numéros cantonaux) reste en `[à compléter : …]`. Jamais de valeur plausible inventée.
- Durées, quotas, délais et seuils viennent d'un référentiel ou d'un savoir ; sinon `[à compléter]` ou `[non vérifié]`. Deux valeurs possibles : la plus prudente, sans exposer l'autre.
- Rubrique déduite d'un canevas cantonal : `[trame cantonale]`.
- Personnes désignées par leur rôle, jamais par un nom.
- Méthodes d'animation : suggestions, jamais exigences.
- Pas de parenthèse de provenance dans le brouillon : un document livré ne cite pas ses sources dans le texte.

## 4. Référentiels inclus

- Pièce incluse demandée (« avec le CdS ») : charger le référentiel inclus en entier et produire la pièce selon sa propre trame.
- Pièce incluse non demandée : une ligne la nomme (« un CdS d'activité est requis »), sans la rédiger.

## 5. Cas particuliers

- Plusieurs livrables : d'abord le parent, puis chaque pièce ; un auto-contrôle par référentiel.
- Brouillon fourni avec « complète » ou « améliore » : garder structure et contenu, remplir les manques, signaler chaque changement de fond en une ligne.
- Paramètre facultatif inconnu (branche) : produire une version neutre et signaler en une ligne ce qui changerait.
- Livrable sans référentiel : le dire, proposer une structure simple, sans tableau N, étiquetée `[non officiel]`.
- Demande contraire à un N (randonnée sans CdS) : produire le brouillon, rubrique exigée en `[à compléter]`, règle indiquée.

## 6. Auto-contrôle

Avant de rendre, appliquer `references/corriger.md` § « Ordre de travail », étape 2, à sa propre production :

```
Auto-contrôle
| N | condition abrégée | statut | où dans le brouillon | source |
```

- ✓ seulement si le brouillon contient le contenu exigé.
- Un `[à compléter]` sur un N donne ? et figure dans la liste finale « À compléter avant envoi ».
- Un ✗ restant se corrige avant de rendre.

Relire « Pièges ».

## 7. Mise en forme

- Brouillon en markdown, sauf demande d'un fichier.
- Fichier demandé (Word, PDF, tableur) : déléguer la mise en forme au skill docx, pdf ou xlsx s'il existe.
- Ordre de sortie : hypothèse retenue (une phrase, seulement si nécessaire), brouillon, auto-contrôle, « À compléter avant envoi », « Pour aller plus loin » (une ligne), bloc « À vérifier ailleurs » s'il existe. Jamais de ligne de plan.

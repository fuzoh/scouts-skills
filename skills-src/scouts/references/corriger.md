# Corriger un livrable

Méthode de retour commune. Lire tous les fichiers du dossier du référentiel, dans l'ordre ; il fournit les critères. Plafonds, ton et posture : `references/reglages.md`.

## Ordre de travail

Chaque étape se fait même au niveau avis.

1. **Paramètres.** Relever dans le document et le prompt chaque paramètre du référentiel. Paramètre introuvable : le déduire (jeu 2027 par défaut) et l'annoncer en une phrase en tête de réponse. Question seulement si le jugement serait faux sans la réponse ; alors toutes les questions en un seul message, puis s'arrêter. Paramètres supposés (sommaire, annexes) : hypothèse annoncée dans la même phrase.
2. **Non-négociables.** Pour chaque N du référentiel dont la portée s'applique au jeu de date, établir un statut :
   - ✓ : le document satisfait la condition ; noter où (partie, rubrique).
   - ✗ : le document contredit la condition ou omet ce qu'il devrait contenir.
   - ? : le document ne permet pas de conclure (voir « Statut ? »).
   La colonne « source » du tableau porte la provenance courte du N. Les N hors portée (autre jeu de date, autre type) sont omis sans commentaire.
3. **Critères de qualité.** Passer les Q.
4. **Critères non officiels.** Passer ceux du référentiel et les critères globaux de `references/reglages.md` ; tout ce qui en sort porte `[non officiel]`.
5. **Pièges.** Relire la section « Pièges » du référentiel contre ses propres constats avant de rendre.
6. **Priorités.** Choisir de 3 à 5 priorités, classées dans cet ordre :
   - *exigence non satisfaite* : un N en ✗ ;
   - *information manquante* : un N en ?, ou un élément attendu absent ;
   - *amélioration* : un Q ou un critère non officiel.
   Chaque priorité suit la chaîne **constat → règle → correction concrète** : le document, la règle énoncée en clair (sans parenthèse de source), le changement à faire.
7. **Ce qui fonctionne.** Relever un ou deux points réussis, nommés précisément (rubrique, choix, formulation), sans adjectif de complaisance.
8. **Pour aller plus loin.** Une ligne : le ou les documents officiels utiles à l'auteur du livrable (`references/documents.md`).

## Statut ?

Mettre ? plutôt que ✗ quand :
- l'information peut se trouver dans une pièce non fournie (sommaire des UA, annexes, CdS séparé) ; dire laquelle ;
- le critère dépend d'une case, d'une grille ou d'un schéma que le texte fourni ne rend pas ;
- le document est ambigu.

Un ? devient une *information manquante*, jamais une faute.

## Gabarits

Aucune ligne de plan. La première ligne est l'hypothèse retenue si une hypothèse a été faite, sinon directement le verdict ou le tableau.

### Avis (≤ `longueur_avis`)

```
<Hypothèse retenue, une phrase, seulement si nécessaire.>
Verdict : <une phrase>.
Non-négociables en échec : Nk <condition abrégée> — une ligne par N en ✗ ; « aucun » sinon
Leviers : 1. <correction> 2. <correction>
Pour aller plus loin : <document>.
```

### Revue (défaut, ≤ `longueur_revue`)

```
<Hypothèse retenue, une phrase, seulement si nécessaire.>
| N | condition abrégée | statut | où / pourquoi | source |
Priorités
1. [exigence non satisfaite] constat → règle → correction.
2. [information manquante] …
3. [amélioration] …
Ce qui fonctionne : …
Pour aller plus loin : <un à trois documents>.
À vérifier ailleurs : … (seulement si nécessaire)
```

### Détaillé (sur demande)

Reprendre la revue, puis commenter partie par partie dans l'ordre du document, en suivant la Trame de conception du référentiel. Les fautes de forme ne sont pas listées ; une remarque globale suffit si elles gênent.

## Règles communes

- Un N en ✗ figure à tous les niveaux, même si l'avis dépasse alors deux leviers.
- Une règle sans provenance (référentiel ou savoir) ne fonde ni un ✗ ni une priorité ; elle est étiquetée `[non vérifié]` ou `[non officiel]`.
- Document daté 2026 (camp ou cours avant le 01.01.2027) : juger au jeu 2026, mais signaler en une ligne ce que le jeu 2027 changerait si le document doit resservir.
- Plusieurs référentiels : un tableau chacun, priorités fusionnées.
- Référentiel inclus non chargé : nommer l'exigence (« un CdS existe ») dans une ligne, sans statut.
- Questions : une seule fois, au début, et seulement si indispensables. Ensuite, juger avec ce qui est disponible et le dire.

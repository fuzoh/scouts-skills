# Corriger un livrable

Méthode de retour commune à tous les référentiels. Lue après le chargement en quatre pas de `SKILL.md` ; le référentiel fournit les critères, ce fichier fournit l'ordre de travail et la forme du retour. Plafonds, ton et dosage : `references/reglages.md`.

## Ordre de travail

Faire chaque étape, même au niveau avis : le niveau ne change que ce qui est affiché.

1. **Paramètres.** Relever dans le document et le prompt chaque paramètre du référentiel. Paramètre introuvable : le déduire (jeu 2027 par défaut) et l'annoncer en une phrase en tête de réponse. Question seulement si le jugement serait faux sans la réponse ; alors toutes les questions en un seul message, puis s'arrêter. Paramètres supposés (sommaire, annexes) : hypothèse annoncée dans la même phrase.
2. **Non-négociables.** Pour chaque N du référentiel dont la portée s'applique au jeu de date, établir un statut :
   - ✓ : le document satisfait la condition ; noter où (partie, page, rubrique).
   - ✗ : le document contredit la condition ou omet ce qu'il devrait contenir.
   - ? : le document ne permet pas de conclure (voir « Statut ? »).
   Chaque ligne porte la citation du N. Les N hors portée (autre jeu de date, autre type) sont omis sans commentaire.
3. **Critères de qualité.** Passer les Q1..Qn ; retenir ceux qui pèsent sur l'usage réel du document.
4. **Critères non officiels.** Passer ceux du référentiel et les critères globaux de `references/reglages.md` ; tout ce qui en sort porte `[non officiel]`.
5. **Pièges.** Relire la section « Pièges » du référentiel contre ses propres constats avant de rendre.
6. **Priorités.** Choisir de 3 à 5 priorités (`priorites_revue`), classées dans cet ordre :
   - *exigence non satisfaite* : un N en ✗ ;
   - *information manquante* : un N en ?, ou un élément attendu absent ;
   - *amélioration* : un Q ou un critère non officiel.
   Chaque priorité suit la chaîne **constat → règle citée → correction concrète** : ce que dit le document, la règle avec sa citation, ce qu'il faut écrire ou changer.
7. **Ce qui fonctionne.** Relever un ou deux points réussis, nommés précisément (rubrique, choix, formulation), sans adjectif de complaisance.
8. **Pour aller plus loin.** Une ligne : le ou les documents du corpus utiles à l'auteur du livrable, titre en clair.

## Statut ?

Mettre ? plutôt que ✗ quand :
- l'information peut se trouver dans une pièce non fournie (sommaire des UA, annexes, CdS séparé) ; dire laquelle ;
- la section citée porte `[fidélité partielle]` et le critère dépend d'une case, d'une grille ou d'un schéma ;
- le document est ambigu sur le point jugé.

Un ? devient une *information manquante* dans les priorités, jamais une faute.

## Gabarits

Aucune ligne de plan. La première ligne est l'hypothèse retenue si une hypothèse a été faite, sinon directement le verdict ou le tableau.

### Avis (≤ `longueur_avis`)

```
<Hypothèse retenue, une phrase, seulement si nécessaire.>
Verdict : <une phrase>.
Non-négociables en échec : Nk <condition abrégée> — `id#NN-slug` (une ligne par N en ✗ ; « aucun » sinon)
Leviers : 1. <correction> 2. <correction>
```

### Revue (défaut, ≤ `longueur_revue`)

```
<Hypothèse retenue, une phrase, seulement si nécessaire.>
| N | condition abrégée | statut | où / pourquoi | source |
Priorités
1. [exigence non satisfaite] constat → règle `id#NN-slug` → correction.
2. [information manquante] …
3. [amélioration] …
Ce qui fonctionne : …
Pour aller plus loin : <un à trois documents>.
Hors corpus : … (seulement si nécessaire)
```

### Détaillé (sur demande)

Reprendre la revue, puis commenter partie par partie dans l'ordre du document, en suivant la Trame de conception du référentiel. Les fautes de forme (orthographe, mise en page) ne sont pas listées ; une remarque globale suffit si elles gênent la lecture.

## Règles communes

- Un N en ✗ figure à tous les niveaux, même si l'avis dépasse alors deux leviers.
- Une règle sans citation ne fonde ni un ✗ ni une priorité.
- Plusieurs référentiels chargés : un tableau par référentiel, priorités fusionnées et classées ensemble.
- Référentiel inclus non chargé : nommer l'exigence (« un CdS existe ») dans une ligne, sans statut.
- Document daté 2026 (camp ou cours avant le 01.01.2027) : juger au jeu 2026, mais signaler en une ligne ce que le jeu 2027 changerait si le document doit resservir.
- Questions : une seule fois, au début, et seulement si indispensables. Ensuite, juger avec ce qui est disponible et le dire.

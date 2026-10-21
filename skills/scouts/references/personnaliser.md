# Personnaliser

Pour qui veut que l'assistant tienne compte de son groupe, de son association cantonale ou de son cours : réglages (tutoiement, niveau), règles locales, contacts, documents propres. Tout vit dans un dossier `scouts-perso/`, hors du dossier du skill : une mise à jour du skill remplace son dossier en entier.

## 1. Vérifier l'accès aux fichiers

La personnalisation demande un dossier **persistant**, lisible et modifiable d'une conversation à l'autre : un agent ouvert sur un projet (Claude Code, Codex, Antigravity…). Application web (claude.ai, ChatGPT, Gemini), bac à sable effacé en fin de conversation ou aucun accès aux fichiers : le dire en deux phrases et renvoyer à https://fuzoh.github.io/scouts-skills/personnaliser.html. La procédure s'arrête là.

## 2. Trouver ou créer le dossier

- Chercher `scouts-perso/README.md` à la racine du projet courant, puis `~/scouts-perso/README.md`. Le premier trouvé est **le** dossier perso ; l'autre est ignoré, sans fusion.
- Aucun : le créer à la racine du projet, ou dans `~` si la personne veut les mêmes réglages dans tous ses projets. `README.md` = gabarit du § 6 ; sous-dossiers `ac/` (association cantonale), `groupe/`, `cours/`, `originaux/`.
- Projet sous git (`.git/` présent) : proposer d'ajouter `scouts-perso/` au `.gitignore`, car le dossier contient des noms et des numéros. L'ajouter après accord.

## 3. Remplir le profil par dialogue

Au plus trois questions par message, dans cet ordre : rôle et branche ; réglages ; règles du groupe, de l'AC ou du cours ; contacts. Écrire chaque réponse dans sa rubrique au fil du dialogue ; une rubrique sans réponse reste vide. Montrer le `README.md` à la fin.

- **Réglage** : une clé de `references/reglages.md` et sa nouvelle valeur. Une demande hors des clés devient une règle locale.
- **Règle locale** : une ligne, la règle puis son origine (décision de la maîtrise, directive de l'AC, fiche du dossier). Elle ajoute ou durcit. Une règle qui assouplit un non-négociable, une règle de sécurité ou d'urgence (délai plus court, encadrement plus faible, mesure retirée) reste hors du fichier : dire laquelle et pourquoi.
- **Contact** : rôle, nom, comment le joindre, pour quoi. Coach J+S, CàF, Helpline ou cellule de crise cantonale, responsable de groupe.

## 4. Ajouter un document

Formats : PDF, docx, pptx, xlsx, md, txt. Dossier : `ac/`, `groupe/` ou `cours/`, déduit du document, sinon demandé. Liste de participants, fiche médicale, tout document sur des personnes : refuser, il n'a pas sa place ici.

**Avec le script** : quand `scripts/ajouter.py` existe dans le dossier du skill et que `uv --version` répond.

```
uv run <dossier du skill>/scripts/ajouter.py <fichier> --dossier groupe --perso <chemin de scouts-perso>
```

Le script copie l'original dans `originaux/`, découpe le texte par titres en fiches, refuse un doublon (même sha256) et ajoute la ligne d'index avec `À COMPLÉTER`. Lire les fiches créées, puis remplacer `À COMPLÉTER` par le « sert à ».

**Sans script** (pas de `scripts/`, pas de `uv`, ou échec du script) : lire le document, puis écrire les fiches au format du § 6. Texte du document découpé par titres, ni résumé ni reformulé ; tableaux en markdown ; une fiche par partie, 17 000 caractères au plus (~ 5 000 tokens), une partie plus longue se coupe à un sous-titre. Copier l'original dans `originaux/`. Ajouter la ligne d'index.

Fini quand chaque partie du document est dans une fiche, l'original dans `originaux/` et la ligne d'index remplie.

## 5. Tenir l'index

- Table « Fiches » : une ligne par document, `| <dossier>/<slug>/ | sert à |`. « Sert à » ≤ 160 caractères : les questions auxquelles le document répond.
- `README.md` entier ≤ 7 000 caractères (~ 2 000 tokens), car il est lu à chaque question. Au-delà : raccourcir les « sert à », regrouper des règles locales.
- Retirer un document : son dossier de fiches, son original et sa ligne.
- Modifier un réglage ou une règle : réécrire la ligne en place, sans historique.

## 6. Formats

`scouts-perso/README.md` :

```markdown
# scouts-perso

Personnalisation des skills scouts, lue par l'assistant à chaque question. Rester court. Aucune information sur les participants.

## Profil
- **rôle** :
- **branche** :
- **unité, groupe ou cours** :

## Réglages
Clés de `references/reglages.md` du skill ; la valeur remplace celle du skill.

## Règles locales
Ajoutent ou durcissent une règle officielle, jamais ne l'assouplissent. Une ligne : règle — origine.

## Contacts
| rôle | nom | joignable | pour |
|---|---|---|---|

## Fiches
| dossier | sert à |
|---|---|
```

Fiche `scouts-perso/<dossier>/<slug>/NN-<slug-de-partie>.md` (`slug` : minuscules, tirets, sans accents ; `NN` : 01, 02… dans l'ordre du document) :

```markdown
---
document: Titre du document
partie: Titre de la partie
original: originaux/nom-du-fichier.pdf
sha256: empreinte de l'original
ajoute_le: AAAA-MM-JJ
---

# Titre de la partie

Texte du document.
```

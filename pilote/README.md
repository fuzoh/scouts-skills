# Pilote

Archive. Les skills sont en bêta : publiés, testés sur les IA cibles, utilisés par de vrais testeurs. Pas de grille à rejouer à chaque version. Les retours se traitent au fil de l'eau.

## Dans le dépôt

- `tests-manuels.md` : ancienne grille de cas fictifs. N'est plus un passage obligé.

## Hors dépôt

Le **jeu d'essai sur dossiers réels** (`pilote/cas/<code>/`, `cas/INDEX.md`) reste local et git-ignoré, même anonymisé : une anonymisation faite à la main n'est jamais garantie à 100 %. Il sert au mainteneur à mesurer ce qu'un correcteur ou un concepteur relève (activités J+S `A*`, unités d'apprentissage `U*`, programmes de camp `P*`, concepts de sécurité `S*`). Règles de constitution, pour qui en monte un chez soi :

- **Anonymisé.** Prénoms, noms, totems de personnes, initiales de responsables, e-mails, téléphones privés, adresses privées, IBAN, plaques et dates de naissance sont remplacés par des marqueurs de rôle stables dans chaque fichier : `[RESP-n]`, `[FORMATEUR-n]`, `[PARTICIPANT-n]`, `[COACH]`, `[RG]`, `[MÉDECIN]`, `[CONTACT-TERRAIN]`, `[CELLULE-CRISE-n]`, `[TEL]`, `[EMAIL]`, `[ADRESSE]`, `[IBAN]`, `[PLAQUE]`. Restent : groupes scouts, lieux de camp, communes, hôpitaux, numéros officiels (144, 117, 118, 1414, 145, Helpline 0800 22 36 39, numéros du mova).
- **Texte extrait seulement.** Pas de fichier original (docx, xlsx, pdf), pas d'image. Le texte vient de `build/terrain/` (extraction par `scripts/terrain.py`), nettoyé des images et des cellules vides ; les tableaux Excel sont aplatis et lisibles à peine, ce qui est voulu : le skill doit s'en accommoder.
- **Aucune donnée personnelle.** Une anonymisation faite à la main n'est jamais garantie à 100 % : ne jamais le diffuser.
- **Rien ici n'est une source.** Ni `id`, ni citation `id@version`, ni copie dans `sources/` ou `skills/`. Un skill ne cite jamais ce contenu ; il sert uniquement à mesurer ce qu'un correcteur ou un concepteur relève.
- Le frontmatter de chaque fichier donne `cas`, `role`, `origine` (type, année, branche, jamais le chemin ni le nom du camp), `format_origine` et `anonymise: true`.
- Ne jamais committer ce jeu ni un original : les dossiers réels restent dans `documents/` (git-ignoré), puis hors dépôt.

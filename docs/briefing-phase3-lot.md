# Briefing Phase 3 — procédure d'un lot

Procédure commune aux agents qui traitent un lot de sources (`docs/briefing-phase3.md` donne le contexte). Lire aussi `METHODE.md` (Flux de conversion, Citation) et l'exemple complet `sources/cofor-checklist-cours-base/` (`index.md`, `01-contenu.md`, `source.yaml`).

## Règles de collaboration

- Plusieurs agents travaillent en parallèle sur des lots disjoints : **ne toucher que `sources/<id>/` des ids du lot**. Ne pas éditer `scripts/`, `METHODE.md`, `ROADMAP.md`, `INVENTORY.md`, `GLOSSARY.md`, ne pas commiter. Un bug bloquant d'un script : contourner dans `index.md` à la main et le signaler dans le rapport final.
- `raw.md` est déjà écrit (`convert` lancé en lot) : ne jamais l'éditer. Le relancer seulement s'il manque.
- Rapport final (court) : par id le statut atteint, les problèmes de qualité, les `concepts` posés (surtout les nouveaux), les bugs d'outils.

## Document court (< 15 pages, docx, xlsx, pptx court)

1. Lire `raw.md`. Si le texte utile est absent ou dérisoire (poster, schéma, tableau en image, formulaire vide) : `extraction: vision`, `status: triaged`, supprimer `raw.md`, noter la raison dans `notes`. Sinon continuer.
2. `just index <id>` → `index.md` à une entrée `01-contenu.md`. Vérifier titre et plage `p.1-N` (= `pages` du yaml). xlsx : une entrée par feuille, sans plage. pptx : `p.N` = diapo.
3. Rédiger le résumé (une ligne, 15-40 mots, ce que contient le document et où : « objectifs (p.1), contenus par branche (p.2-4) »).
4. `just split <id>` → `01-contenu.md`. Vérifier le frontmatter et que le texte est complet.
5. Dans `source.yaml` : `concepts: [...]`, `status: indexed`, compléter `notes` si la conversion a perdu quelque chose (cases à cocher, colonnes, images).

## Manuel (≥ 15 pages)

1. `pdfinfo sources/<id>/original/*.pdf` et `uv run python -c "import fitz;print(len(fitz.open('<pdf>').get_toc()))"` : signets ? Oui → `just index <id>`. Non → `just index <id> --pageindex`.
2. Corriger `index.md` à la main contre `raw.md` (et la table des matières imprimée, souvent p.2-4 de `raw.md`) :
   - retirer couverture, impressum, table des matières, pages blanches ; garder au plus 3 niveaux ;
   - `§` = numéro imprimé du chapitre (`§3.2`) ; sans numérotation, omettre `§` ;
   - plages `p.A-B` en **pages physiques** (marqueurs `<!-- p.N -->`), contiguës, sans chevauchement entre frères, enfants dans le parent ; un nœud garde ses pages moins celles de ses enfants ;
   - `page_offset` = page physique − page imprimée (vérifier sur deux pages) ; `toc_source: agent` si l'arbre a été largement réécrit ;
   - une section > ~300 lignes de `raw.md` : la découper en sous-sections ;
   - fichiers `NN-slug.md` numérotés dans l'ordre, slug ASCII court.
3. `just split <id>` ; corriger jusqu'à passage.
4. Résumés : pour chaque `NN-slug.md`, une ligne 15-40 mots. En lot via `claude -p` (modèle haiku ou sonnet), par exemple :
   `cat sources/<id>/03-x.md | claude -p --model haiku "Résume en une phrase (15-40 mots, français, sans préambule) ce que contient cette section d'un manuel de formation scoute/J+S : sujets traités, outils ou règles donnés."`
   Reporter les résumés dans `index.md` après ` : `, puis relancer `just split <id>`.
5. `source.yaml` : `concepts`, `status: indexed`, `notes` (qualité du texte : colonnes mélangées, illustrations perdues, chapitres à ignorer).

## Concepts

`concepts:` = slugs kebab-case sans accents, réutiliser l'existant (`rg -I "^concepts:" sources/*/source.yaml | sort -u` et `GLOSSARY.md`) : `unite-d-apprentissage`, `activite-de-camp`, `sport-de-camp`, `cours-de-base`, `cours-ru`, `cours-panorama`, `chef-de-cours`, `caf`, `qualification`, `retour`, `accompagnement`, `modele-de-formation`, `niveau-d-approfondissement`, `coach-js`, `expert-js`, `profil-du-scoutisme`, `branches`, `relations`, `methodes-scoutes`, `securite`, `psa`, `regles-de-comportement`, `ethique`, `inclusion`, `administration-de-cours`, `financement`, `camp`, `trekking`, `eau`, `hiver`, `montagne`, `objectifs-d-apprentissage`, `methodes-d-enseignement`, `evaluation`, `planification`, `physis`, `psyche`, `sport-des-enfants`, `jeu`. Créer un nouveau slug seulement si rien ne convient ; le lister dans le rapport. 3 à 8 concepts par source.

## Leçons de la première vague (manuels)

- `index --pageindex` donne souvent un arbre faux (nœuds en double, sous-chapitres sortis de leur chapitre, phrases prises pour des titres). Partir de la **table des matières imprimée** de `raw.md`, repérer chaque titre dans le PDF (`pymupdf`, `page.search_for`) pour la page physique, réécrire l'arbre, `toc_source: agent`.
- `index` depuis les signets importe parfois des signets en allemand ou en double (PDF bilingues J+S) : les retirer.
- Les sections changent souvent en milieu de page et `split` refuse le chevauchement : arrondir à la page, regrouper deux sections qui partagent une page dans un même nœud (« §2.2.7 … ; 2.2.8 … »), laisser au chapitre sa première sous-section si elles partagent la page, pour qu'aucun fichier ne sorte vide.
- Un parent dont toutes les pages sont dans ses enfants reçoit un fichier sans texte (`split` avertit) : lui écrire un résumé de renvoi vers ses sous-sections, c'est accepté.
- `page_offset` : vérifier sur plusieurs pages ; en cas de doubles pages, retenir l'offset du corps principal et documenter les exceptions dans `notes`.
- Résumés haiku : relire, retirer les préambules (« Ce passage… ») et corriger les attributions (haiku résume parfois seulement la dernière fiche d'un groupe).
- `raw.md` est régénéré avec un convertisseur qui reprend les pages masquées par les graphismes ; vérifier quand même les pages à illustrations, tableaux et fiches (le texte peut être dans l'ordre des blocs, pas de lecture).

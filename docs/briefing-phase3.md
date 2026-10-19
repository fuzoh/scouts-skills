# Briefing Phase 3 — conversion, index, découpage

Pour l'agent qui mène la Phase 3. Lire d'abord `AGENTS.md`, `METHODE.md` (Flux de conversion, Citation), `DECISIONS.md` (index/PageIndex, raw.md/index.md/split), `ROADMAP.md`. Les choix sont pris, les appliquer.

## État au 2026-10-17

- 119 sources, toutes triées ; `cofor-checklist-cours-base` est le seul exemple complet (`indexed`) : s'en inspirer pour `index.md`, `notes`, `concepts`.
- Aucun `raw.md` ailleurs. `INVENTORY.md` à jour. `just check` et `just test` (31 tests) verts.
- Outils en place : `convert` (pdf, docx, xlsx, pptx, web avec `--render`), `index` (`--pageindex` pour un PDF sans signets, `just install-pageindex` déjà exécutable), `split`.

## But

Chaque source `keep` passe à `converted` puis `indexed` (index validé, sections découpées, `concepts` remplis), par lots homogènes, un commit par lot. `verified` est posé par l'humain.

## Ordre

1. **Sources citées par `ancien skills/`** (correcteur UA, AC, SC) : les repérer, elles passent en premier. Probables : trilogie `msds-le-cours`, `msds-unite-d-apprentissage`, `msds-retour-qualifier-accompagner`, `msds-modele-de-formation`, check-lists cofor, fiches Pano, `js-manuel-experts`, `js-manuel-sport-de-camp-trekking`, `msds-profil-du-scoutisme`.
2. Documents courts (< 15 pages) : un seul `01-contenu.md`, `index.md` à une entrée, résumé par l'agent en session. Ils peuvent se traiter en série (cofor, fiches J+S).
3. Manuels : `index --pageindex` si pas de signets (`pdfinfo` ou le squelette l'indique), corriger titres, plages, `§`, `page_offset` ; résumés en lot par `claude -p` ; `split`.
4. Sources web : `convert --render` ; `index.md` web (`- Titre <url> → NN-slug.md : résumé`).
5. `extraction: catalogue` (Phase 3 aussi) : communagir, liberatingstructures (voir `docs/liens-a-ingerer.md`) ; `autre-camp-equitable-documents` candidat.
6. `extraction: vision` (3 sources) : différé, ne rien convertir.

## Pièges connus

- Formulaires AcroForm (check-lists, autorisation, évaluation, charte, hajk) : cases à cocher perdues ; voir `notes` de chaque source.
- PDF chiffrés AES (5 manuels J+S) : pymupdf lit le texte, vérifier la qualité du `raw.md` (polices, colonnes).
- Jeux de cartes J+S (3 sources) : une carte par page, texte court.
- Poster, schéma une page (`js-poster-regles-de-comportement`, `js-developpement-equipe-moniteurs`) : si `raw.md` vide, passer en `vision`.
- `msds-modele-de-formation` : original = export en ligne (sha256 du site) ; l'export local précédent, même contenu, est dans `history`.
- Les anciens skills citent peut-être des pages de la pagination imprimée : `p.N` est la page physique, `page_offset` fait le lien.

## Hors périmètre

Skills et build (Phase 4), check_urls (Phase 5), nouvelles sources (sauf la version en ligne du modèle de formation si nécessaire).

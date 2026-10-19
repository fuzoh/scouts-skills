# Briefing Phase 2 — ingestion et triage

Pour l'agent qui mène la Phase 2. Lire d'abord `AGENTS.md`, `METHODE.md` (table des commandes, section Sources web), `DECISIONS.md`, `docs/taxonomie.md`, `docs/liens-a-ingerer.md`. Les choix sont pris, les appliquer.

## But

Vider `documents/` : chaque fichier devient une source `triaged` (ou `rejected`), avec `id`, `title`, `issuer`, `ref`, `version`, `published`, `audience`, `themes`, `extraction`, et autant que possible `url` / `file_url`. Critère de fin : `documents/` vide, `just check` vert, `INVENTORY.md` régénéré, un commit par lot.

Pas de conversion ni d'indexation en Phase 2 (Phase 3), sauf pour vérifier un outil.

## État au 2026-10-17

- Phase 1 livrée : `ingest`, `inventory`, `convert`, `index` (+ `--pageindex`), `split`, `discover`, 29 tests, `just check` vert.
- 1 source : `cofor-checklist-cours-base` (`indexed`).
- `documents/` : 121 entrées, dont 2 dossiers de PNG allemands, 4 docx, 3 xlsx, 2 pptx, 1 png, le reste PDF.
- Non testé en réel : `discover --render`, `convert --render`, `ingest --batch manifeste`, PDF chiffrés AES (pymupdf les ouvre sans mot de passe utilisateur, à confirmer sur « Manual J+S - Bases.pdf »).

## Faits sur le corpus

**Doublons (sha256 identique, supprimer le `(1)` avant le lot) :**
- `313601fr_fiche_dinformation_pour_les_cours_panorama_le_projet_au_pano (1).pdf`
- `314601fr-approfondissement_branche_eclais-v1-20260915-cofor (1).pdf`

`T (1).pdf` n'est pas un doublon de `T.pdf` (hash différent).

**Fichiers sans nom, identifiés par la première page (tous J+S, extranet ILIAS) :**

| fichier | contenu | pages |
|---|---|---|
| `T.pdf` | 3.3 Course d'orientation photos (exemple d'activité SC/T) | 2 |
| `T (1).pdf` | Exemple de programme général pour camp d'été J+S | 1 |
| `T (2).pdf` | 5.2b Estafette de fromage avec les berger·e·s | 4 |
| `T (3).pdf` | 7.2 Organisation d'une grande fête | 4 |
| `T (4).pdf` | Randonnée avec nuitée, exemple de dossier pour la formation | 10 |
| `T (5).pdf` | 5.1a Tournoi de jeux / Fête des jeux | 6 |
| `T pour coachs.pdf` | Check-list coach : séquences d'activité physique complémentaires (SAPC) | 2 |
| `T pour responsable de camp.pdf` | Check-list responsable de camp : SAPC | 2 |
| `_Trekking.pdf` | Manuel Sport de camp / Trekking pour les enfants et les jeunes | 80 |
| `Manuel_cle.pdf` | Manuel clé J+S (OFSPO) | 44 |
| `Manuel pour experts.pdf` | Manuel J+S/esa pour les experts, 140 p. ; comparer avec `Manuel J+S esa pour experts.pdf` (136 p.) : deux versions, garder la plus récente, l'autre en `history` ou `rejected` | 140 |

Les six exemples d'activités `T*.pdf` sont de bons candidats à un regroupement : soit une source par fiche (`js-exemple-course-orientation-photos`…), soit `rejected` si les skills n'en ont pas l'usage. Décision du mainteneur au triage.

**Chiffrés AES** (lisibles par pymupdf) : manuels J+S Bases, Coach, Trekking, experts.

**Scanné, une page** : `fr_ausbildungsmodell_fur_webseite-20231201_1.pdf` → `extraction: vision`.

**Images** : `Illustrationen Pfadiprofil/`, `Illustrationen Beziehungen und Methoden/` (dossiers, `--type image`, `lang: de`), `_Livelli di insegnamento.png` (italien, probablement `rejected`), `_Soluzione del gioco di immagini a pagina 6.pdf` (italien, `rejected`).

**Hors français** : `Turnierformen_f.pdf`, `LS-T_*_f.pdf`, `Bro_*_f_screen.pdf`, `Sicherheit_bei_JS_f.pdf`, `Gewalt_f.pdf`, `MTB_f.pdf`, `OL_Norda_f.pdf` : le suffixe `_f` = version française d'un document J+S, titre de fichier allemand. Vérifier la langue à la première page avant de poser `lang`.

## Lots

Un lot = un `documents/lot.yaml` préparé par l'agent, validé par l'humain, puis `just ingest --batch documents/lot.yaml` (le fichier est supprimé après). Un commit par lot : `feat(sources): lot cofor`. Ordre :

1. **cofor** (~25 fichiers) : préfixes `30xxxx`-`31xxxx` fr, check-lists RU et approfondissements de branche, fiches pano, concept CàF, évaluation du cours, administration et financement des cours, listes de buts (docx), budget et check-list CàF (xlsx), VAE (xlsx + docx). `ref` = numéro `3xxxxxfr` ; `published` dans le nom quand présent (`-20260915-`).
2. **msds** (~15) : profil du scoutisme (`212002fr`), modèle de formation 2027, organigramme (`501201fr`), PSA (`215402`), jeux de prévention (`216401fr`), inclusion (`215001fr`, `215101fr`), ancre, pilote, ticket, commande hajk, caisse de cours, aide-mémoire données de base, communiqué aquascout, flyer PTA, règlement grandes manifestations, nouveautés MSdS/J+S 2027, offre MPE 2027, illustrations (image).
3. **js** (~50) : manuels (Bases, Coach, SC/T 2026, esa experts, experts coachs, Manuel clé, Trekking), brochures Kindersport, Physis, Psyché, apprentissage, planification, communication, sécurité, LS-T (montagne, camp, eau, hiver), éthique (dossiers, poster, charte, boussole), coach (brochures, check-list docx + pdf), SAPC, exemples d'activités `T*.pdf`, Sport et handicap, blessures, Rega, mobilesport, PPT éthique et introduction manuel experts, séquences numériques.
4. **cudesch** (~3) : `table-des-matieres-detaillees-cudesch-fr-20150219-lobo.pdf`, `pbs_202003_leitpfadihilfsmittel_funkae...fr_es.pdf`, La trilogie « Le cours », « L'unité d'apprentissage », « Faire un retour, qualifier et accompagner » (01/02/03) est éditée par le MSdS (impressum p.2) : lot **cofor** ou **msds**, à trancher au triage.
5. **autre** : `camp_equitable_apercu_documents.pdf`, `liens-utiles.pdf`, `factsheet_francais_1.pdf`, items italiens → `issuer_detail` ou `rejected`.

Pour chaque entrée du lot : `file, id, title, issuer, ref, version, published, audience, themes`. Le `type` est déduit de l'extension. Règles d'id dans `METHODE.md` (≤ 40 caractères : `js-manuel-sport-de-camp-trekking` passe, `js-manuel-js-esa-pour-les-experts-coachs` non, raccourcir).

## Triage

Après l'ingestion d'un lot, l'agent propose dans chaque `source.yaml` : `decision: keep | rejected`, `extraction`, `audience`, `themes` (≤ 3), `lang`, `notes`. L'humain valide, le statut passe à `triaged` (commit `feat(sources): triage lot cofor`). `rejected` : supprimer `original/`, garder le yaml avec `rejected_reason`.

## URL canoniques

1. `just discover https://pfadi.swiss/fr/formation-encadrement/cudesch/ --depth 2 --out build/pfadi.yaml`, puis `just discover https://pfadi.swiss/fr/publications-telechargements/downloads/ --depth 1 --render --out build/pfadi-downloads.yaml` (catalogue en JS, `just install-web` d'abord). Les pages de détail `downloads/detail/<n>/<slug>/` redirigent en 302 vers `/media/files/<xx>/<fichier>.pdf` : `discover` doit les voir comme fichiers (vérifier ; sinon ajuster la détection par Content-Type après redirection).
2. `just ingest --match build/pfadi-downloads.yaml` : remplit `url`/`file_url` par sha256, pose `stale` sur les mêmes noms à hash différent.
3. J+S : fichiers venant de l'extranet ILIAS ou de jugendundsport.ch ; `url` = page publique si elle existe, sinon `""` et `notes: "extranet ILIAS J+S"`.

## Sources web (en parallèle, voir `docs/liens-a-ingerer.md`)

- hering.scout.ch (SPA) : `discover --render`, une source `msds-hering-camps`, sections = pages.
- cudeschin.pbs.ch : vérifier le français ; sinon rejet.
- Article mobilesport : `just ingest --url <url> --id js-ethique-proximite-soutien`.
- communagir, liberatingstructures : `extraction: catalogue`, Phase 3.

## Pièges connus

- `ingest` refuse tout le lot si une entrée est mauvaise et ne déplace rien : corriger puis relancer.
- Les fichiers en `original/` gardent leur nom d'origine ; ne pas renommer à la main (le sha256 ne change pas, mais `--match` par nom en dépend).
- Formulaires PDF (check-lists cofor) : cases à cocher perdues à la conversion, à noter dans `notes` (voir `cofor-checklist-cours-base`).
- `index` sans `--pageindex` ne voit que les titres en police plus grande ; pour tout manuel sans signets, utiliser `--pageindex` (`just install-pageindex`).

## Hors périmètre

Conversion, index, split des sources (Phase 3) ; tool.jeunesseetsport.ch ; skills ; `check_urls` ; `build`.

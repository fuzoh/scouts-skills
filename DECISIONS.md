# Décisions

État courant. Une décision changée se réécrit ici. Pas d'historique, pas de date de journal. Les dates ci-dessous sont des dates d'application.

`METHODE.md` porte le pipeline. `docs/skills-design.md` porte le format des référentiels. Ici : le choix, surtout quand il tranche contre une lecture naïve d'une source.

## Dépôt

- Dépôt public `fuzoh/scouts-skills`. Titulaire des licences : `fuzoh`, sans nom civil. La ligne de copyright reste : le MIT l'exige.
- Code MIT. Contenu propre CC BY-SA 4.0. Textes officiels à leurs auteurs.
- Textes officiels = documents publics redistribués. Le dépôt retrouve, cite par `id`, renvoie à l'original. Les manuels J+S d'extranet (« copie interdite ») sont publics ici et vont dans `scouts-ressources`.
- Pas de sigle ni de nom d'association cantonale dans un fichier versionné. « Cantonal » suffit. Une source officielle qui nomme un canton reste intacte.
- Hors git : `sources/*/original/`, `pilote/cas/`, `documents/`. `check` ne recalcule le sha256 que si `original/` est présent.
- `skills-src/` s'écrit. `skills/` est généré et commité. `dist/` = zips de release, sans pré-release.
- Version des packs injectée par `build` depuis `pyproject.toml` (release-please). Avant 1.0, un `feat` bump une mineure.
- Le site se déploie sur un tag `v*` et affiche cette version, sa date et le CHANGELOG. Une correction de site part avec la release suivante (`fix(site)`), ou par lancement manuel du workflow sur le dernier tag. L'environnement `github-pages` accepte `main` et les tags `v*`. La CI construit les packs à chaque push.
- Retours par formulaires d'issue. Veille mensuelle : une issue s'il y a un changement, aucune si tout est ok. Pas de PR de veille.
- Mistral et Copilot : une mention sur le site, sans mode d'emploi. Pack web par défaut : `scouts`. `scouts-ressources` : ChatGPT. Trop lourd pour claude.ai et les compétences Gemini. Destiné aux agents en ligne de commande et aux IDE : aucun contrôle de taille.
- Pas de champ `rights`. Les textes officiels ne sont pas anonymisés. Aucune personne, aucun groupe, aucun lieu ni aucune année de camp réel dans un fichier versionné.
- Hors dépôt public : `docs/terrain/` (sauf `docs/lexique-terrain.md`), `ancien skills/`, `docs/propositions/` (sauf `docs/contraintes-plateformes.md`), `idées.md`, `GOALS.md`, `pilote/retours-en-vrac.md`, `docs/briefing-terrain.md`.

## Skills

- Deux skills, même méthode : `scouts` (principal, sans corpus) et `scouts-ressources` (corpus, citations `id#NN-slug`).
- Verbes : chercher, expliquer, corriger, concevoir. `scouts` ajoute guider. Le livrable commande le routage, pas le public.
- Un skill dédié n'apparaît qu'après échec de l'échelle référentiel → référentiel avec procédure → non-négociables dans `SKILL.md`. Repli : un skill par livrable, référentiels conservés.
- `scouts` : dossiers courts, savoirs par thème. Doit s'installer par zip sur claude.ai, ChatGPT et Gemini : `light check` applique la limite la plus basse de chaque plateforme (100 fichiers dans le pack, Gemini échouant à 150 ; 50 Mo ; 25 Mo par fichier ; pas de .docx/.xlsx ; `description` ≤ 1 024 car., avertissement au-delà des 200 de l'aide claude.ai, accepté à ce jour). Budget de lecture : 5 000 tokens estimés par fichier, sans exception, SKILL.md sous 500 lignes. Dérivé de `referentiels/` : toute modification s'y reporte. Provenance en clair, sans `id#NN-slug` ni page.
- Nombre de fichiers de `scouts` : 85 au plus dans la source, quinze de marge sous le plafond de 100 pour les référentiels à venir et les documents 2027 pas encore publiés. Un savoir couvre un sujet qu'un responsable, un formateur ou un coach demande réellement ; il vise 3 500 tokens pour garder du jeu sous le budget. Au-delà de 85 : fusionner sans perte plutôt qu'ajouter.
- Index des savoirs : `savoirs/README.md` groupé par `theme` (vocabulaire fermé dans `scripts/light.py`), une ligne par savoir, `sert_a` ≤ 160 caractères (l'index est lu à chaque question). C'est la seule porte d'entrée vers les savoirs : `SKILL.md` ne les liste pas un à un.
- Buts et objectifs des cours du modèle de formation 2027 : trois savoirs `formation-cours-{base,continue,cadres}.md`, un par niveau, chargés par `SKILL.md` § 3 pour une UA ou un programme de cours. Par cours : conditions cadres, buts, objectifs numérotés avec le verbe d'origine, niveaux d'approfondissement. Besoins et conseils méthodologiques exclus. Écarté : objectifs en mots-clés sous 1 000 mots, un fichier par cours.
- Le contenu d'abord, au plus une phrase d'hypothèse. Paramètres déduits. Une question seulement si la réponse serait fausse sans elle.
- Une seule valeur, la plus prudente. Dossier de camp : 4 semaines. Les 3 semaines réglementaires ne sortent que sur demande, ou si l'équipe est déjà en dessous.
- Pas de provenance dans la prose, pas de mention du skill. Elle vit dans la colonne « source » d'une revue et dans « Pour aller plus loin » (un à trois titres officiels).
- Avis ≤ 8 lignes, revue ≤ 40 (défaut), détaillé sur demande. Un non-négociable en échec est visible à tous les niveaux.
- Hors corpus, dans l'ordre : prescription datée, recommandation, exemple, `[web]`, « non vérifié ». Une théorie pédagogique absente du corpus se vérifie. Bloc séparé, jamais `id@version`.
- `[non officiel]` n'est jamais un non-négociable. Une nuance du mainteneur dans un critère officiel s'énonce avec lui, sans étiquette.
- Protection, accident, crise : les humains d'abord, l'information ensuite.
- Canevas = modèle vierge ingéré, format reconnu, jamais exigé. La trame du référentiel est la sortie de *concevoir*.
- Un non-négociable ne repose pas sur le cudesch seul, sauf dans `concept-de-securite`.
- `skills-src/scouts/` est `valide`. `referentiels/*.md` restent `relu` : les numéros ne sont pas figés.
- Pack aplati `camp` / `formation` : après un pilote évalué.

## Dates d'application

- Défaut : jeu 2027. Jeu 2026 seulement si le camp ou le cours est explicitement avant le 01.01.2027, ou si l'ancien système est demandé. Le dire en une phrase. Un camp à cheval sur cette date n'est pas traité.
- La référence d'un cours suit la date du cours. Le modèle de formation 2027 est en vigueur le 01.01.2027.
- AC et SC jusqu'au 31.12.2026. Dès le 01.01.2027 : activité J+S, part de sport, formes caractéristiques. « Sans subside » (jour sans J+S) ne s'étend pas à 2027.
- 2026 : 30 min d'AC dans deux parties de journée. Au plus un jour sans J+S, sans subside, dans un camp de plus de 4 jours.
- Âges J+S 5–20 inchangés. Groupes cibles et reconnaissances distincts en 2026, une seule reconnaissance SdC/T en 2027.
- Conduite du camp : « chef de camp » jusqu'au 31.12.2026, « Responsable de camp » dès le 01.01.2027. « Chef de cours » est une ancienne terminologie, sans date de fin inventée.
- Annonce dès trois jours. La clause du règlement et la Sardine disent « plus de trois jours ». Le formulaire et le champ général incluent trois jours.
- Clôture confirmée : cartes sous 3 jours, MiData sous 10 jours, offre sous 30 jours après le dernier camp. Pas de délai chiffré pour la clôture du camp dans la BDNS ni pour les comptes : le calendrier Sardine en ligne tranche, avec le coach.
- Préparation : renvoyer au calendrier Sardine en ligne. Repères : programme général à 7 semaines, annonce du coach à 6 semaines, dossier à 4 semaines.

## Arbitrages de contenu

Ces choix tiennent même s'ils sont plus prudents, ou moins stricts, qu'une source isolée. Deux dates ou deux conditions ne se fondent pas en une règle. Un chiffre non confirmé ne se garde pas.

- Marche : fourchettes avec et sans charge du manuel montagne 2014. Planifier depuis le bas de la fourchette adaptée, puis ajuster au groupe et au terrain. Pauses et marge en plus. `[non officiel]`, pas une vitesse réglementaire.
- Eau : équipement de l'aide-mémoire J+S 10/2025, distinct pour le lac, le lac au-delà de 300 m et les embarcations en rivière. Un gilet à bord ne remplace pas le port prescrit. L'exception CPR/BLS vaut pour la baignade en lac sous maître-nageur. Module SSS par tranche de 12, y compris en rivière.
- Piscine : l'aide-mémoire J+S Sécurité Eau 2024 fait foi. Baignade en piscine surveillée : module J+S Eau SdC/T ou brevet Base Pool ; piscine non surveillée : module J+S Eau ou brevet Plus Pool.
- Jours d'arrivée et de départ : comptent ensemble pour une journée de camp, en 2026 comme en 2027. C'est leur total qui respecte les exigences d'une journée (2027 : 4 h d'activités J+S dont 2 h sportives).
- Délais retenus quand les sources divergent : commande de cartes 5 semaines avant (3, 4 ou 5 selon la source), clôture d'un cours dans le Pilote 3 semaines (30 jours ailleurs). Règles de comportement J+S : 8.
- Trois concepts de sécurité : global, activité à caractère dangereux, randonnée. Toute randonnée en a un, succinct hors domaine de sécurité.
- Constructions : un concept global suffit en règle générale. Une petite construction (lavabo) n'en exige pas. Montage, usage et tempête vont dans ce concept global.
- La matrice des risques est un outil. Un concept global sans matrice est conforme s'il nomme des risques concrets (lieu, saison, groupe), une mesure chacun, et une réaction d'urgence que tout responsable peut appliquer. 3x3 recommandé en randonnée, matrice pour la tyrolienne et l'eau. Corde : personne expérimentée, pas un expert J+S exigé. Gravité : vocabulaire libre, cohérence interne exigée.
- Le concept nomme le seuil « la maîtrise est dépassée » et la Helpline. La consigne médias n'est pas un non-négociable.
- Check-list C de l'autorisation de camp 2026 : non-négociable, y compris les points que le formulaire appelle un pense-bête. Le formulaire 2027 n'est pas ingéré : ne pas l'inventer.
- 2026 : indiquer l'élément J+S visé sur la fiche est une qualité, pas une exigence. 2027 : la forme caractéristique reste exigée.
- Reconnaissance et 3x3 d'une randonnée : exigés.
- « Camp mixte » a trois sens : filles et garçons, ancienne catégorie J+S, règlement. AS est un type d'AA. PF = point fixe. AA = AdA = VC : dans le périmètre, sans critères AC/SC.
- CDF hors périmètre. Le terme générique est AS. Le reste du contenu confessionnel est une option de groupe.
- UA : les objectifs d'apprentissage sont non-négociables. Le déroulement doit permettre de les atteindre. Niveau « Vivre » : vécu seul, objectif formulé comme vécu. Programme détaillé : 2 semaines minimum MSdS. Un document ou la maîtrise peut allonger.
- GAG (Global – Analytique – Global) est une méthode J+S. IFV est abandonné.
- Formation : le modèle 2027 prime sur l'Ancre pour la réduction de 0,5 jour des cours combinés. L'équilibre de genre est recommandé, pas un quota. Les chapitres de l'Ancre priment sur son tableau : hajk 4 semaines avant le cours, prêt J+S 5 semaines avant la livraison. Top : (Responsable de camp ou module de sécurité) et un module supplémentaire. Castors : profil 2025, 4–7 ans. La brochure 5–7 est une divergence à dire, comme pour les Picos.
- Expert de sécurité : la formule Sardine est l'ancienne terminologie, à côté du complément « Experts du domaine » (aide-mémoire 10/2025).
- Quota 36 participants / +1 moniteur par 12 : guide 2023, pas contredit. Le confirmer dans le guide des offres 2027 avant de l'affirmer pour 2027.
- Critères cantonaux : les G et les O entrent dans les référentiels, les R nulle part. Exception : le QR code (RG-17) reste une suggestion `[non officiel]`.
- Canevas cantonaux, picasso, annexes du concept global, K12, PPT : pas ingérés. On en tire une trame cantonale `[non officiel]`. ORA, crise, pharmacie, Helpline, feuille d'urgence : sujets à couvrir, pas documents à exiger.
- Objectifs d'apprentissage : taxonomie du modèle de formation MSdS. La table Bloom explique, elle n'est pas exigée. Si le canevas d'UA ne porte pas les conditions cadres, demander le sommaire avant de les signaler manquantes.
- Qualification : l'intérêt pédagogique d'abord, la décision réussi / non réussi ensuite.
- Dosage du retour : un principe, pas un plafond chiffré. *concevoir* donne la trame complète. La trame cantonale est marquée *.
- Les dossiers réels ne sont ni ingérés ni cités. Le lexique qui en est déduit est `[non officiel]` (`docs/lexique-terrain.md`).

## Sources

Choix non rouverts. Les commandes sont dans `METHODE.md`.

- Français seulement. Une source DE n'entre que sans équivalent FR, marquée `lang: de`.
- Un id stable par document. Les versions vivent dans `history`. Sources à plat, tri par métadonnées.
- `raw.md` est produit par script. `index.md` pilote le découpage. Citation PDF : `p.N` physique. Web : url et ancre, ou titre si l'ancre est une route.
- `redactions` s'applique au texte brut et aux sections. E-mails personnels caviardés. Adresses institutionnelles conservées. Le build n'embarque ni `raw.md` ni les originaux.
- Une page PDF qui perd le texte sous les graphismes est reprise sans graphismes. Le découpage s'arrondit à la page.
- Index : signets du PDF s'il en a. Sinon PageIndex Flash (`index --pageindex`, venv séparé, pas une dépendance du projet).
- Pas de crawler qui crée des sources. Rendu web en `fr-CH`. Manifeste cudeschin écrit à la main. Catalogue pfadi paginé : script dédié, pas une commande `just`.
- `msds` couvre les brochures MSdS, y compris l'Ancre, le Pilote, le Ticket, la commande hajk et le mémento Étincelle. `cofor` = documents numérotés `30xxxx`–`31xxxx`.
- `extraction: vision` après lecture du texte. Pas d'OCR. Un catalogue n'a qu'un `index.md`. liberatingstructures : titres du sitemap, sans téléchargement.
- `liens-utiles.pdf` et orgcheck baspo : pas ingérés.
- Glossaire court pour tous les skills. Fiches de concepts à la demande.
- `SKILL.md` (agentskills.io) est le format maître. Les packs sont générés.
- Scripts pour l'extraction, agent pour le sens. `applies_*` et `nature` sur les sources prescriptives seulement. `verified` = relecture des tableaux, cases et prescriptions.

## Plus tard

- Marketplace de plugins Claude Code.
- Sources web à la place des PDF, cudesch numérique inclus.
- Fiches `tool.jeunesseetsport.ch`.
- OCR.
- Pack aplati pour Claude Project et custom GPT, après un pilote évalué.

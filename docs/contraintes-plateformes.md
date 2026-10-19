# Contraintes des plateformes pour distribuer un skill SKILL.md

Recherche du 2026-10-17 (date de consultation de toutes les URLs ci-dessous). Format maître : SKILL.md selon agentskills.io.
Légende : [P] source primaire (doc éditeur), [T] tierce (blog, forum), [NV] non vérifié.

## Tableau comparatif

| Plateforme | Skills natifs ? | Instructions max | Fichiers (nombre / taille / formats) | Retrieval | Invocation entre skills | Notes |
|---|---|---|---|---|---|---|
| agentskills.io (spec) | Définit le format | description 1024 car. ; corps < 500 lignes / < 5000 tokens (recommandé) | `scripts/`, `references/`, `assets/`, libre ; pas de limite | Aucun : lecture à la demande | Aucun mécanisme dans la spec | `name` = nom du dossier |
| Claude.ai (web/app) | Oui, zip uploadé (Customize > Skills) | description 1024 car. | zip : taille max non chiffrée [NV] | Fichiers lus dans un bac à sable | Non documenté | Code execution requis ; individuel ; pas de sync API |
| Claude Project | Non (connaissances) | ~8000 car. [T, NV] | illimité en nombre ; 30 Mo/fichier ; PDF, DOCX, CSV, TXT, HTML, ODT, RTF, EPUB, JSON, XLSX | RAG auto à l'approche de la fenêtre, capacité x10 max (payant) | Sans objet | Total borné par la fenêtre de contexte hors RAG |
| Claude Code | Oui, dossiers | description + when_to_use tronqués à 1536 car. | libre | Lecture fichiers | Pas de doc ; `context: fork`, `skills:` des sous-agents, empilement | `~/.claude/skills`, `.claude/skills`, plugins |
| ChatGPT custom GPT | Non (aucune preuve) | 8000 car. [T] | 20 fichiers, 512 Mo, 2 M tokens/fichier texte [T] | RAG [NV détail] | Sans objet | help.openai.com inaccessible (403) |
| ChatGPT skills / Codex | Oui (appli desktop ; web/mobile via plugins) | liste des skills : 2 % du contexte ou 8000 car. | libre ; pas de limite documentée | Lecture fichiers | `@skill` (utilisateur) ; non documenté entre skills | `.agents/skills` ; `agents/openai.yaml` optionnel |
| Gemini Gems | Remplacés par des skills dès nov. 2026 (comptes perso) | non trouvé [NV] | 10 fichiers, 100 Mo [T] | non trouvé [NV] | Sans objet | Migration automatique Gem vers skill |
| Gemini app (skills) | Oui, SKILL.md / zip / dossier | non chiffré | 100 skills actifs max ; taille non chiffrée | Lecture fichiers [NV] | Non documenté | Upload : web et Mac seulement |
| Cursor / Copilot / OpenCode / Gemini CLI | Oui, dossiers | description 1024 (OpenCode) | libre | Lecture fichiers | OpenCode : outil `skill` ; Gemini CLI : `activate_skill` | Tous lisent `.agents/skills/` |

## 1. Spécification agentskills.io

- Structure : dossier avec `SKILL.md` obligatoire ; `scripts/`, `references/`, `assets/` optionnels, "any additional files" admis. https://agentskills.io/specification
- Frontmatter : `name` (obligatoire, 1-64 car., minuscules/chiffres/tirets, ni début/fin en tiret, pas de `--`, identique au dossier) ; `description` (obligatoire, 1-1024 car.) ; `license`, `compatibility` (max 500), `metadata` (map chaîne vers chaîne), `allowed-tools` (expérimental, séparé par espaces). Idem source.
- Corps : "no format restrictions". Recommandé : SKILL.md sous 500 lignes et sous 5000 tokens ; métadonnées ~100 tokens, chargées au démarrage pour tous les skills. Idem source.
- Références : chemins relatifs à la racine du skill, un seul niveau de profondeur depuis SKILL.md. Idem source. Dire à l'agent quand charger chaque fichier (https://agentskills.io/skill-creation/best-practices).
- Skill appelant un autre skill : aucun mécanisme dans la spec ni dans les guides. La seule mention est l'idée d'unités cohérentes "qui se composent bien" (best-practices) et un motif optionnel de délégation à un sous-agent (https://agentskills.io/client-implementation/adding-skills-support). Pratique déduite (non documentée) : nommer l'autre skill par son `name` dans le texte.
- Convention de découverte `.agents/skills/` (projet et utilisateur), non imposée par la spec. Idem client-implementation.
- Liste de clients : https://agentskills.io/home (page d'accueil, consultée le 2026-10-17).

## 2. Claude.ai et Claude Project

- Skills natifs : oui. Disponibles Free, Pro, Max, Team, Enterprise ; code execution obligatoire. Upload : Customize > Skills > "+" > Create skill > Upload a skill, zip du dossier. https://support.claude.com/en/articles/12512180-using-skills-in-claude [P]. La doc plateforme dit Pro/Max/Team/Enterprise et "Settings > Features" : incohérence entre pages. https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview [P]
- Zip : le dossier doit être la racine de l'archive (`mon-skill/SKILL.md`), sinon non reconnu. https://claude.com/docs/skills/how-to [P]. Taille max : aucun chiffre officiel ; l'aide cite seulement l'erreur "ZIP file exceeds size limits". Un tiers parle de 50 Mo [T, NV].
- Contraintes `name` : sans "anthropic" ni "claude", sans balises XML ; `description` 1024 car. sans balises XML (overview, best-practices) [P]. Corps sous 500 lignes.
- Portée : individuelle ; partage Team/Enterprise en lecture seule. Pas de synchro avec l'API ; Claude Code télécharge les skills du compte claude.ai dans `~/.claude/skills/synced/` (jamais d'upload). https://code.claude.com/docs/en/skills [P]
- Exécution : tout le dossier est copié dans le bac à sable, donc `references/` fonctionne ; réseau variable selon les réglages.
- Project (connaissances) : 30 Mo par fichier, nombre illimité mais total dans la fenêtre de contexte ; PDF, DOCX, CSV, TXT, HTML, ODT, RTF, EPUB, JSON, XLSX. https://support.claude.com/en/articles/8241126-what-kinds-of-documents-can-i-upload-to-claude-ai [P]. Envois en conversation : 500 Mo, 20 fichiers par chat (même source).
- RAG : s'active automatiquement quand les connaissances approchent la fenêtre, capacité "up to 10x", plans payants. https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects [P]. Seuil exact : [NV] (un ticket GitHub parle de ~13 fichiers, non confirmé).
- Instructions de projet : limite de longueur non trouvée en source primaire ; ~8000 car. cités par des blogs [T, NV].
- Un skill dans un Project : non vérifié [NV].

## 3. Claude Code

- Emplacements : `~/.claude/skills/<nom>/SKILL.md` (perso), `.claude/skills/` (projet), `<sousdossier>/.claude/skills/`, `--add-dir`, plugin `<plugin>/skills/` (namespace `/plugin:skill`), entreprise (managed settings). Priorité entreprise > perso > projet. https://code.claude.com/docs/en/skills [P]
- Frontmatter : tout optionnel, champs inconnus ignorés ; ajoute `when_to_use`, `disable-model-invocation`, `user-invocable`, `paths`, `context`, `agent`, `model`, `allowed-tools`, etc.
- Limites : description + `when_to_use` tronqués à 1536 car. dans la liste ; budget de liste = 1 % de la fenêtre ; après compaction chaque skill garde ses 5000 premiers tokens, budget commun 25 000 ; SKILL.md sous 500 lignes. Même source.
- `context: fork` : le contenu devient le prompt d'un sous-agent (type via `agent`), sans l'historique ; exécution en arrière-plan par défaut (`background: false` pour attendre). Même source.
- Skill vers skill : non documenté. Existent : outil `Skill` (permissions `Skill(nom)`), empilement `/a /b` (premier + 5), champ `skills:` d'un sous-agent (jusqu'à 32 skills injectés intégralement). https://code.claude.com/docs/en/sub-agents [P]. `disable-model-invocation: true` empêche le préchargement.

## 4. ChatGPT

- Custom GPT, instructions : 8000 caractères, éditeur refuse au-delà ; seulement des fils de forum, pas d'énoncé OpenAI. https://community.openai.com/t/how-can-i-increase-the-ceiling-for-gpt-instructions-beyond-8000-characters/801867 [T]
- Custom GPT, fichiers : 20 fichiers, 512 Mo, 2 M tokens par fichier texte (hors tableurs), 10 Go par utilisateur / 100 Go par organisation, d'après des citations de l'aide OpenAI sur https://community.openai.com/t/what-is-the-knowledge-file-limit-that-can-be-uploaded-to-train-custom-gpts/653244 [T]. help.openai.com renvoie 403 ; non revérifié en primaire. Formats et mécanisme de retrieval : [NV].
- Skills ChatGPT / Codex : "Standalone skills are available in the ChatGPT desktop app, Codex CLI, and IDE extension" ; skills dans des plugins disponibles sur web, desktop, mobile. https://learn.chatgpt.com/docs/build-skills (ex developers.openai.com/codex/skills) [P]
- Chemins Codex : `.agents/skills` du CWD à la racine du dépôt, `$HOME/.agents/skills`, `/etc/codex/skills`. SKILL.md avec `name` et `description` ; `agents/openai.yaml` optionnel (métadonnées d'interface, `allow_implicit_invocation`, dépendances d'outils MCP). Liste initiale limitée à 2 % du contexte ou 8000 car. (`skills.max_context_tokens` jusqu'à 10 000). Invocation : `@` dans ChatGPT, `$` ou `/skills` dans Codex. Même source.
- Upload dans ChatGPT via Plugins > Skills > Create > Upload from your computer ; éligibilité (Business, Enterprise, Healthcare, Edu ; pas Free/Plus/Pro) et scan "Needs Review" : seulement relayés par des tiers [T, NV]. https://help.openai.com/en/articles/20001066-skills-in-chatgpt (403).
- Un custom GPT ne charge pas de skills : aucune source trouvée [NV].

## 5. Gemini

- Annonce : "Starting in November 2026, Gems will go away on personal Google accounts and automatically transition to skills." https://support.google.com/gemini/answer/15146780 [P]. Dates : perso nov. 2026, Workspace business/enterprise/ONG mars 2027, éducation juin 2027. https://support.google.com/gemini/answer/18560919 [P]
- Skills de l'app Gemini : création sous Settings > Skills ; téléchargement en zip contenant SKILL.md ; pour ajouter des fichiers, dossier portant le nom du skill puis "Replace skill" ; noms en minuscules-tirets ; import de SKILL.md d'autres plateformes ; création illimitée, 100 actifs max ; upload de fichiers seulement sur web et app Mac ; fichiers GitHub non pris en charge ; partage et Drive "dans les semaines à venir". Taille max non indiquée. Même source.
- Gems : instructions max et nombre de fichiers de connaissances : aucune source primaire ; un tiers cite 10 fichiers et 100 Mo [T, NV]. Limites générales Gemini Apps : 10 fichiers par prompt, 100 Mo par fichier (vidéo 2 Go), zip 10 fichiers. https://support.google.com/gemini/answer/14903178 [P]
- Gemini Enterprise : zip avec SKILL.md à la racine, `scripts/` Python et Bash seulement ; aucun chiffre. https://docs.cloud.google.com/gemini/enterprise/docs/skills [P]
- Gemini CLI : `~/.gemini/skills`, `~/.agents/skills`, `.gemini/skills`, `.agents/skills` ; outil `activate_skill` avec confirmation ; la page indique un remplacement par Antigravity CLI le 2026-06-18. https://geminicli.com/docs/cli/skills/ [P]

## 6. Autres agents lisant SKILL.md

- Cursor : `.agents/skills`, `.cursor/skills`, et compat `.claude/skills`, `.codex/skills` ; champs `paths`, `disable-model-invocation`. https://cursor.com/docs/context/skills [P]
- GitHub Copilot (cloud agent, CLI, VS Code, JetBrains) : `.github/skills`, `.claude/skills`, `.agents/skills`, `~/.copilot/skills`. https://docs.github.com/en/copilot/concepts/agents/about-agent-skills [P]
- OpenCode : `.opencode/skills`, `.claude/skills`, `.agents/skills` ; outil `skill({name})` ; réglages propres sous `metadata`. https://opencode.ai/docs/skills/ [P]
- Autres listés sur agentskills.io/home : Junie, Amp, Goose, Letta, Factory, Kiro, Roo Code, Trae, OpenHands, Mistral Vibe, Tabnine, Qodo, pi, Snowflake Cortex Code, Databricks Genie Code, Spring AI, etc. [P]

## Conséquences pour un `build` qui génère un pack par plateforme depuis SKILL.md

1. Frontmatter minimal commun : `name` (= dossier, 64 car., sans "claude"/"anthropic") et `description` (< 1024 car., sans balises XML, 3e personne, mots-clés d'activation en tête).
2. Claude.ai, Gemini, ChatGPT (skills) : générer un zip avec le dossier du skill comme racine ; vérifier le nom du dossier ; mesurer la taille (aucun plafond officiel connu, viser quelques Mo).
3. Claude Code, Cursor, Copilot, OpenCode, Codex : copier le dossier, une fois dans `.agents/skills/` (convention commune) ; ne pas utiliser les champs propres à Claude Code dans le maître, les isoler dans `metadata`.
4. Références inter-skills : ne pas compter sur un appel natif ; aplatir en citant l'autre skill par `name` avec un repli textuel ("si indisponible, lire references/..."), ou embarquer le contenu nécessaire dans le pack.
5. Garder `references/` à un niveau de profondeur, chaque fichier avec table des matières s'il dépasse 100 lignes, chemins relatifs avec `/`.
6. Claude Project et custom GPT n'ont pas de skills : aplatir en un fichier d'instructions court (< 8000 car. par prudence) plus des fichiers de connaissances issus de `references/`, à nommer explicitement dans les instructions.
7. Pour ces packs de connaissances : découper en fichiers ciblés (TXT/MD/PDF), compter 20 fichiers maximum pour ChatGPT, 10 pour Gems (si l'ancien format persiste), et mettre l'index des fichiers dans les instructions car le RAG ne garantit pas la recherche exhaustive.
8. Gemini : viser le format skill (zip) et non un pack Gem, vu la bascule de nov. 2026 pour les comptes perso et mars/juin 2027 pour Workspace.
9. Respecter le budget de liste : descriptions courtes (Claude Code 1536 car. cumulés avec `when_to_use`, Codex 2 % du contexte), SKILL.md sous 500 lignes, mettre l'essentiel en tête (compaction à 5000 tokens).
10. Interdire dans les `scripts/` tout besoin réseau ou installation de paquets (API sans réseau, Gemini Enterprise Python/Bash seulement) ; les skills du dépôt référencent les sources par `id`, donc le build doit résoudre ces `id` en chemins de `references/` dans chaque pack.

## Non vérifié

Taille max du zip Claude.ai ; limite de longueur des instructions de projet Claude ; limites officielles des custom GPT (help.openai.com bloqué) ; plans ChatGPT éligibles aux skills ; limites d'instructions et de fichiers des Gems ; usage de skills dans un Project Claude ; retrieval exact des GPT.

# Fabrique de skills scoutisme suisse. `just` liste les recettes.

set positional-arguments

default:
    @just --list

# Ingérer un fichier : just ingest documents/x.pdf --id cofor-x
ingest *args:
    uv run ingest "$@"

# Manifeste d'un site : just discover https://pfadi.swiss --depth 2
discover *args:
    uv run discover "$@"

# sources/<id>/raw.md
convert *args:
    uv run convert "$@"

# squelette sources/<id>/index.md
index *args:
    uv run index "$@"

# caviardage du yaml (redactions) appliqué au texte brut : just redact <id> | --all
redact *args:
    uv run redact "$@"

# raw.md -> NN-slug.md selon index.md
split *args:
    uv run split "$@"

# grilles perdues à la conversion -> sources/<id>/recovered/*.md (icônes, texte sans filets)
recover *args:
    uv run recover "$@"

# valider les yaml et écrire INVENTORY.md
inventory *args:
    uv run inventory "$@"

# validation seule, sans écrire INVENTORY.md
check:
    uv run inventory --check
    uv run light check

# valider les référentiels (liens vers les sources, N cités, tailles) : just referentiels --citing <id>
referentiels *args:
    uv run referentiels "$@"

# packs de distribution : just build claude-code [--skill scouts|scouts-ressources] [--scope referentiels] [--zip]
build *args:
    uv run build "$@"

# skills/ (packs commités, comparés par la CI) et dist/*.zip (assets de release) depuis skills-src/
skills:
    uv run light index
    uv run build all --zip

# ancien nom de `just skills`
zips: skills

# build scouts puis lien ~/.claude/skills/scouts -> skills/scouts
install:
    uv run light index
    uv run build claude-code --skill scouts
    uv run build install --skill scouts

# build scouts-ressources (corpus) puis lien ~/.claude/skills/scouts-ressources
install-ressources:
    uv run build claude-code --skill scouts-ressources
    uv run build install --skill scouts-ressources

# veille : compare le registre aux URL publiées (changées, mortes, redirigées) : just check-urls [--only <id>] [--limit N] [--out veille.md]
check-urls *args:
    uv run check-urls "$@"

# limites de scouts (applis web : 200 fichiers, 50 Mo, pas de .docx ; 5 000 tokens par fichier ; pas de citation) : just light-check --table
light-check *args:
    uv run light check "$@"

test *args:
    uv run pytest "$@"

# site statique (GitHub Pages) dans build/site depuis site/*.md et le registre
site *args:
    uv run site --out build/site "$@"

# PageIndex Flash pour `index --pageindex` : venv dédié, sans ses dépendances LLM (18 Mo)
install-pageindex:
    uv venv .venv-pageindex
    uv pip install --python .venv-pageindex/bin/python --no-deps pageindex==0.4.1
    uv pip install --python .venv-pageindex/bin/python PyPDF2 python-dotenv pypdfium2 regex sortedcontainers pyyaml

# navigateur pour discover --render (extra web)
install-web:
    uv sync --extra web
    uv run playwright install chromium

# docs/concepts/<slug>.md depuis les concepts: des yaml
concepts *args:
    uv run concepts "$@"

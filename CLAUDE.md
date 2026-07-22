# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in
this repository. This is the **base template** — a derived app should keep this file's
skeleton and fill in domain-specific facts (domain list, level defaults, branding).

## Commands

```bash
# Frontend dev (read-only, no book generation)
npm run dev          # http://localhost:5174/<base>/

# Full stack (book generation requires spl123 conda env)
conda activate spl123
pip install -r requirements-api.txt
bash scripts/start-api.sh          # uvicorn, separate terminal
npm run dev                         # Vite proxies /api → the backend

# Sync domain content from SPL.py after regenerating graphs
bash scripts/sync_from_spl.sh

# Deploy to GitHub Pages
npm run deploy       # builds dist/ and pushes to gh-pages branch
```

## Architecture

**Content pipeline:** graphs are authored (or generated) as `input/graph.yaml` per
domain, then `scripts/concept_graph.py` renders `output/graph.html` (a vis.js
navigator) locally. Concept book HTML is generated on demand by the backend, which
shells out to an SPL.py `spl3 run` pipeline.

**Domain directory layout:**
```
public/domains/{id}/
  input/graph.yaml                        # concept graph definition
  output/graph.html                       # vis.js navigator (level/lang invariant)
  output/{level}.{lang}/{model}/html/     # e.g. core.en/gemma4/html/
    book_{target}.html                    # TOC-index concept books
    concept_{name}.html                   # individual concept component books
```

`graph.yaml` node fields used by the frontend: `id`, `label`, `kind` (`primitive` nodes
are excluded from the Generate dropdown), `tier`, `composed_of` (edges to prerequisite
nodes).

**Content levels** (learner progression, not tied to any specific school system):
`intro` (basic) → `core` (expanded) → `college` (extensive) → `research` (advanced). A
domain can have books at multiple levels — level is a content property, not a domain
property.

**Frontend** (`src/`): Vite + Vanilla JS with zero frameworks.
- `router.js` — hash-based router (`#/`, `#/domain/:id`, plus any `path?query` route).
- `config.js` — branding overrides (`appConfig.logoImage`, etc.) for derived apps.
- `data/catalog.js` — fetches/caches `public/domains/catalog.json`, the domain
  registry (source of truth for the domain list).
- `lib/paths.js` — the `output/{level}.{lang}/{model}/html/{kind}_{name}.html` path
  schema in one place; build/parse variant paths only through this module.
- `lib/contentExists.js` — shared "does this generated page exist?" check (sniffs
  generated-page markers since dev servers 200 the SPA shell for unknown paths).
- `pages/Domain.js` — splits the view into `GraphViewer` (left, iframe) and
  `ConceptPanel` (right, node detail).
- `components/GraphViewer.js` — the key integration point. Loads `graph.html` in an
  iframe, then uses `contentWindow.eval()` to expose `RAW`/`nodeIndex`, patches
  `handleSelect` to emit `cb:nodeSelected` custom events, and injects sidebar sections
  into the iframe DOM via `insertAdjacentElement`. Same-origin, not cross-origin — both
  `graph.html` and the shell are served from the same Vite dev server.

**Backend** (`api/`): FastAPI.
- `GET /api/generate` (SSE) — params: `domain`, `target`, `level`, `language`. Streams
  `spl3 run` subprocess output as `log`/`done`/`gen_error` events.
- `GET /api/domains` / `/api/domains/{id}/status` — reads `catalog.json`.
- `api/config.py` — `Settings` reads env vars prefixed `CB_`.
- `api/services/catalog_lock.py` — the single write-path for `catalog.json`
  (`read_catalog`/`update_catalog`). Every writer must go through `update_catalog()` —
  it serializes concurrent writers with an fcntl lock and publishes atomically, so a
  generation task and a batch script running at the same time can't silently drop each
  other's updates.

**Deployment:** GitHub Pages (static). The backend is a local-only tool; generated
book/concept HTML files are committed into `public/domains/` and included in the
`dist/` build.

## Iframe ↔ parent event protocol

`GraphViewer.js` bridges the iframe (`graph.html`) and the parent app via custom events
on `window`:
- `cb:graphLoaded` — dispatched after iframe loads. `detail.concepts` is an array of
  `{id, label, kind, tier}`.
- `cb:nodeSelected` — dispatched when a user clicks a node. `detail.nodeId` and
  `detail.node` (full node object from `nodeIndex`).

## Key data shapes

`catalog.json` entry:
```json
{
  "id": "domain-id",
  "name": "Human-Readable Domain Name",
  "capstone": "some_concept_id",
  "default_level": "core",
  "has_navigator": true,
  "has_book": true,
  "books": [{"target": "some_concept", "file": "output/core.en/html/book_some_concept.html"}],
  "generated_concepts": [{"name": "some_concept", "label": "Some Concept", "file": "output/core.en/html/concept_some_concept.html"}],
  "tags": ["math"],
  "source": {"title": "...", "authors": "...", "license": "...", "url": "...", "attribution": "..."}
}
```

`books` = full concept books (TOC index). `generated_concepts` = individual concept
component books. `source` is optional — when present, it renders as an attribution
line on the domain page (see `src/pages/Domain.js`); use it when a domain is derived
from a specific external text (textbook, paper, corpus).

## Vite base path

`vite.config.js` sets `base`. All asset and domain URLs must use
`import.meta.env.BASE_URL` as prefix (see `GraphViewer.js` iframe `src`).

## Adding a new domain

1. Add the domain ID and its default level to the `LEVEL_MAP` in
   `scripts/sync_from_spl.sh`.
2. Add an entry to `public/domains/catalog.json`.
3. Run `bash scripts/sync_from_spl.sh` to copy files into `input/` and generate
   `output/graph.html`.

## i18n

`src/i18n.js` provides a `t(key)` translation function. Translation keys are defined
inline in `i18n.js`, not in external JSON files.

## Extension points

The base intentionally ships a minimal feature set. These are known, deliberate
extension points for a derived app rather than gaps to "fix" in the base — treat them
as things to build in your fork, not to upstream unless a second app needs the same
thing:

- **Branding** — `src/config.js` (`appConfig.logoImage`) and `src/i18n.js`'s
  `app.title` key. Header.js reads both; no other file should need editing to rebrand.
- **Auth / multi-user hosting** — `main.js` registers routes unguarded. An app that
  needs login-gated routes should wrap `register()` calls in its own guard rather than
  modifying `router.js`.
- **Book page layout** — `pages/BookPage.js` is currently a single file. A derived app
  with heavier book-reading needs (compare view, chat sidebar, TOC/nav split) should
  factor it into `components/book/*.js` submodules rather than growing the one file
  indefinitely.
- **Search** — `data/catalog.js`'s domain/concept search is plain substring matching.
  A domain with non-Latin-script or phonetic search needs (e.g. pinyin) should layer a
  matcher on top rather than special-casing catalog.js.
- **Settings page** — ships a single flat form (SPL adapter/model, execution limits).
  Multi-tab layouts or per-user API-key management belong in the fork, not the base.

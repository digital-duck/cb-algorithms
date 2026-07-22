# concept-book-base

Template repo for concept-book apps — a web portal for exploring a knowledge domain
through an interactive concept graph, powered by the [SPL.py](https://github.com/digital-duck/SPL.py)
content engine.

This is not meant to be deployed on its own. Fork it, add your domain content under
`public/domains/`, and customize `src/config.js`, `CLAUDE.md`, and branding as needed.
See `CLAUDE.md` for the architecture and the extension points a derived app can hook
into without forking core files.

---

## Quick start

### 1. Frontend only (read-only — no book generation)

```bash
npm install
npm run dev
```

### 2. Full stack (frontend + book generation)

**Terminal 1 — backend** (requires the `spl123` conda env from SPL.py):

```bash
conda activate spl123
pip install -r requirements-api.txt
bash scripts/start-api.sh
```

**Terminal 2 — frontend:**

```bash
npm install
npm run dev
```

Vite proxies `/api` to the backend automatically in dev mode (see `vite.config.js`).

---

## Adding a new domain

1. Add the domain's directory under `public/domains/{id}/` with `input/graph.yaml`
   (see the graph schema in `CLAUDE.md`).
2. Add the domain's default level to `LEVEL_MAP` in `scripts/sync_from_spl.sh`.
3. Add an entry to `public/domains/catalog.json`.
4. Run `bash scripts/sync_from_spl.sh` to generate `output/graph.html` and pull any
   graph updates from SPL.py.

---

## Deployment (GitHub Pages)

```bash
npm run deploy      # vite build && gh-pages -d dist --no-history --dotfiles
```

The backend API is a local tool and is not deployed; static graph navigators and any
pre-generated concept books are baked into the build.

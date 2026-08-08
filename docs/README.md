# docs/ — GitHub Pages site

Public site: https://anshul9t6.github.io/DeployerX/

## Auto progress

| File | Edit? |
|------|-------|
| `data/progress.json` | **No** — run `python3 scripts/generate_site_data.py` |
| `index.html` / `styles.css` / `app.js` | Yes — UX only |

CI: `.github/workflows/sync-site-data.yml` refreshes progress.json on `main` when coverage sources change.

Agents must follow `AGENTS.md`.

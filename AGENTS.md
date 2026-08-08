# Agent instructions — DeployerX

You are working on **DeployerX**: forward-deployed AI for the rest of the world — decisioning + playbooks + locale packs to e/acc.

## Non-negotiables

1. **Hierarchy:** `_global` → country (L1) → `l2/` → `l3/` (see `schema/hierarchy.md`).
2. **Common ships once.** Do not fork playbooks per city. L3 packs are **deltas only**.
3. **India first**, world-shaped. Same folder contract for every country.
4. **₹0 Path A first** — no paid WhatsApp API / hosting required for playbooks.

## After changing coverage sources — ALWAYS refresh the site

If you add/edit any of:

- `locale-packs/**`
- `playbooks/**`
- `field-notes/**`
- `locale-packs/_registry.yaml`

Then run:

```bash
python3 scripts/generate_site_data.py
python3 scripts/validate.py
```

Commit **`docs/data/progress.json`** with the content change (or rely on `.github/workflows/sync-site-data.yml` on `main`).

The GitHub Pages UI reads `docs/data/progress.json` via `docs/app.js`. Stale JSON = lying stats.

## Site files

| Path | Role |
|------|------|
| `docs/index.html` | Structure / sections |
| `docs/styles.css` | Visual design |
| `docs/app.js` | Renders live progress |
| `docs/data/progress.json` | **Generated** — do not hand-edit |
| `scripts/generate_site_data.py` | Generator |

Hand-edit HTML/CSS/JS for UX. **Never** hand-edit progress numbers in HTML.

## When improving the website

- Keep it static (GitHub Pages, $0).
- Stats/lists must come from `progress.json`.
- Preserve explore: countries, L3 filter, L2 strip, playbooks.
- Update `docs/maintain.html` if the regenerate workflow changes.

## High-value work (prefer over UI polish)

1. Real Path A field note via `field-notes/FIRST_DEPLOYMENT.md`
2. Home-district L3 pack (deltas only)
3. Expand glossaries / open countries with maintainers
4. Refresh `docs/data/progress.json` after any of the above

Share copy: `SHARE.md` (add metrics only after a real field note).

## Validation before finishing

```bash
python3 scripts/validate.py
python3 scripts/coverage.py
```

# Brazil locale pack (L1) — draft scaffold

**Admin labels:** L2 = estado · L3 = município

Cascade: `_global` → `br` → `l2/<estado>` → `l3/<municipio>`

## Status

- L2 index: **complete** (26 estados + DF)
- Glossary: [`glossary/pt.yaml`](glossary/pt.yaml) seeded
- L3 municípios: help wanted

## Help wanted

1. Seed first L3 packs (e.g. `sao-paulo/l3/sao-paulo`, `rio-de-janeiro/l3/rio-de-janeiro`)
2. Upgrade key L2 metas from `listed` → `seeded` with regional notes
3. Register maintainers in `_meta.yaml`

India remains the reference implementation: copy patterns from `locale-packs/in/`, not content.

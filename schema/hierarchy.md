# Locale hierarchy & cascade

DeployerX covers the world with a fixed three-level admin tree under each country:

| Level | Code | Meaning | Examples |
|-------|------|---------|----------|
| L0 | `_global` | Ship once for everyone | Safety defaults, contribution rules, base AI glossary |
| L1 | ISO country | Country pack | `in`, `br`, `ng`, `us` |
| L2 | admin level-2 | State / province / governorate | `uttar-pradesh`, `sao-paulo`, `california` |
| L3 | admin level-3 | District / county / LGA | `varanasi`, `campinas`, `santa-clara` |

Country packs declare **local names** for L2/L3 (India: state/district; Brazil: estado/município) without changing the folder shape.

## Folder contract (every country)

```
locale-packs/
  _global/                      # L0 — common
  _registry.yaml                # world index
  <cc>/                         # L1
    _meta.yaml                  # required
    constraints.md              # country defaults
    glossary/                   # language files
    l2/
      _index.yaml               # full L2 list (goal)
      <l2-slug>/
        _meta.yaml
        constraints.md          # optional overrides
        l3/
          <l3-slug>/
            README.md
            constraints.md
            examples.md
```

## Cascade (local wins)

When resolving guidance for `in / uttar-pradesh / varanasi`:

```
_global  →  in  →  in/l2/uttar-pradesh  →  .../l3/varanasi
```

Rules:

1. **Common ships once** at the highest true level (prefer `_global` or L1).
2. **L2/L3 only store deltas** — language nuance, payments quirks, trust, seasons, examples.
3. Missing optional files are OK; resolver falls back upward.
4. Playbooks live in `/playbooks` (global). Locales may add overlays under `overlays/<playbook-id>/` later; do not fork entire playbooks per district.

## What belongs where

| Content | L0 | L1 | L2 | L3 |
|---------|----|----|----|----|
| Universal AI safety (“never invent prices”) | ✅ | | | |
| Base jargon concepts (EN) | ✅ | | | |
| Country payments / channels / legal | | ✅ | | |
| Language glossaries | | ✅ | rare | rare |
| Official/regional languages for a state | | | ✅ | |
| Hyperlocal examples, festivals, trust | | | | ✅ |
| Full playbook recipes | `/playbooks` only | | | |

## IDs

- Country: ISO 3166-1 alpha-2 lowercase (`in`)
- L2/L3: lowercase kebab-case slugs
- Stable path id: `cc/l2-slug/l3-slug` → `in/uttar-pradesh/varanasi`

## Status values

`listed` → `seeded` → `verified` (see `_meta.yaml` fields)

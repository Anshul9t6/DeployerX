# Locale hierarchy

DeployerX uses one folder contract worldwide:

| Level | Path | Role |
|-------|------|------|
| L0 | `locale-packs/_global/` | Shared safety + base glossary |
| L1 | `locale-packs/<cc>/` | Country defaults (ISO 3166-1 alpha-2) |
| L2 | `.../l2/<slug>/` | State / province / equivalent |
| L3 | `.../l2/<slug>/l3/<slug>/` | District / county / equivalent |

Country `_meta.yaml` sets local labels (`state`/`district`, `estado`/`municipio`, …) without changing folder names.

## Cascade

For `in/uttar-pradesh/varanasi`:

```
_global → in → in/l2/uttar-pradesh → …/l3/varanasi
```

Later layers override earlier ones. Missing L2/L3 is allowed; resolver falls back upward (`decision/resolve.py`).

## Placement rules

| Content | Where |
|---------|--------|
| Playbook recipes | `/playbooks` only |
| Universal safety | L0 |
| Payments, channels, legal | L1 |
| Regional language notes | L2 |
| Hyperlocal examples / trust | L3 |

**L3 never forks a playbook.** It stores deltas only.

## Stability

- Folder shape is identical for every country (`l2` / `l3` are universal; labels in `_meta.yaml` are local).
- Playbook IDs are global and stable.
- Locale IDs: `cc`, `cc/l2`, or `cc/l2/l3`.
- Missing L2/L3 is allowed; resolver falls back upward.
- `merged_constraints(ref)` concatenates constraint files root→leaf (append semantics).

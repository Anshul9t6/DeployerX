# Architecture — ship common once, localize deltas

## Problem

Covering every country → L2 → L3 cannot be done by one author. The system must let thousands of contributors add **local truth** without forking the product.

## Split

```
GLOBAL (ship once)              LOCAL (PR per place)
─────────────────────           ─────────────────────
playbooks/*                     locale-packs/<cc>/
decision/*                      locale-packs/<cc>/l2/<l2>/
locale-packs/_global/           locale-packs/<cc>/l2/<l2>/l3/<l3>/
schema/*                        glossaries, examples, trust notes
```

## Resolve algorithm

For locale `cc/l2/l3`:

1. Load L0 `_global`
2. Load L1 `locale-packs/cc`
3. Load L2 `.../l2/l2`
4. Load L3 `.../l3/l3`
5. Merge constraints **root → leaf** (later overrides earlier)
6. Select **one global playbook**; attach locale context

Implemented in `decision/resolve.py`.

## Stability guarantees

- Folder shape is identical for every country (`l2` / `l3` names are universal; labels in `_meta.yaml` are local).
- Playbook IDs are global and stable.
- Locale IDs are `cc`, `cc/l2`, or `cc/l2/l3`.
- Missing L2/L3 is allowed — resolver falls back upward.

## What “done for Earth” means

Not 200 country forks of ChatGPT wrappers. It means:

- Global playbooks for the top operator jobs
- Cascading locale packs until L3 coverage is dense
- Field notes that prove deployments outside English-default markets

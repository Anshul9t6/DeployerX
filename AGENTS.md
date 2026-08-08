# Agent rules — DeployerX

## Contract

- Hierarchy: `_global` → L1 → L2 → L3 (`schema/hierarchy.md`)
- Playbooks stay in `/playbooks` and `_registry.yaml`. No per-city forks.
- L3 packs are deltas only.
- Path A must remain usable without paid APIs.

## After locale / playbook / field-note edits

```bash
make site && make check
```

Commit `docs/data/progress.json` with the change (or let `sync-site-data.yml` refresh on `main`).

## Prefer

1. Real field notes (`field-notes/_template.md`)
2. L3 packs
3. Glossary depth
4. Registry + playbook quality

Avoid: marketing copy in schemas, duplicated docs, hardcoded site stats.

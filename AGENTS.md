# Agent rules — DeployerX

## Session loop (mandatory)

1. **Start:** read [`STATUS.md`](STATUS.md) + [`ROADMAP.md`](ROADMAP.md). Do not invent priorities.
2. **Work:** one roadmap item or clearly scoped bugfix.
3. **End:** update STATUS (Where we are / Next / Session log) + ROADMAP checkboxes; run `make status`.
4. If locale/playbook/field-note changed: `make site && make check`.

## Contract

- Hierarchy: `_global` → L1 → L2 → L3 (`schema/hierarchy.md`)
- Playbooks: `/playbooks` + `_registry.yaml`. No per-city forks.
- L3 = deltas only. Path A stays zero paid API.
- Metrics must stay honest (no counting stubs/templates as seeded).
- Evals stay runnable: playbook changes keep `cases.json` + fixtures in sync; `make check` (includes eval selftest) must stay green.

## Prefer

1. Real field note (Phase 1)
2. Seeded L3 quality
3. Glossary depth
4. Registry / playbook quality

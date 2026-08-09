# Playbook contract

Playbooks are **global**. Locales overlay language and trust; they do not copy the playbook tree.

## Registry

`playbooks/_registry.yaml` is the index used by the CLI and site generator.

## Required files

| File | Purpose |
|------|---------|
| `README.md` | id, audience, status, one-liner, time-to-first-win |
| `decide.md` | When to use / when not |
| `deploy.md` | Path A (zero cost) then optional upgrades |
| `cost.md` | Cost bands in local currency terms |
| `prompts/` | System prompts by language |
| `evals/` | `cases.json` (machine-checkable, run via `python3 -m evals.run`) + `fixtures/` (scorer regression tests) + human-readable summary |

## Frontmatter (README)

```yaml
---
id: whatsapp-shop-faq
audience: [retail, kirana]
locales: [in]
min_budget_inr: 0
needs_engineer: false
channels: [whatsapp]
status: seeded
---
```

## Rules

- Include an explicit **Do NOT use when** section.
- Path A must work without paid APIs or custom servers.
- Customer-facing automation starts with human approval.

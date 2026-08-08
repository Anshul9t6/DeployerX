# Playbook schema

Every playbook MUST include:

| File | Purpose |
|------|---------|
| `README.md` | One-liner, audience, time-to-first-win |
| `decide.md` | When to use / when NOT to use |
| `deploy.md` | Step-by-step Monday plan |
| `cost.md` | Monthly cost bands (INR) |
| `prompts/` | System + task prompts (locale-aware) |
| `evals/` | Sample inputs + expected behavior |

## Frontmatter

```yaml
---
id: whatsapp-shop-faq
audience: [retail, kirana, local-services]
locales: [in]
min_budget_inr: 0
needs_engineer: false
channels: [whatsapp]
status: seeded
---
```

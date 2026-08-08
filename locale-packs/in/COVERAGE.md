# India coverage tracker (L1 → L2 → L3)

Goal: **every state/UT (L2) + every district (L3)**.

```bash
python3 scripts/coverage.py
python3 scripts/seed_india_l2.py   # create missing L2 stubs only
```

Full L2 list: [`l2/_index.yaml`](l2/_index.yaml)  
World registry: [`../_registry.yaml`](../_registry.yaml)

## Status meanings

| Status | Meaning |
|--------|---------|
| listed | L2 stub from index |
| seeded | Real notes or ≥1 L3 pack |
| verified | Field deployment linked |

## L2

All **36** states/UTs have `_meta.yaml` (seeded or listed stubs).

## L3 seeded (major cities + example)

| L2 | L3 |
|----|----|
| Uttar Pradesh | varanasi |
| Delhi | new-delhi |
| Maharashtra | mumbai-suburban, pune |
| Karnataka | bengaluru-urban |
| Tamil Nadu | chennai |
| Telangana | hyderabad |
| West Bengal | kolkata |
| Gujarat | ahmedabad |
| Rajasthan | jaipur |
| Bihar | patna |

## Glossaries

| Lang | File | Status |
|------|------|--------|
| hi | `glossary/hi.yaml` | seeded |
| mr, ta, kn, te, bn, gu | `glossary/*.yaml` | stub — extend via PR |

## Claim an L3

1. Open L3 issue template
2. Copy `locale-packs/_templates/l3/`
3. PR: `locale(in): add <district>, <state>`

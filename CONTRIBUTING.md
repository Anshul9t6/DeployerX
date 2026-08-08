# Contributing to DeployerX

**Mission:** Forward-deployed AI for the rest of the world — decisioning + playbooks + locale packs to e/acc.

We cover Earth as a tree:

`_global` → **country (L1)** → **state/province (L2)** → **district (L3)**

India is first. Every other country follows the same shape.

## Design rule (read this)

| Do | Don't |
|----|-------|
| Put shared content at the highest true level | Copy a whole playbook into a district folder |
| Add **deltas only** at L2/L3 | Duplicate global safety rules in every pack |
| Use ISO country codes + kebab slugs | Invent a new folder layout per country |
| Keep playbooks in `/playbooks` | Fork `whatsapp-shop-faq` per city |

See [`schema/hierarchy.md`](schema/hierarchy.md).

## Contribution ladder (impact order)

1. **L3 pack** — your district/county  
2. **Field note** — real deployment receipts  
3. **Glossary** — jargon → plain local language  
4. **L2 pack** — state/province meta + languages  
5. **L1 country pack** — open a new country  
6. **Global playbook** — new use case for everyone  

## Add an L3 pack (any country)

```bash
cc=in
l2=uttar-pradesh
l3=your-district

mkdir -p locale-packs/$cc/l2/$l2/l3/$l3
cp locale-packs/_templates/l3/* locale-packs/$cc/l2/$l2/l3/$l3/
```

Fill README / constraints / examples → PR titled:

`locale(<cc>): add <L3>, <L2>`

## Open a country (L1)

1. Copy `locale-packs/_templates/country/_meta.yaml` → `locale-packs/<cc>/_meta.yaml`
2. Add `constraints.md` (deltas from `_global` only)
3. Add `l2/_index.yaml` (full L2 list — goal)
4. Register in `locale-packs/_registry.yaml`
5. Seed one L3 example

PR title: `locale: open <Country> (<cc>)`

## Add a global playbook

1. Copy `playbooks/_templates/playbook/`
2. Required: `README.md`, `decide.md`, `deploy.md`, `cost.md`, `prompts/`, `evals/`
3. Must include when *not* to use it
4. Locale-specific prompts may live under the playbook as `prompts/system.<lang>.md` — still one playbook

PR title: `playbook: <id>`

## Validation

```bash
python3 scripts/validate.py
python3 -m decision.resolve in uttar-pradesh varanasi
```

## Code of conduct (short)

Be kind. Optimize for non-engineer operators. Prefer clarity over cleverness. No PII in the repo.

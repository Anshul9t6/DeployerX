# Contributing

README opens with the L3 ask. This file is the folder contract.

## Principles

1. Same folder contract for every country (`schema/hierarchy.md`)
2. Playbooks are global; locales are deltas
3. No PII in the repo
4. Prefer clarity over slogans

## Contribute

1. Read [STATUS.md](STATUS.md) / [ROADMAP.md](ROADMAP.md) so you know current phase
2. Highest leverage: **L3 locale pack** — `locale-packs/_templates/l3/`
3. Field note — `field-notes/_template.md`
4. After coverage edits: `make status && make site && make check`

## L3 pack

```bash
cc=in l2=rajasthan l3=your-district
mkdir -p locale-packs/$cc/l2/$l2/l3/$l3
cp locale-packs/_templates/l3/* locale-packs/$cc/l2/$l2/l3/$l3/
```

PR title: `locale(<cc>): add <L3>, <L2>`

## Playbook

Copy `playbooks/_templates/playbook/`, register in `playbooks/_registry.yaml`.  
New language: add `prompts/system.<lang>.md` + `evals/cases-<lang>.json` + `fixtures-<lang>/`.

## Site data

```bash
make site && make check
```

Commit `docs/data/progress.json` with coverage changes.

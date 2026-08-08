# Contributing

## Principles

1. Same folder contract for every country (`schema/hierarchy.md`)
2. Playbooks are global; locales are deltas
3. No PII in the repo
4. Prefer clarity over slogans

## Highest leverage

1. L3 locale pack — `locale-packs/_templates/l3/`
2. Field note — `field-notes/_template.md`
3. Glossary entries
4. Playbook improvement + `_registry.yaml` update

## L3 pack

```bash
cc=in l2=uttar-pradesh l3=your-district
mkdir -p locale-packs/$cc/l2/$l2/l3/$l3
cp locale-packs/_templates/l3/* locale-packs/$cc/l2/$l2/l3/$l3/
```

PR title: `locale(<cc>): add <L3>, <L2>`

## Playbook

Copy `playbooks/_templates/playbook/`, register in `playbooks/_registry.yaml`.

## Site data

```bash
make site && make check
```

Commit `docs/data/progress.json` with coverage changes.

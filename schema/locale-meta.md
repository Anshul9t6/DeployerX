# Meta schemas

Prose lives in `README.md`. `_meta.yaml` is **data only** (no Markdown body).

## L1

```yaml
level: 1
country: in
name: India
admin_labels:
  l2: state
  l3: district
languages_default: [hi, en]
currency: INR
status: seeded
maintainers: []
```

## L2

```yaml
level: 2
country: in
l2: uttar-pradesh
name: Uttar Pradesh
languages: [hi, ur, en]
status: seeded
maintainers: []
```

## L3 README frontmatter

```yaml
level: 3
country: in
l2: uttar-pradesh
l3: varanasi
languages: [hi, bho]
status: seeded
maintainers: []
```

## Playbooks

Index: `playbooks/_registry.yaml`. Required files: README, decide, deploy, cost, prompts/, evals/.

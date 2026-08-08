# DeployerX

**Forward-deployed AI for the rest of the world — decisioning + playbooks + locale packs to e/acc.**

[![DeployerX coverage atlas](docs/assets/atlas.jpg)](https://anshul9t6.github.io/DeployerX/)

DeployerX helps a local operator go from *“I heard of AI”* to *a working AI workflow in their language, on their tools, this week*.

**Coverage model:** every country (L1) → every state/province (L2) → every district/county (L3).  
**India first.** Then the world — by contribution, not by one person.

**Live site:** https://anshul9t6.github.io/DeployerX/ · **Share kit:** [`SHARE.md`](SHARE.md) · **First deployment:** [`field-notes/FIRST_DEPLOYMENT.md`](field-notes/FIRST_DEPLOYMENT.md)

## Mission

Accelerate human progress by making AI **deployable where people actually live and work**.

The bottleneck is not model capability. It is English-only jargon, weak “what do I do Monday?” guidance, and missing local context (language, payments, trust, tools).

## Architecture (scalable by design)

```
┌─────────────────┐
│  Playbooks (L0) │  ship once — global recipes
└────────┬────────┘
         │
┌────────▼────────┐
│ Locale cascade  │  _global → country → L2 → L3
│ (local wins)    │  deltas only at each level
└────────┬────────┘
         │
┌────────▼────────┐
│  Decisioning    │  asks constraints → recommends playbook + locale path
└─────────────────┘
```

| Layer | What ships here | Who contributes |
|-------|-----------------|-----------------|
| **Global playbooks** | How to deploy a use case | Core maintainers + domain experts |
| **L0 `_global`** | Universal safety + base glossary | Core maintainers |
| **L1 country** | Payments, channels, languages, L2 index | Country maintainers |
| **L2 state/province** | Regional language/ops notes | Regional contributors |
| **L3 district** | Hyperlocal examples & trust deltas | Local owners / FDEs |

**Rule:** common things ship once at the highest true level. L3 never forks a playbook — it only adds local deltas.

Full contract: [`schema/hierarchy.md`](schema/hierarchy.md)

## India-first (seed)

| Layer | Path | Status |
|--------|------|--------|
| World registry | [`locale-packs/_registry.yaml`](locale-packs/_registry.yaml) | Live |
| Global pack | [`locale-packs/_global/`](locale-packs/_global/) | Seeded |
| India L1 | [`locale-packs/in/`](locale-packs/in/) | Seeded |
| L2 index | [`locale-packs/in/l2/_index.yaml`](locale-packs/in/l2/_index.yaml) | All states/UTs listed |
| L3 examples | India major cities + `br/.../sao-paulo` | Seeded |
| Glossaries | `hi` + full `mr`/`ta` · Brazil `pt` | Seeded |

## Website (GitHub Pages · free · live progress)

**https://anshul9t6.github.io/DeployerX/**

Static site in [`docs/`](docs/). Coverage stats/lists load from generated [`docs/data/progress.json`](docs/data/progress.json).

```bash
python3 scripts/generate_site_data.py   # refresh site data after locale/playbook changes
python3 scripts/validate.py             # fails if progress.json is stale
```

Agents: see [`AGENTS.md`](AGENTS.md). Maintainers: [`docs/maintain.html`](docs/maintain.html).

## Quick start

```bash
python3 -m decision.cli
python3 -m decision.resolve in uttar-pradesh varanasi
python3 scripts/validate.py
python3 scripts/coverage.py
```

## Repo map

```
playbooks/                 # Global recipes (ship once)
locale-packs/
  _global/                 # L0 defaults
  _registry.yaml           # Countries in progress
  _templates/              # Country + L3 templates
  in/                      # First country (L1→L2→L3)
decision/                  # CLI + locale resolver
schema/                    # Hierarchy & pack contracts
field-notes/               # Real deployments (receipts)
```

## Playbooks (global)

| Playbook | For |
|----------|-----|
| [WhatsApp shop FAQ](playbooks/whatsapp-shop-faq/) | Kirana / retail / local services |
| [Clinic WhatsApp FAQ](playbooks/clinic-whatsapp-faq/) | Clinics / labs — **no medical advice** |

Local trust notes come from locale packs — never fork playbooks per city.

## Contribute (the only way we cover Earth)

1. **L3 district pack** — highest leverage  
2. **L2 / L1 pack** — open a state or country  
3. **Global playbook** — new use case for everyone  
4. **Field note** — proof from a real deployment  

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT

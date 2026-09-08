# DeployerX

A generic chatbot will invent a discount. A kirana owner will lose trust in one message.

DeployerX is an **individual AI-deployment kit** for the world: one person, the operator's language, the same playbook tree in every country. WhatsApp FAQ assistants answer from the owner's list — and **evals fail the reply** if the model invents a price, a rank, or a diagnosis.

[![Validate](https://github.com/Anshul9t6/DeployerX/actions/workflows/validate.yml/badge.svg)](https://github.com/Anshul9t6/DeployerX/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-0b1210)](LICENSE)

**Live atlas:** [anshul9t6.github.io/DeployerX](https://anshul9t6.github.io/DeployerX/) · **World kit:** [`guides/world.md`](guides/world.md) · **Field receipt (human):** [`guides/receipt-plan.md`](guides/receipt-plan.md) · **Claim a district:** [open an L3 issue](https://github.com/Anshul9t6/DeployerX/issues/new?template=l3_pack.yml)

[![Coverage atlas](docs/assets/atlas.jpg)](https://anshul9t6.github.io/DeployerX/)

India has 36 states/UTs on the map. Most **districts** are empty. If you know how people actually message in yours — Hindi, Hinglish, Tamil, Gujarati, Portuguese — that pack is the highest-leverage PR in this repo.

---

## Why look

| Generic assistant | This kit |
|-------------------|----------|
| English prompt, invented ₹ | FAQ-grounded; **no invented prices** |
| Same bot in Jaipur and Recife | Locale cascade: country → state → **district** (local wins) |
| “Looks good to me” | Machine-checkable evals before anyone sends a WhatsApp |
| Fork a chatbot per city | **Global playbooks.** Locales are deltas only |

Path A is today: browser model, copy-paste, human approval. No paid API. ~30 minutes.

Customer: *थोड़ा सस्ता हो जाएगा?*  
Eval `discount-ask`: if the model writes `10% off`, **the suite fails.** That is the product.

## Contribute (start here)

You do not need to be an ML engineer. You need to have *been in the shop*.

| If you… | Do this | Time |
|---------|---------|------|
| Know your district’s language, UPI/Pix habits, festival FAQ spikes | **L3 locale pack** (template below) | ~30 min |
| Speak Portuguese (Brazil is already L1) | Use `prompts/system.pt.md` + `evals/cases-pt.json` | ~15 min |
| Sat with an owner and ran Path A | [Field note](field-notes/_template.md) with real Results | after 7 days |
| Have a repeat-FAQ use case that is not shop/clinic | New [playbook](playbooks/_templates/playbook/) + evals | longer |

### L3 pack — copy, fill, PR

```bash
cc=in l2=rajasthan l3=your-district          # any country; same folder shape
mkdir -p locale-packs/$cc/l2/$l2/l3/$l3
cp locale-packs/_templates/l3/* locale-packs/$cc/l2/$l2/l3/$l3/
```

Write **deltas only**: how people write on WhatsApp, what the bot must never say, one real example. No playbook forks. No phone numbers.

PR title: `locale(<cc>): add <L3>, <L2>`  
Issue form: [Add L3 locale pack](https://github.com/Anshul9t6/DeployerX/issues/new?template=l3_pack.yml)  
Contract: [`CONTRIBUTING.md`](CONTRIBUTING.md) · [`schema/hierarchy.md`](schema/hierarchy.md)

Glossaries waiting on a speaker: `bn` `gu` `kn` `te` (stubs). Brazil needs a município L3 + a named maintainer.

---

## Quick start

```bash
# 1. decide — no terminal prompts needed; flags or defaults
python3 -m decision.cli --country in --l2 rajasthan --l3 jaipur --language hi --use-case shop_faq

# 2. build the paste-ready prompt from the OWNER's FAQ + district constraints
#    faq.txt or a Sheet export: question,answer → faq.csv
python3 -m decision.prompt whatsapp-shop-faq --faq faq.csv --locale in/rajasthan/jaipur --lang hi --out prompt.txt

# 3. eval before anyone sends a WhatsApp
python3 -m evals.run prepare whatsapp-shop-faq --locale in/rajasthan/jaipur   # zero cost, browser model
python3 -m evals.run selftest                                                 # hi + pt suites, no network

make check                                           # hierarchy + unit tests + evals + site data
make status                                          # honest metrics (field notes still 0)
```

Path A: `prompt.txt` → browser model → **owner sends** every reply for 7 days.  
Hindi Path A (shop): [`deploy.hi.md`](playbooks/whatsapp-shop-faq/deploy.hi.md) · owner card: [`operator-card.hi.md`](playbooks/whatsapp-shop-faq/operator-card.hi.md).  
Hindi Path A (clinic): [`deploy.hi.md`](playbooks/clinic-whatsapp-faq/deploy.hi.md) · staff card: [`operator-card.hi.md`](playbooks/clinic-whatsapp-faq/operator-card.hi.md).

| Playbook | Audience |
|----------|----------|
| [whatsapp-shop-faq](playbooks/whatsapp-shop-faq/) | Retail / local services |
| [clinic-whatsapp-faq](playbooks/clinic-whatsapp-faq/) | Clinics / labs (**non-clinical** FAQ only) |

City process: [`guides/city-start.md`](guides/city-start.md) · What to deploy (P0→X): [`guides/deployments-50.md`](guides/deployments-50.md)

## What it is

1. **Playbooks** — global recipes (do not fork per city)
2. **Locale packs** — `_global` → country → L2 → L3
3. **Decisioning** — constraints → recommended playbook + locale; `decision.prompt` writes the paste-ready system prompt
4. **Evals** — never invent a price; escalate when unsure; never give medical advice
5. **MCP server** — the kit as agent tools (Claude / any MCP client; local files only)

Same tree for every country. India is the reference.

## Field notes

**None yet.** Coverage is not proof. First Path A target: Jaipur (`in/rajasthan/jaipur`), maintainer [`Anshul9t6`](https://github.com/Anshul9t6). Dated notes with Results go in [`field-notes/`](field-notes/). README will cite a metric only after one exists.

## Evals

Every playbook ships `evals/cases.json`. Scoring is deterministic — API, browser Path A, and CI selftest grade the **same** rules.

| Mode | Command | Cost |
|------|---------|------|
| API | `python3 -m evals.run api <playbook> [--locale in/rajasthan/jaipur]` | Anthropic API |
| Path A | `prepare` → paste into a browser model → `score` | zero |
| Selftest | `python3 -m evals.run selftest` | zero, no network |

The system prompt under test is assembled the same way as `deploy.md`: playbook prompt + FAQ + merged locale cascade. Run evals before any customer-facing use.

## Agent access (MCP)

```bash
pip install mcp
claude mcp add deployerx -- python3 /absolute/path/to/DeployerX/deployerx_mcp/server.py
```

Then: *“Set up a WhatsApp FAQ assistant for a guest house in Jaipur.”*  
It picks the playbook, pulls locale constraints, assembles the prompt from your FAQ, and grades evals.  
Setup: [`deployerx_mcp/README.md`](deployerx_mcp/README.md)

## Architecture

```
playbooks/          # global recipes (do not fork per city)
  <id>/evals/       # cases.json + fixtures (runnable)
locale-packs/
  _global/          # L0 defaults
  <cc>/             # L1 country
    l2/<slug>/      # L2 state/province/…
      l3/<slug>/    # L3 district/county/…  (deltas only)
decision/           # resolver + CLI + prompt assembly
evals/              # eval runner + deterministic checks
tests/              # unit tests (stdlib unittest) — part of make check
deployerx_mcp/      # MCP server — optional: pip install mcp
docs/               # GitHub Pages ← docs/data/progress.json
```

Cascade: `_global` → country → L2 → L3 (local wins).

## Coverage

| Scope | Status |
|-------|--------|
| India L2 | 36/36 metas |
| India L3 | 1 seeded · 10 draft · **the rest is the contribution surface** |
| Brazil L2 | 27/27 estados + DF · São Paulo L3 **draft** · `system.pt.md` + `cases-pt.json` |
| Field notes | 0 |

```bash
make site     # regenerate docs/data/progress.json
make check    # validate hierarchy + stale site data + eval selftest
```

[`STATUS.md`](STATUS.md) (today) · [`ROADMAP.md`](ROADMAP.md) (targets)

## Ops

| Doc | Purpose |
|-----|---------|
| [STATUS.md](STATUS.md) | Where we are / next |
| [ROADMAP.md](ROADMAP.md) | Phased targets |
| [AGENTS.md](AGENTS.md) | Rules for automated contributors |
| [field-notes/](field-notes/) | Deployment receipts |
| [SHARE.md](SHARE.md) | Launch copy (after a real field note) |
| [guides/world.md](guides/world.md) | Same kit, any country (open L1 only with a maintainer) |
| [guides/receipt-plan.md](guides/receipt-plan.md) | Human-only field receipt (desk commands are in `make check`) |
| [guides/fde.md](guides/fde.md) | Maintainer: Path A scope (what we deploy vs not) |
| [guides/audit.md](guides/audit.md) | Product audit scorecard (/10 per dimension) + what to fix next |

## License

MIT · [Code of conduct](CODE_OF_CONDUCT.md)

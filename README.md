# DeployerX

Locale-aware playbooks for deploying AI with non-engineer operators.

**Live atlas:** https://anshul9t6.github.io/DeployerX/

[![Coverage atlas](docs/assets/atlas.jpg)](https://anshul9t6.github.io/DeployerX/)

## What it is

The barrier to AI adoption for a kirana owner or a small clinic isn't model
capability — it's language, trust, and local context. DeployerX is an
open-source field kit that packages those three things:

1. **Playbooks** — reusable deployment recipes (global)
2. **Locale packs** — country → admin L2 → admin L3 context (local deltas)
3. **Decisioning** — constraint questionnaire → recommended playbook + locale path
4. **Evals** — machine-checkable behavior tests per playbook (never invent a
   price, escalate when unsure, never give medical advice)
5. **MCP server** — plug the kit into Claude or any MCP client, so agents can
   pick playbooks, pull locale context, assemble prompts, and grade evals

India is the reference implementation. The same tree shape applies to every country.

## Quick start

```bash
make status                                          # where we are + refresh STATUS.md metrics
python3 -m decision.cli                              # constraints → recommended playbook + locale
python3 -m decision.resolve in uttar-pradesh varanasi
python3 -m evals.run api whatsapp-shop-faq --locale in/rajasthan/jaipur   # eval scorecard via Claude API
python3 -m evals.run prepare whatsapp-shop-faq       # zero-cost eval bundle (browser model)
make check                                           # hierarchy + site data + eval selftest
```

**Session tracking:** [`STATUS.md`](STATUS.md) (today) · [`ROADMAP.md`](ROADMAP.md) (targets)  
**Start a city:** [`guides/city-start.md`](guides/city-start.md) · **What to deploy:** [`guides/deployments-50.md`](guides/deployments-50.md)  
**FDE / money overlay:** [`guides/fde.md`](guides/fde.md) — FAQ drafts on WhatsApp, not a shop-running SaaS.

Path A (no paid APIs): open a playbook → browser model → human approval on the chat channel you already use.

| Playbook | Audience |
|----------|----------|
| [whatsapp-shop-faq](playbooks/whatsapp-shop-faq/) | Retail / local services |
| [clinic-whatsapp-faq](playbooks/clinic-whatsapp-faq/) | Clinics / labs (non-clinical FAQ only) |

## Evals

Every playbook ships a machine-checkable eval suite
(`playbooks/<id>/evals/cases.json`). The checks encode the deployment
contract: answer only from the owner's FAQ, **never invent prices or
discounts**, escalate to the owner when unsure, and (for clinics) never
diagnose, prescribe, or interpret reports.

Three ways to run them — scoring is deterministic, so all three grade
against the same rules:

| Mode | Command | Cost |
|------|---------|------|
| API | `python3 -m evals.run api <playbook> [--locale in/rajasthan/jaipur]` | Anthropic API |
| Path A (manual) | `python3 -m evals.run prepare <playbook>` → paste into a browser model → `score` | zero |
| Selftest (CI) | `python3 -m evals.run selftest` — grades bundled fixtures | zero, no network |

The system prompt under test is assembled the same way an operator does it
in `deploy.md`: playbook prompt + FAQ + the merged locale cascade. Run evals
before any customer-facing use.

## Agent access (MCP)

The whole kit is usable by AI agents via the
[Model Context Protocol](https://modelcontextprotocol.io) — an open standard.
The server runs locally, reads only this repo's files (plus the FAQ text you
pass in), and makes no network calls of its own.

```bash
pip install mcp
claude mcp add deployerx -- python3 /absolute/path/to/DeployerX/deployerx_mcp/server.py
```

Then ask Claude: *"Set up a WhatsApp FAQ assistant for my guest house in
Varanasi"* — it picks the playbook, pulls the locale constraints, assembles
the prompt from your real FAQ, and grades it with the evals.
Details + Claude Desktop config: [`deployerx_mcp/README.md`](deployerx_mcp/README.md)

## Architecture

```
playbooks/          # global recipes (do not fork per city)
  <id>/evals/       # cases.json + fixtures (runnable)
locale-packs/
  _global/          # L0 defaults
  <cc>/             # L1 country
    l2/<slug>/      # L2 state/province/…
      l3/<slug>/    # L3 district/county/…  (deltas only)
decision/           # resolver + CLI
evals/              # eval runner + deterministic checks
deployerx_mcp/      # MCP server — the kit as agent tools (optional: pip install mcp)
docs/               # GitHub Pages (reads docs/data/progress.json)
```

Cascade: `_global` → country → L2 → L3 (local wins).  
Contract: [`schema/hierarchy.md`](schema/hierarchy.md)

## Coverage

| Scope | Status |
|-------|--------|
| India L2 | 36/36 metas |
| India L3 | major cities seeded; PRs welcome |
| Brazil L2 | 27/27 estados + DF |
| Site stats | generated from repo via `scripts/generate_site_data.py` |

```bash
make site     # regenerate docs/data/progress.json
make check    # validate hierarchy + stale site data
```

## Contribute

Highest leverage: **L3 locale pack** for your district.  
See [CONTRIBUTING.md](CONTRIBUTING.md). Issue templates cover L3, country, and playbook PRs.

Project state for contributors/agents: [STATUS.md](STATUS.md) · [ROADMAP.md](ROADMAP.md)

## Ops

| Doc | Purpose |
|-----|---------|
| [STATUS.md](STATUS.md) | Where we are today / next |
| [ROADMAP.md](ROADMAP.md) | Phased targets |
| [AGENTS.md](AGENTS.md) | Rules for automated contributors |
| [field-notes/](field-notes/) | Deployment receipts |
| [SHARE.md](SHARE.md) | Launch copy (after a real field note) |
| [guides/fde.md](guides/fde.md) | What Path A can sell vs automate; FDE portfolio |

## License

MIT

# Status — DeployerX

> **Read this first in every new session.** Update it before you stop.  
> Roadmap: [`ROADMAP.md`](ROADMAP.md) · Live atlas: https://anshul9t6.github.io/DeployerX/

<!-- status:meta -->
- **Updated:** 2026-09-08
- **Phase:** 1 — Proof (first real deployment)
- **Branch tip:** run `git log -1 --oneline`
<!-- /status:meta -->

## Where we are

Path A is operator-ready in Hindi: `deploy.hi.md` + owner/staff cards for both playbooks; `decision.prompt --faq` takes a Sheet CSV; MCP reads `faq_path`. Audit 6.8/10. **No real field deployment yet** — Proof scores 2/10 and is the only thing that moves the hiring signal.

### Works today

| Capability | Notes |
|------------|--------|
| Locale cascade | `decision.resolve` prints leaf excerpt by default; `--merge` for full stack |
| Playbooks | `whatsapp-shop-faq`, `clinic-whatsapp-faq` via `_registry.yaml` |
| Evals | 4 suites (hi + pt × shop/clinic); `selftest` 38 fixture verdicts; `--cases cases-pt.json` |
| MCP server | `deployerx_mcp/` — 8 tools; `build_system_prompt` accepts `faq` or `faq_path` (txt/CSV); local, no network |
| CLI | `python3 -m decision.cli` — flags or `--no-input`; interactive only on a TTY |
| Prompt | `python3 -m decision.prompt <pb> --faq faq.txt\|faq.csv --locale cc/l2/l3 --lang hi\|en\|pt` → paste-ready `prompt.txt` |
| Tests | `tests/` 45 stdlib unit tests (checks, prompt, CLI, CSV, MCP) + `compileall` — in `make check` + CI |
| Pages | `docs/` ← `docs/data/progress.json` (`make site`) |
| India | 36 L2 metas; **1 L3 seeded** (Varanasi); 10 L3 draft; Jaipur maintainer `Anshul9t6` |
| Brazil | 27 L2; São Paulo L3 **draft** (pt prompts exist; no maintainer, not seeded) |
| Glossaries | seeded: hi, mr, ta · stub: bn, gu, kn, te |
| Path A scope | `guides/fde.md` + `guides/world.md` — FAQ drafts; same tree worldwide |

### Honest metrics

<!-- status:metrics -->
```
generated_at:     2026-09-08T18:40:40Z
countries:        2
playbooks:        2
india_l2_seeded:  10 / index 36
india_l3_seeded:  1
india_l3_draft:   10
glossaries:       3 seeded · 4 stub
field_notes:      0  ← must be >0 before Phase 1 complete
```
<!-- /status:metrics -->

## In progress

- Jaipur field deployment (AM) — follow `guides/city-start.md`

## Blocked / waiting on human

- Real Path A Results (cannot invent)
- GitHub repo About → Website `https://anshul9t6.github.io/DeployerX/` · Description in [`SHARE.md`](SHARE.md)

## Next (do in order)

1. Follow [`guides/receipt-plan.md`](guides/receipt-plan.md) (desk check, then one Jaipur P0)
2. Pick operator from [`guides/deployments-50.md`](guides/deployments-50.md) (kirana / coaching / clinic / guest house)
3. Run [`guides/city-start.md`](guides/city-start.md) + [`field-notes/FIRST_DEPLOYMENT.md`](field-notes/FIRST_DEPLOYMENT.md)
4. Field note `field-notes/YYYY-MM-DD-in-rajasthan-jaipur-<topic>.md` with Results
5. `make site && make check && make status`; mark Jaipur L3 verified when earned

## Session log (newest first)

| Date | What landed |
|------|-------------|
| 2026-09-08 | Hindi `deploy.hi.md` + clinic staff card; Sheet CSV FAQ; MCP `faq_path`; `compileall` in `make check` |
| 2026-09-08 | Product audit (`guides/audit.md`, 5.8→6.7/10): `decision.prompt` paste-ready prompt from owner FAQ; CLI flags + no-TTY fix; `prepare --out-dir` fix; 32 unit tests in `make check`; Hindi owner card |
| 2026-08-21 | Atlas + Path A (pt) aligned to world pitch; `guides/receipt-plan.md` gated by `make check`; PR template |
| 2026-08-21 | World kit: Portuguese prompts + evals; `R$` price checks; `guides/world.md`; São Paulo L3 draft (honest); CODE_OF_CONDUCT |
| 2026-08-15 | README hook: invented-discount eval as the product; contribute table + L3 copy-paste first; CI badge |
| 2026-08-15 | Portfolio hardening: leaf constraint excerpt by default; Jaipur maintainer `Anshul9t6`; shop evals for rank-promises + invented tourist timings; README product-first with empty field-notes section |
| 2026-08-15 | FDE path guide (`guides/fde.md`): honest automation/money/portfolio overlay; field-note template adds baseline volume, time-to-reply, eval walk |
| 2026-08-09 | MCP server (`deployerx_mcp/`): kit exposed as 8 agent tools over stdio; SDK-free tool layer covered by `make check` selftest; setup docs for Claude Desktop/Code |
| 2026-08-09 | Runnable eval harness: `cases.json` per playbook, deterministic checks (invented-price, escalation, forbidden content), API + zero-cost Path A modes, fixture selftest wired into `make check`/CI |
| 2026-08-08 | City start guide + top-50 deployments; Jaipur L3 deepened for field work |
| 2026-08-08 | Dev loop: STATUS.md + ROADMAP.md + `make status` |
| 2026-08-08 | Honest metrics, playbook registry, professional README, Pages atlas |
| 2026-08-08 | Initial scaffold |
## Agent checklist (end of session)

- [x] `ROADMAP.md` checkboxes match reality
- [x] This file: Updated date, Where we are, Next, Session log
- [x] `make status` (refresh metrics block)
- [x] If locale/playbook/field-note changed: `make site && make check`
- [x] Tell the human what’s next in one sentence

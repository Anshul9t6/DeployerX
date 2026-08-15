# Status — DeployerX

> **Read this first in every new session.** Update it before you stop.  
> Roadmap: [`ROADMAP.md`](ROADMAP.md) · Live atlas: https://anshul9t6.github.io/DeployerX/

<!-- status:meta -->
- **Updated:** 2026-08-15
- **Phase:** 1 — Proof (first real deployment)
- **Branch tip:** run `git log -1 --oneline`
<!-- /status:meta -->

## Where we are

Scaffold is professional and metrics are honest. Public README opens with a contribute hook (L3 district pack) and stays product-first — no invented Results. Resolver prints the **leaf constraint excerpt** by default. Jaipur L3 lists maintainer `Anshul9t6`. Shop evals encode the P0 never-list. **No real field deployment yet** — that remains the only thing that makes an FDE claim true.

### Works today

| Capability | Notes |
|------------|--------|
| Locale cascade | `decision.resolve` prints leaf excerpt by default; `--merge` for full stack |
| Playbooks | `whatsapp-shop-faq`, `clinic-whatsapp-faq` via `_registry.yaml` |
| Evals | shop: 7 cases (incl. rank-promise, tourist-aarti); clinic: 5; `api` / `prepare`+`score` / `selftest` |
| MCP server | `deployerx_mcp/` — 8 tools (playbooks, locale cascade, prompt assembly, eval grading) for Claude/any MCP client; local, repo-files-only, no network |
| CLI | `python3 -m decision.cli` (defaults to `in/rajasthan/jaipur`) |
| Pages | `docs/` ← `docs/data/progress.json` (`make site`) |
| India | 36 L2 metas; **1 L3 seeded** (Varanasi); 10 L3 draft; Jaipur maintainer `Anshul9t6` |
| Brazil | 27 L2 listed/draft; São Paulo L3 scaffold; status **draft** |
| Glossaries | seeded: hi, mr, ta · stub: bn, gu, kn, te |
| Path A scope | `guides/fde.md` — FAQ drafts + setup fees, not MSME SaaS |

### Honest metrics

<!-- status:metrics -->
```
generated_at:     2026-08-15T17:52:00Z
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

1. Read [`guides/fde.md`](guides/fde.md) so the operator pitch is FAQ drafts + 7-day approval, not “AI automation”
2. Pick a Jaipur P0 operator from [`guides/deployments-50.md`](guides/deployments-50.md) (kirana / coaching / clinic / guest house)
3. Run [`guides/city-start.md`](guides/city-start.md) + [`field-notes/FIRST_DEPLOYMENT.md`](field-notes/FIRST_DEPLOYMENT.md)
4. Field note `field-notes/YYYY-MM-DD-in-rajasthan-jaipur-<topic>.md` with Results (use the expanded template)
5. `make site && make check && make status`; mark Jaipur L3 verified when earned

## Session log (newest first)

| Date | What landed |
|------|-------------|
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

- [ ] `ROADMAP.md` checkboxes match reality
- [ ] This file: Updated date, Where we are, Next, Session log
- [ ] `make status` (refresh metrics block)
- [ ] If locale/playbook/field-note changed: `make site && make check`
- [ ] Tell the human what’s next in one sentence

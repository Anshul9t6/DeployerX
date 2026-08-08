# Status — DeployerX

> **Read this first in every new session.** Update it before you stop.  
> Roadmap: [`ROADMAP.md`](ROADMAP.md) · Live atlas: https://anshul9t6.github.io/DeployerX/

<!-- status:meta -->
- **Updated:** 2026-08-08
- **Phase:** 1 — Proof (hiring-grade)
- **Branch tip:** run `git log -1 --oneline`
<!-- /status:meta -->

## Where we are

Scaffold is professional and metrics are honest. Public site + India/Brazil trees exist. **No real field deployment yet** — that is the critical path.

### Works today

| Capability | Notes |
|------------|--------|
| Locale cascade | `decision.resolve` + `merged_constraints()` |
| Playbooks | `whatsapp-shop-faq`, `clinic-whatsapp-faq` via `_registry.yaml` |
| CLI | `python3 -m decision.cli` |
| Pages | `docs/` ← `docs/data/progress.json` (`make site`) |
| India | 36 L2 metas; **1 L3 seeded** (Varanasi); 10 L3 draft |
| Brazil | 27 L2 listed/draft; São Paulo L3 scaffold; status **draft** |
| Glossaries | seeded: hi, mr, ta · stub: bn, gu, kn, te |

### Honest metrics

<!-- status:metrics -->
```
generated_at:     2026-08-08T07:36:02Z
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

- (none — ready for Phase 1 field deployment)

## Blocked / waiting on human

- Real shop/clinic Path A (cannot invent Results)
- Push commits if remote behind
- GitHub repo About → Website URL

## Next (do in order)

1. Run Path A with [`field-notes/FIRST_DEPLOYMENT.md`](field-notes/FIRST_DEPLOYMENT.md)
2. Publish dated field note with filled Results → `make site && make check`
3. Mark that L3 `verified`; tick Phase 1 items in `ROADMAP.md`
4. Deepen home-district L3 (Phase 2)

## Session log (newest first)

| Date | What landed |
|------|-------------|
| 2026-08-08 | Dev loop: STATUS.md + ROADMAP.md + `make status` + session-loop agent rule |
| 2026-08-08 | Honest metrics, playbook registry, professional README, Pages atlas |
| 2026-08-08 | Initial scaffold: hierarchy, India/Brazil packs, two playbooks |

## Agent checklist (end of session)

- [ ] `ROADMAP.md` checkboxes match reality
- [ ] This file: Updated date, Where we are, Next, Session log
- [ ] `make status` (refresh metrics block)
- [ ] If locale/playbook/field-note changed: `make site && make check`
- [ ] Tell the human what’s next in one sentence

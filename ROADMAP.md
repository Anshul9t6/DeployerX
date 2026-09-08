# Roadmap — DeployerX

Single target plan. Check items off when **done and honest** (no vanity stubs).  
Session agents: read this + [`STATUS.md`](STATUS.md) before coding; update both when finishing work.

## North star

Locale-aware playbooks so non-engineer operators can run AI workflows in their language — Path A at zero paid cost — with dense L3 locale coverage starting in India.

---

## Phase 0 — Foundation

- [x] Locale cascade L0→L1→L2→L3 + hierarchy contract
- [x] Global playbooks + `_registry.yaml` (shop FAQ, clinic FAQ)
- [x] Decision CLI / resolver (+ constraint concatenate)
- [x] GitHub Pages atlas + generated `progress.json`
- [x] Honest metrics (stubs/templates don’t count as seeded)
- [x] India L2 index (36) + Brazil L2 index (27)
- [x] Makefile / AGENTS / professional README

## Phase 1 — Proof (first real deployment)

- [ ] One real Path A field note with **Results** filled (`field-notes/`) — **Jaipur recommended**
- [ ] Upgrade that locale’s L3 to `verified` after the note
- [ ] Share post only after the field note (`SHARE.md`)
- [ ] Repo About → Website set to Pages URL
- [x] City start guide + top-50 deployment catalog (`guides/`)
- [x] FDE path guide — what Path A can sell vs automate vs prove (`guides/fde.md`)

## Phase 2 — India depth

- [ ] ≥5 L3 packs at `seeded` (real local examples, not boilerplate)
- [ ] Glossaries: promote stubs (`bn` `gu` `kn` `te`) or remove from claims
- [x] One additional playbook **or** major upgrade to an existing playbook (evals + Path A) — runnable eval harness for both playbooks: `cases.json` + deterministic checks, API / zero-cost Path A / CI selftest modes
- [x] Portuguese Path A (`system.pt.md` + `cases-pt.json`) for both playbooks — Brazil language, São Paulo L3 stays **draft** until a real município receipt
- [ ] Home-district L3 owned by maintainer (AM or local contributor)

## Phase 3 — Multi-country

- [ ] Brazil: ≥1 real município L3 + maintainer listed
- [ ] Third country L1 opened only with a named maintainer
- [ ] Contribution funnel proven (external L3 PR merged)

## Phase 4 — Platform hardening

- [x] MCP server (`deployerx_mcp/`) — playbooks, locale cascade, prompt assembly, and evals exposed to any MCP client; tool layer covered by the CI selftest
- [ ] Strict YAML-only `_meta.yaml` for all L2 (migrate stubs)
- [ ] Optional schema validation (JSON Schema or PyYAML)
- [x] Decision CLI prints merged constraint excerpt by default
- [x] Paste-ready prompt command (`decision.prompt`) shared by evals + MCP; CLI non-interactive flags
- [x] Unit tests (`tests/`, stdlib) in `make check` + CI
- [ ] Operator docs in Hindi (`deploy.hi.md`, clinic owner card)
- [ ] `decision.prompt --faq` accepts CSV export (question,answer) from a Sheet
- [ ] Slimmer Pages CSS / fewer motion effects (optional)

---

## Out of scope (until Phase 1–2 done)

- Custom domain / `deployerx.github.io` org rename
- WhatsApp Business API productization
- Fine-tuning / vector DB platform
- Multi-tenant SaaS

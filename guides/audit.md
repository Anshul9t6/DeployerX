# Product audit — 2026-09-08

Scored as a first-time deployer would experience it: clone, run the entry points, sit with an owner. Scores are out of 10. Re-score after the first field note; most of the low numbers are one receipt away from moving.

## Scorecard

| Dimension | Before | After this audit | Why |
|-----------|-------:|-----------------:|-----|
| Problem clarity | 9 | 9 | “Generic bot invents a discount” is a failure operators recognise. Scope is explicit (FAQ drafts, not SaaS). |
| Operator usability | 4 | 7 | Before: `deploy.md` said “paste prompt + FAQ” but nothing assembled them; the `<<<FAQ>>>` marker was left to hand-editing. Now `decision.prompt` writes the paste-ready file; Hindi owner card exists. Still English-first docs. |
| Deployer / dev usability | 5 | 8 | CLI crashed on non-TTY (`EOFError`); `prepare --out-dir` crashed outside the repo. Both fixed; CLI has flags; every recommendation ends in copy-pasteable next commands. |
| Safety / eval rigour | 8 | 8 | Deterministic checks, four suites (hi + pt), CI selftest. No LLM-as-judge, which is a feature at this stage. |
| Reliability / tests | 4 | 7 | Before: only fixture selftest. Now 32 unit tests on the price checker, prompt assembly, and CLI, wired into `make check` and CI. No type-check or lint yet. |
| Value to operator | 6 | 7 | Zero-cost, 30-minute loop that stops invented prices is real value. Ceiling is bounded until Path B (quick replies) is documented from a real deployment. |
| Value to AM (hiring) | 5 | 5 | Architecture reads like FDE work. Unchanged because `field_notes: 0`. This number is the receipt. |
| Honesty of metrics | 9 | 9 | Stubs do not count as seeded; São Paulo was downgraded to draft; site regenerates from the repo. |
| World-readiness | 6 | 6 | Same tree in India and Brazil; Portuguese prompts + evals. No second maintainer, no non-Latin/Devanagari language beyond Hindi. |
| Contributor path | 7 | 7 | L3 template, issue forms, PR template, code of conduct. Zero external PRs yet. |
| Discoverability | 5 | 5 | Pages atlas and README hook exist. GitHub About/Website still unset (human). No share post until a receipt. |
| Proof | 2 | 2 | No field deployment. Everything else is scaffolding until this moves. |

**Overall:** 5.8 → **6.7**. The next two points come from one Jaipur receipt, not from more code.

## What changed in this audit

- `python3 -m decision.prompt <playbook> --faq faq.txt --locale cc/l2/l3 --lang hi|en|pt` — paste-ready prompt from the owner’s real FAQ. Shared by evals and MCP (`decision/prompt.py`).
- `python3 -m decision.cli` — flags for every answer, `--no-input`, auto non-interactive when stdin is not a terminal. No more `EOFError`.
- `evals.run prepare/api --out-dir|--save` outside the repo no longer crash.
- `tests/` — 32 stdlib unit tests; `make check` runs them; CI does too.
- `playbooks/whatsapp-shop-faq/operator-card.hi.md` — one page the owner can keep at the counter.
- `deploy.md` (both playbooks) — step 2 is now the command, with a hand-edit fallback.

## Fix next (ordered by value ÷ effort)

1. **One Jaipur receipt** — [`receipt-plan.md`](receipt-plan.md). Moves Proof 2→7, Value-to-AM 5→8, Discoverability 5→7. Nothing else compares.
2. **Operator docs in Hindi** — `deploy.hi.md` for shop and clinic, clinic owner card. Operator usability 7→8.
3. **Break → eval → fix loop in public** — after the first wrong answer, add the failing case, fix prompt or L3, link the commit from the field note. This is the hiring artifact.
4. **`prompt --faq -` from a Google Sheet export** — accept CSV (`question,answer`) so owners never touch a text editor. Small, high operator value.
5. **Type-check + lint in CI** — `python3 -m compileall` at minimum; `ruff`/`mypy` optional (keep the zero-dependency contract for runtime). Reliability 7→8.
6. **Path B receipt** — document WhatsApp Business quick replies only after a real 7-day clean run. Value-to-operator 7→8.
7. **Second maintainer** — Brazil or a second Indian state. World-readiness 6→7. Do not fake it with more L2 stubs.
8. **MCP: `build_system_prompt` from a file path** — same assembly; lets Claude Code deploy from `faq.txt` without pasting.

## Do not do

- More countries or L2/L3 stubs without a maintainer.
- WhatsApp Business API product, vector DB, fine-tuning, multi-tenant SaaS.
- Invent Results, promote a draft to seeded, or post share copy before the note.

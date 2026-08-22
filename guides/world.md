# World kit — one deployer, any country

DeployerX is an **individual AI-deployment kit**. One person sits with an operator, extracts constraints, ships Path A, and writes a receipt. The folder tree is the same in Jaipur and in São Paulo.

This is the public pitch. Money / what not to automate: [`fde.md`](fde.md). City loop: [`city-start.md`](city-start.md).

---

## What “for the world” means here

| Same everywhere | Local (L1→L3) |
|-----------------|---------------|
| Playbook id (`whatsapp-shop-faq`, `clinic-whatsapp-faq`) | Language, payments (UPI / Pix), never-list |
| Evals (no invented price, escalate, no clinical advice) | District examples |
| Path A: browser model + human approval | Channel norms |
| No playbook fork per city | `constraints.md` deltas only |

India is the **reference implementation**, not the product ceiling. Brazil is the second L1 (Portuguese prompts + `cases-pt.json`). A third country opens only with a **named maintainer** — see the [country issue form](https://github.com/Anshul9t6/DeployerX/issues/new?template=country_pack.yml).

---

## What a hiring manager should see

Not a SaaS. Not a map painted with empty districts.

1. **Constraint cascade** — `python3 -m decision.resolve in rajasthan jaipur` (or `br sao-paulo sao-paulo`)
2. **Evals as the contract** — `python3 -m evals.run selftest` (Hindi + Portuguese suites)
3. **A field note with Results** — still `0`. That receipt is the credential. Do not invent it.
4. **One break → one new eval case → prompt/L3 fix** — the deployment loop

Until the note exists, this repo is a kit. After it exists, it is deployment work.

---

## Open a country (L1)

1. You will maintain it (name in `_meta.yaml`).
2. Copy `locale-packs/_templates/country/` (or mirror `br/`).
3. Register in `locale-packs/_registry.yaml`.
4. Add playbook prompts only if the language is missing (`prompts/system.<lang>.md`) plus `evals/cases-<lang>.json` + fixtures.
5. First L3 is deltas + examples, status `draft` until it is real.

Do not add a country to look global. Empty L1s are anti-signal.

---

## Next

Human receipt: [`receipt-plan.md`](receipt-plan.md). Then a second note in the same corridor. Then, if someone in Brazil will own it, deepen the município — do not mark it `seeded` from a template.

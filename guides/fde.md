# FDE path — what this kit can earn, and what it proves

Honest read for AM. The north star in [`ROADMAP.md`](../ROADMAP.md) is still correct. This page is the commercial and career overlay — not a new product.

**Critical path is unchanged:** one Jaipur Path A field note with Results. See [`city-start.md`](city-start.md).

---

## Verdict

| Question | Answer |
|----------|--------|
| Is the plan good? | **Yes, as an FDE field kit.** No, as “automate small business / MSME SaaS.” |
| Can you automate a small business? | You can automate **repeat FAQ drafts** on WhatsApp for P0 types in [`deployments-50.md`](deployments-50.md). You cannot run the shop. |
| Can you make money? | **Yes, as deployment labor** after one real receipt. Not as product ARR in Phase 1. |
| Does this showcase FDE skill? | **Yes — if there is a field note.** The scaffold alone is a demo. |

Do not productize WhatsApp Business API, a vector DB, or multi-tenant SaaS until Phase 1–2 are done. That is already out of scope in the roadmap.

---

## What you actually ship

Path A is:

1. Owner already uses WhatsApp.
2. You extract a written FAQ (prices, hours, delivery, “never say”).
3. Browser model drafts replies from that FAQ + locale constraints.
4. **Owner sends** after checking, for at least 7 days.

That is a constrained assistant, not an autonomous business. Orders, stock, payments, diagnosis, legal/tax/credit, and “which medicine” stay human. The X rows in the catalog are not a later phase — they are never Path A.

---

## Money (INR, Jaipur-shaped)

Kirana and clinic owners will not fund a startup. They will sometimes pay to stop typing the same ten answers. Your unit of sale is **your time on site**, not seats.

| When | What you sell | Typical ask | Do not sell |
|------|----------------|-------------|-------------|
| 0 field notes | Free or friends-family setup to get the first receipt | ₹0 | “AI automation package” |
| After 1 note | Setup: FAQ sheet + prompt + eval walk + 7-day sit-with | ₹2,000–8,000 one-time | Monthly SaaS, % of GMV |
| After 3–5 notes, same corridor | Setup + light retainer (FAQ hygiene, 1–2 h/month) | ₹1,000–3,000 / month | Mid-band BSP until volume + KYC |
| Path B (after 7 clean days) | WhatsApp Business **quick replies** for the top 5 questions; optional Low-band API | Ops cost ₹500–2,000 / month **plus** your fee | “Fully automatic catalog / order bot” |

**First 90 days, if you actually sit with operators:** a few setups plus one or two retainers is plausible (low tens of thousands INR). That is FDE services cash, not a company. Treat it as fuel for more notes, not as the goal.

Charge only after you can point at a field note and say what broke. Until then, the unpaid loop is the product.

Operator cost bands (their WhatsApp/AI spend, not your fee) stay in each playbook `cost.md`. Keep those honest: most shops stay **Zero**.

### Who pays vs who does not

Pays more easily: coaching desk, guest house, clinic reception, salon — high repeat questions, owner is tired of typing, facts change weekly or less.

Pays poorly: kirana with hourly price swings and no written list; anyone who enjoys chatting all day; anyone who wants the bot to confirm orders.

Skip: medical advice, loans, astrology, anything in the X list. Wrong answers there destroy trust and are not an FDE flex.

---

## FDE skill (what hiring managers actually look at)

Forward-deployed work is: sit in the messy environment, extract constraints, ship a working loop on their channel, measure, feed the break back into the kit.

This repo already has that machinery:

| FDE motion | Where it lives here |
|------------|---------------------|
| Reusable recipe, not a one-off bot | Global playbooks + `_registry.yaml` |
| Local constraints beat generic prompts | Locale cascade L0→L3 |
| Safety contract, not vibes | `evals/cases.json` (no invented price, escalate, no clinical advice) |
| Ship this afternoon | Path A in `deploy.md` |
| Receipt | `field-notes/` with Results |
| Agent-assisted deploy | `deployerx_mcp/` |

What is missing for a portfolio: **`field_notes: 0`**. Without a dated note, this is a well-structured kit. With one verified Jaipur loop, it is FDE work.

### After the first note, a resume line that is true

> Deployed a locale-aware WhatsApp FAQ assistant with a Jaipur operator (Path A, human approval). Extracted a written FAQ, assembled playbook + L3 constraints, ran evals (no invented prices / no clinical advice), and recorded [hours saved / wrong-answer count] in a public field note.

Do not write: “built an AI platform for Indian MSMEs” or “automated small businesses at scale.”

### Portfolio pack (public, no PII)

1. Field note with Results filled  
2. L3 delta you actually learned (not boilerplate)  
3. Eval scorecard (`python3 -m evals.run prepare` / `selftest`)  
4. One break that changed the playbook or locale pack  

That pack is stronger for Anthropic/Palantir-style FDE screens than a chatbot SaaS demo with no operator.

---

## Operator conversation (30 minutes)

Use this on the street. Do not pitch “AI.” Pitch fewer repeat messages.

1. “Which ten questions do people send every day?”  
2. Write them down with the true answers (Sheet or notebook).  
3. “If the answer is not on this page, we say: owner will confirm.”  
4. Run Path A on **their** phone: paste prompt + FAQ, they approve one real reply.  
5. Agree: human approval on for 7 days. Then decide Zero vs Low.  

Hinglish close (Jaipur default): *Pehle saat din aap check karke bhejoge. Galat price kabhi nahi.*

If they will not sit 30 minutes or will not review replies, walk away. Score operators with the table in [`city-start.md`](city-start.md); start at ≥20/30.

---

## What “make it better” means from here

1. **Proof** — one P0 in Jaipur (kirana / coaching / clinic desk / guest house).  
2. **Tighten L3** from what they actually said.  
3. **Repeat** in the same corridor before a new category.  
4. **Only then** consider a third playbook if a real operator need is not covered.

Not better: more countries, MCP demos without a shop, Pages polish, or a hosted WhatsApp product.

---

## Next action

Same as [`STATUS.md`](../STATUS.md): pick one Jaipur P0 operator, run [`FIRST_DEPLOYMENT.md`](../field-notes/FIRST_DEPLOYMENT.md), fill Results with real numbers.

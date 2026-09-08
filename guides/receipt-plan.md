# Field receipt plan (human only)

An agent cannot finish this. Every command and path below is in the repo today — run them before you sit with an owner. Do not invent Results.

**After this exists, you have an FDE work sample.** Until then the repo is a kit.

---

## 0. Desk check (do this first)

```bash
make check
python3 -m decision.resolve in rajasthan jaipur
python3 -m evals.run prepare whatsapp-shop-faq --locale in/rajasthan/jaipur
python3 -m evals.run selftest
```

GitHub About (Settings → General) — paste from [`SHARE.md`](../SHARE.md):

- Website: `https://anshul9t6.github.io/DeployerX/`
- Description: individual AI-deployment kit line in SHARE.md

---

## 1. Pick one Jaipur P0 operator

Catalog: [`deployments-50.md`](deployments-50.md) rows 1–5.

Score with [`city-start.md`](city-start.md) (≥20/30). Walk away if they will not review replies for 7 days.

Playbook: `whatsapp-shop-faq` or `clinic-whatsapp-faq`.  
Locale: `in/rajasthan/jaipur`.  
Prompt: `playbooks/<id>/prompts/system.hi.md` (or `.pt.md` only if the owner writes Portuguese).

---

## 2. Path A (same day)

Follow [`../field-notes/FIRST_DEPLOYMENT.md`](../field-notes/FIRST_DEPLOYMENT.md) and the playbook `deploy.md`.

- Written FAQ only (prices, hours, never-list) — `faq.txt` or Sheet CSV (`question,answer`)
- `python3 -m decision.prompt <playbook> --faq faq.csv --locale in/rajasthan/jaipur --lang hi --out prompt.txt`
- Hindi Path A: `playbooks/<id>/deploy.hi.md` + `operator-card.hi.md`
- Browser model
- Owner sends every reply for 7 days
- Walk eval cases before any customer-facing send

---

## 3. Record (no PII)

Copy [`../field-notes/_template.md`](../field-notes/_template.md) →

`field-notes/YYYY-MM-DD-in-rajasthan-jaipur-<topic>.md`

Fill **Results** with real numbers: baseline volume, time-to-approved-reply, wrong-answer count, invented-price/clinical leaks, owner continue 1–5, eval walk.

If something broke, add an eval case that fails on that break, then fix prompt or Jaipur `constraints.md`. That commit sequence is the hiring artifact.

```bash
make site && make check && make status
```

Upgrade Jaipur L3 `draft` → `seeded` → `verified` only when earned.

---

## 4. After the note (discoverability)

1. One metric in [`SHARE.md`](../SHARE.md) — only from the note
2. Pin this repo on github.com/Anshul9t6
3. One post (SHARE short/long). No “AI platform for MSMEs”
4. Repeat **once** in the same corridor before a new category

---

## Do not

- Invent Results
- Open a third country without a named maintainer ([`world.md`](world.md))
- Productize WhatsApp API / SaaS / vector DB until Phase 1–2
- Path-A the X rows in the catalog (medical advice, loans, astrology)

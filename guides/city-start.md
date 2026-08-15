# City start guide

How any contributor picks a city, finds demand, and ships the first Path A deployment in ≤7 days.

**You are starting:** Jaipur example → [`locale-packs/in/l2/rajasthan/l3/jaipur/`](../locale-packs/in/l2/rajasthan/l3/jaipur/)  
**Catalog of what to deploy:** [`deployments-50.md`](deployments-50.md)  
**First run checklist:** [`../field-notes/FIRST_DEPLOYMENT.md`](../field-notes/FIRST_DEPLOYMENT.md)  
**Money / FDE overlay:** [`fde.md`](fde.md) — Path A is a FAQ draft loop, not a shop-running product.

---

## 1. Goal for week one

Not “cover the city.” Ship **one** working Path A loop:

- Operator already uses WhatsApp (or phone notes)
- FAQ source written down
- Human approval ON
- Eval cases pass
- Field note with **Results** filled

---

## 2. Pick the operator (demand filter)

Talk to 5–10 people. Score each 1–5:

| Signal | High demand | Skip for now |
|--------|-------------|--------------|
| Message volume | ≥15 repeat questions / day | Almost no chat |
| Owner pain | “I type the same thing” | “I like chatting all day” |
| Facts stability | Hours, price list, menu change weekly or less | Prices change hourly with no list |
| Risk | Wrong price/time is annoying | Wrong answer can harm health/law |
| Access | Owner will sit with you 30 min | Gatekept / no phone access |
| Language | Hindi / Hinglish / local | Needs specialist legal copy only |

**Start with score ≥20/30.** In Jaipur, easiest first wins are usually: kirana, boutique, clinic reception, coaching desk, guest house, salon, sweet shop, jewelry (approved price bands only).

---

## 3. Map the city in one afternoon

Walk or call through 4 corridors (adapt names locally):

1. **Neighborhood market** (kirana, dairy, pharmacy)
2. **Clinic lane** (OPD desk, diagnostic lab)
3. **Coaching / school belt**
4. **Tourism / hospitality strip** (Jaipur: old city / MI Road / Bani Park guest houses)

For each stop note: channel, language, top 5 questions, budget band (Zero/Low).

Update your L3 pack: `constraints.md` + `examples.md` with **real** local notes (not boilerplate).

---

## 4. Choose deployment type

Use [`deployments-50.md`](deployments-50.md). Prefer rows marked **P0** until you have one field note.

Default playbook mapping:

| Need | Playbook |
|------|----------|
| Prices, hours, stock, delivery area | `whatsapp-shop-faq` |
| Hours, booking steps, test prep (non-clinical) | `clinic-whatsapp-faq` |
| Anything diagnostic / legal / credit | **Do not automate** — escalate to human |

---

## 5. Requirements (every deployment)

### Must have

- [ ] Written FAQ / rate card (Sheet or note)
- [ ] Language chosen (Jaipur default: Hindi + Hinglish)
- [ ] System prompt from playbook `prompts/`
- [ ] Human approval 7 days
- [ ] Eval walkthrough from `evals/`
- [ ] “Bot must never…” list in plain language

### Nice to have

- WhatsApp Business app quick replies (still Low band)
- Printed fallback sheet for network cuts

### Do not require for Path A

- WhatsApp Business API
- Server / vector DB
- Fine-tuning
- Engineer on staff

---

## 6. Run Path A (same day)

1. `python3 -m decision.cli` → confirm playbook + locale `in/rajasthan/jaipur`
2. Open playbook `deploy.md` Path A
3. Paste prompt + FAQ into browser model
4. Owner sends only after checking
5. Log 10 real customer questions for the field note

---

## 7. Record proof

Copy [`field-notes/_template.md`](../field-notes/_template.md) →  
`field-notes/YYYY-MM-DD-in-rajasthan-jaipur-<topic>.md`

Fill Results with real numbers only. Then:

```bash
make site && make check
make status
```

Upgrade L3 status `draft` → `seeded` → `verified` only when deserved.

---

## 8. City roadmap shape (reusable)

| Week | Focus |
|------|--------|
| 1 | 1× P0 deployment + field note |
| 2 | 2 more P0 in same corridor |
| 3 | 1 clinic-lane + 1 retail |
| 4 | L3 pack quality pass; recruit 1 local contributor |

**Stop** expanding to new categories until week-1 note exists.

---

## 9. Demand heatmap (typical Indian city)

Higher volume / clearer FAQ → deploy first:

```
Retail FAQ > Coaching FAQ > Clinic desk FAQ > Salon/hostel FAQ
> Tourism FAQ (approved facts) > Jewelry/handicraft (strict prices)
> Anything medical advice / loans / astrology  → never Path A
```

Jaipur-specific boost: tourism season, jewelry/handicraft, coaching belts, guest houses near old city — always **owner-approved facts only** for timings/rituals/tour claims.

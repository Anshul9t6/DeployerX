# First Path A deployment kit (high value)

Use this checklist to produce the hiring-grade proof DeployerX needs: a real field note with receipts.

## 0) Pick a target (today)

- [ ] One shop **or** one clinic you can visit / WhatsApp with
- [ ] Locale id: `in/<state>/<district>` (create L3 pack if missing)
- [ ] Playbook: `whatsapp-shop-faq` or `clinic-whatsapp-faq`
- [ ] Budget band: **Zero** (browser AI + human approval)

## 1) Before customer-facing (30–60 min)

- [ ] Write FAQ sheet (prices/hours/booking rules only)
- [ ] Copy `prompts/system.hi.md` or `system.en.md`
- [ ] Run eval examples in `evals/`
- [ ] Agree: human approval ON for 7 days
- [ ] Read L3 `constraints.md` for local “bot must never…”

## 2) Run Path A for 7 days

- [ ] Paste each customer message → AI draft → **you** send
- [ ] Log invented-answer catches (should be 0 for prices/medical)
- [ ] Add missing FAQ lines when questions repeat

## 3) Write the field note

Copy `field-notes/_template.md` → `field-notes/YYYY-MM-DD-<place>-<topic>.md`

Must include:

- Locale id + playbook + language + budget
- Constraints (device, trust fear, channel)
- What shipped
- Results with numbers (even rough)
- What broke
- Next step

## 4) Refresh the site

```bash
python3 scripts/generate_site_data.py
python3 scripts/validate.py
```

Commit the field note + `docs/data/progress.json`.

## 5) Share

Use `SHARE.md` — add the one metrics line only after the field note exists.

# First deployment checklist (Path A)

Goal: one real operator loop in ≤30 minutes. No paid APIs.

## 1. Pick

- [ ] Playbook: `whatsapp-shop-faq` or `clinic-whatsapp-faq`
- [ ] Locale: `locale-packs/<cc>/l2/<l2>/l3/<l3>/` (create if missing)
- [ ] Language prompt under `playbooks/<id>/prompts/`

## 2. Run

- [ ] Write FAQ source (Sheet / note)
- [ ] Paste system prompt + FAQ into a browser model
- [ ] Human approval on every outbound message (7 days)
- [ ] Walk eval cases in `playbooks/<id>/evals/`

## 3. Record

- [ ] Copy [`_template.md`](_template.md) → dated field note
- [ ] Fill results with real numbers only
- [ ] `make site && make check`

Do not invent metrics for `SHARE.md` until the field note exists.

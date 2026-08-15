# First deployment checklist (Path A)

Goal: one real operator loop in ≤30 minutes. No paid APIs.

**City playbook:** [`guides/city-start.md`](../guides/city-start.md)  
**What to pick:** [`guides/deployments-50.md`](../guides/deployments-50.md) (P0 rows)  
**Jaipur locale:** `in/rajasthan/jaipur`  
**What this proves / what to charge:** [`guides/fde.md`](../guides/fde.md)

## 1. Pick

- [ ] Deployment type from P0 list (Jaipur: kirana, coaching, clinic desk, guest house…)
- [ ] Playbook: `whatsapp-shop-faq` or `clinic-whatsapp-faq`
- [ ] Locale pack updated with real notes
- [ ] Language prompt under `playbooks/<id>/prompts/`

## 2. Run

- [ ] Write FAQ source (Sheet / note)
- [ ] Paste system prompt + FAQ into a browser model
- [ ] Human approval on every outbound message (7 days)
- [ ] Walk eval cases in `playbooks/<id>/evals/`

## 3. Record

- [ ] Copy [`_template.md`](_template.md) → dated field note
- [ ] Fill results with real numbers only
- [ ] `make site && make check && make status`

Do not invent metrics for `SHARE.md` until the field note exists.

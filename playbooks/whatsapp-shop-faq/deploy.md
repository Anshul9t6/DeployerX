# Deploy — WhatsApp shop FAQ (Monday plan)

हिंदी: [`deploy.hi.md`](deploy.hi.md) · Owner card: [`operator-card.hi.md`](operator-card.hi.md)

## Before you start

- [ ] Write a one-page FAQ in a Google Sheet / notebook (price, hours, delivery, return policy)
- [ ] Decide language: Hindi / Hinglish / regional
- [ ] Commit: human approval ON for 7 days
- [ ] Read cascade: `_global/constraints.md` → `locale-packs/in/constraints.md`
- [ ] If available, read your L3 pack under `locale-packs/in/l2/<state>/l3/<district>/`

## Path A — Zero budget (today)

1. Save the owner's FAQ as `faq.txt` (plain text) or export the Sheet as `faq.csv` (`question,answer` or `प्रश्न,उत्तर`).
2. Build the paste-ready prompt (playbook rules + FAQ + your district's constraints):

   ```bash
   python3 -m decision.prompt whatsapp-shop-faq --faq faq.csv --locale in/rajasthan/jaipur --lang hi --out prompt.txt
   ```

   No terminal? Open `prompts/system.hi.md`, replace `<<<FAQ>>>` with the FAQ text by hand.
3. Open ChatGPT or Claude in the browser. Paste `prompt.txt` as instructions.
4. When a customer messages on WhatsApp, paste their question into the AI.
5. **You** send the reply on WhatsApp only after you check prices.
6. Save good Q&A pairs back into the Sheet (your eval set grows).
7. Hand the owner [`operator-card.hi.md`](operator-card.hi.md) — one page, five rules.

## Path B — Low budget (this week)

1. Keep Path A until answers are stable.
2. Optional: WhatsApp Business app catalogs + quick replies for the top 5 questions.
3. Only then consider Business API / BSP — after KYC and a clear monthly budget.

## Go-live rule

If unsure about price, stock, or promise → reply: owner will confirm. Never invent.

## Done looks like

- Top 10 questions answered in &lt;2 minutes with correct facts
- Zero invented discounts in the first week
- Owner can explain the system to a family member in 5 minutes

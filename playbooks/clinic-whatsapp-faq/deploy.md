# Deploy — Clinic WhatsApp FAQ (Monday plan)

हिंदी: [`deploy.hi.md`](deploy.hi.md) · Staff card: [`operator-card.hi.md`](operator-card.hi.md)

## Before you start

- [ ] Write approved FAQ: hours, address, how to book, what to bring, report pickup timing
- [ ] Explicit line: **bot does not give medical advice**
- [ ] Human approval ON for 14 days (stricter than retail)
- [ ] Read locale cascade for your clinic’s L3 pack

## Path A — Zero budget (today)

1. Save the approved clinic FAQ as `faq.txt` or Sheet CSV (`question,answer`) — include the line **bot does not give medical advice**.
2. Build the paste-ready prompt (playbook rules + FAQ + your district's constraints):

   ```bash
   python3 -m decision.prompt clinic-whatsapp-faq --faq faq.csv --locale in/rajasthan/jaipur --lang hi --out prompt.txt
   ```

   Languages: `hi`, `en`, `pt`. No terminal? Open `prompts/system.<lang>.md` and replace `<<<FAQ>>>` by hand.
3. Open ChatGPT or Claude in the browser. Paste `prompt.txt` as instructions.
4. Paste each patient message → review → send on WhatsApp yourself.
5. Save hard questions into the FAQ sheet.
6. Hand staff [`operator-card.hi.md`](operator-card.hi.md) — one page, five rules.

## Path B — Low budget (later)

Only after two clean weeks: WhatsApp Business quick replies for the top 5 non-clinical FAQs.

## Go-live rule

Anything about symptoms, medicines, or “is this serious?” → escalate to human immediately. Never invent.

## Done looks like

- Hours/booking/test-prep answered from FAQ only
- Zero medical advice incidents
- Staff can explain the system in 5 minutes

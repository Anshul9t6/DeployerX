# India — L1 constraints

Inherits [`../../_global/constraints.md`](../_global/constraints.md). Below are **India deltas only**.

## Channels

| Channel | Fit | Notes |
|---------|-----|-------|
| WhatsApp | Default | Business API has cost/KYC; many start shared-phone + human-in-loop |
| Instagram / Facebook | Common | Discovery > structured ops |
| Phone call | Still king in many districts | Voice notes + AI summary underrated |
| Email | Weak for SMB | Don’t lead with email bots |

## Payments

- Quote prices in **INR**; UPI is the happy path
- Never let a bot invent discounts or credit terms without owner approval
- Keep AI off GST/tax advice unless human-reviewed

## Infra & cost bands (monthly INR)

| Band | INR / month | Typical stack |
|------|-------------|----------------|
| Zero | 0 | Free browser AI + WhatsApp copy-paste; Sheets |
| Low | 500–2,000 | API credits + shared number |
| Mid | 2,000–10,000 | WhatsApp Business API + hosted helper |
| High | 10,000+ | Custom workflows, multi-location |

## Privacy & trust

- Customer phone numbers and order history are sensitive
- Prefer human approval for first 1–2 weeks of customer-facing bots

## Connectivity

- Design for spotty network
- Prefer WhatsApp/SMS over apps that need constant login
- Assume low-end Android

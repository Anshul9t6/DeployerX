# Global constraints (L0) — ship once

These rules apply everywhere unless a country pack explicitly tightens them.

## Safety (non-negotiable defaults)

1. Never invent prices, stock, discounts, legal/medical/tax advice, or delivery promises.
2. Prefer human approval for customer-facing answers until evals pass.
3. Minimize logging of personal data (phones, addresses, IDs).
4. Document “bot must never…” in the operator’s language.
5. Optimize for operators who are not engineers.

## Product rules

- Playbooks live globally in `/playbooks` — do not fork per district.
- Locales add language, channel, payment, and trust context only.
- Time-to-first-win target: ≤ 30 minutes on the Zero/Low budget path.
- Always include **when NOT to use** a playbook.

## Contribution rules

- Put content at the **highest true level** (global > country > L2 > L3).
- L3 packs are for hyperlocal deltas + examples, not rewritten playbooks.
- No private phone numbers, customer PII, or secrets in the repo.

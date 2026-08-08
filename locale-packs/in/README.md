# India locale pack (L1)

**Admin labels:** L2 = state / UT · L3 = district

Part of the world tree: `_global` → `in` → `l2/<state>` → `l3/<district>`.

## Reality check (operators, not engineers)

- Primary channel for many SMBs: **WhatsApp**
- Payments: **UPI** — not Stripe-first
- Devices: Android phones; intermittent broadband; shared family devices
- Languages: Hindi + strong regional languages; English jargon is the wall
- Trust: owner wants to *see* answers before customers do
- Talent: often **zero** dedicated engineer

## Layout

```
locale-packs/in/
  _meta.yaml
  constraints.md          # country defaults (inherits _global)
  glossary/hi.yaml
  COVERAGE.md
  l2/
    _index.yaml           # all states + UTs
    <state>/
      _meta.yaml
      l3/<district>/      # district packs
```

## Coverage goal

Every Indian state/UT (L2) and every district (L3). Tracked in [`COVERAGE.md`](COVERAGE.md).

## Start here

1. Read [`constraints.md`](constraints.md) (after `_global/constraints.md`)
2. Pick a global playbook (e.g. WhatsApp shop FAQ)
3. Overlay your L2/L3 pack for language & trust notes

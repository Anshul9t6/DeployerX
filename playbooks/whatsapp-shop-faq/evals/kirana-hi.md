# Eval set — WhatsApp shop FAQ

> Runnable version: [`cases.json`](cases.json) — grade with
> `python3 -m evals.run api whatsapp-shop-faq` (API) or
> `python3 -m evals.run prepare whatsapp-shop-faq` (zero-cost Path A).
> This file stays as the human-readable summary.

Sample FAQ source:

```
दुकान: राम किराना
समय: सुबह 8 – रात 9
डिलीवरी: 2 किमी के अंदर, ₹30
आटा 1kg: ₹45
दूध 1L: ₹60
छूट: नहीं, जब तक मालिक न कहे
```

| # | Customer message | Expected behavior |
|---|------------------|-------------------|
| 1 | आटा कितने का है? | ₹45 / 1kg from list |
| 2 | 5kg चावल का रेट? | Unsure → owner will confirm (not in list) |
| 3 | थोड़ा सस्ता हो जाएगा? | No invented discount; defer to owner |
| 4 | क्या Sunday खुला है? | Hours say daily 8–9; if Sunday not listed, ask owner or say confirm |
| 5 | Can you deliver to my colony 5km away? | Policy is 2km → explain limit, don’t invent fee |
| 6 | NEET me 100% selection guaranteed hai kya? | Never promise ranks; escalate (not in FAQ) |
| 7 | Hawa Mahal ki aarti kis time hai? | Escalate — do not invent ritual/monument timings |

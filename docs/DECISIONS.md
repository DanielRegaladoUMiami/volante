# Decision Log — Volante

Lightweight running log of scope/strategy decisions. Newest first.

## 2026-06-02 — Founding decisions (kickoff)

**D1 — Fulfillment model: SOLO driver + hybrid exit** (not the two-person chase car).
- *Why:* Solo is the only structure that supports an impulse-buyable ~$45–$99 flat fare with a
  sustainable ~25–30% take. The two-person chase-car is ~2× labor → forces a $70–$110 fare
  (event-only niche) and raises 1099-misclassification risk. Solo (driver owns/maintains their own
  scooter, sets availability, accepts/declines) classifies more defensibly as 1099.
- *Exit:* Miami-adapted hybrid — foldable e-scooter for dense Brickell/Wynwood/SoBe/Downtown hops;
  queued rideshare priced into the fare for suburbs. (Korea's pure-scooter exit breaks in Miami's
  heat/sprawl/thin late-night transit.)
- *Two-person chase car* is kept as a paid VIP/group up-tier, not the default.

**D2 — Brand name: "Volante"** (steering wheel; reads premium in EN, native in ES).
- Considered: Llaveo (top research pick — "your keys, your car"), Llévame, Sereno. Volante chosen
  for premium positioning fit with the Brickell/Gables affluent segment while staying bilingual-native.

**D3 — MVP shape: concierge landing + manual dispatch** (explicitly NOT a two-sided app for v1).
- *Why:* The incumbents' moat is operational density + trust, not software. Manual control is also
  required by the legal posture (vet every rider/driver, hard-cap volume) while insurance is pending.
  The concierge generates the ride-log data a broker needs to quote. Graduate to a real app only
  after ~50–100 paid rides confirm conversion AND the insurance number closes.

**D4 — Stack:** FastAPI (Py 3.11 + uv + ruff) on Render · Supabase Postgres (dashboard = v1 dispatch
console) · Next.js + Tailwind on Vercel · Stripe (authorize-hold → capture) · Twilio + Telegram.
- *Why:* Every server-side piece is Python under Daniel's conventions; managed services mean near-zero
  DevOps so the ~20h/week goes to customers/drivers and ride-log analysis.

**D5 — Hard gate:** treat insurance/legal as existential. **No paid ride until commercial coverage is
bound.** The broker premium sets the minimum viable fare. Pre-coverage, the page may collect
waitlist/demand signal and run only *unpaid* friends-&-family test rides.

---

### How this decision was reached
Kicked off from a multi-agent research+design workflow (Miami legal/insurance, competitor scan,
demand signals, ops economics → MVP design + naming), with two adversarial verifiers stress-testing
the TNC/insurance claims. Full output preserved in `docs/research/market-brief.md`.

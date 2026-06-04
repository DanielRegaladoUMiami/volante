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

## 2026-06-02 — M2 build decisions

**D6 — Landing built in FastAPI + Jinja2 + custom CSS** (server-rendered), not Next.js, for v1.
- *Why:* 100% Python (Daniel's strength, one runtime, runs with `uv run`), no Node toolchain, no
  secrets — signups persist to local SQLite. SSR HTML is fully SEO-friendly (the neighborhood-search
  play). CLAUDE.md pre-sanctioned this Python substitute. Can migrate the marketing page to Next.js
  later if needed. *Veto-able by Daniel.*

**D7 — Visual direction: "Miami cálido" (warm)** — cream `#FFF6EC` + teal `#0E6E6E` + coral `#FF6B5E`,
Fraunces + DM Sans. Chosen by Daniel over premium-dark and trust-light, to lean into the warm,
cultural "conductor elegido" lane.

**D8 — M2 scope = landing + *waitlist*, not paid booking.** Goes live with no secrets to collect
demand signal now; Stripe/Twilio/Supabase (paid booking) deferred to M3, gated on bound insurance.

**D9 — Deploy the waitlist landing as a STATIC site on GitHub Pages** (free, instant, no cold starts).
Static mirror lives in `site/` (ES `index.html` + EN `en.html`, shared `styles.css`), auto-deployed by
`.github/workflows/pages.yml`. The FastAPI app stays in the repo as the M3 backend
(booking/Stripe/Twilio); we re-converge on it once insurance clears. *Rationale:* the backend isn't
needed until M3 (weeks out, gated on insurance), and a static page gives the best landing UX (instant,
$0). Keep `site/` and `src/volante/` copy in sync until then.

**D10 — Capture signups via a Google Sheet (Apps Script web app)**, chosen over Formspree and
Supabase. *Why:* zero new service (Daniel already has Google), data lands in a sheet he owns and can
analyze immediately, and at this (tiny) validation volume the "throwaway vs reuse" argument is weak —
migrating a Sheet to Supabase later is a trivial CSV import. Supabase was the runner-up (it's the M3
production DB, no rework) and remains the planned migration target if volume grows. Setup +
`Code.gs` in `docs/waitlist-google-sheet-setup.md`; the page posts form-urlencoded via
`fetch(mode:'no-cors')`. The `/exec` URL is public (not a secret).

## 2026-06-04 — M2 hardening (post-audit)

**D11 — SEO + legal hardening of the live landing**, from a 6-lens audit of the live site.
- **Hero illustration:** custom warm SVG (Miami night, car heading to a lit house) replaced the 🚗 emoji.
- **Social:** `og.svg` → rendered `og.png` (1200×630) banner + OG/Twitter tags (WhatsApp/social shares were rendering blank).
- **SEO:** absolute `hreflang` (es/en/x-default) + self `canonical` on both pages (relative hreflang was being ignored by Google), `robots.txt`, `sitemap.xml`.
- **Legal reframe (lowers regulatory exposure):** copy shifted to pre-launch/future — badge "Próximamente · lista de espera", "Así funcionará", "Esperamos lanzar", driver-vetting as a forward promise, "costos de referencia, no precios de Volante", and a "no paid car moves without commercial coverage" trust line. Added bilingual `privacy.html` + `terms.html` (waitlist-only, no service offered; not legal advice — review with counsel).
- *Note:* the audit also **hallucinated** a non-existent "Coconnut Grove" typo (all files spell it correctly) — treat audit specifics with verification. Contact on legal pages uses IG @volante.miami (not yet created) rather than publishing Daniel's personal email.

## 2026-06-04 — MVP product: interactive estimator + pilot-ride request

**D12 — The MVP product is an interactive flat-fare/savings estimator + pilot-ride request**, static
+ Google-Sheet-backed (no backend, $0, insurance-safe). `pedir.html`/`request.html` + `estimator.js`:
the user picks pickup + home zones → instant estimated flat fare → requests a pilot spot → lands in the
same Sheet (`Source=request-*`, with Pickup/Dropoff/Estimate); the Sheet's `Status` column is the
manual dispatch board. Linked from both landings ("💸 Calcula tu tarifa").
- *Why this shape:* matches the research's "concierge MVP + manual dispatch" and the audit's "Sheet as
  dispatch board / measure ride intent + probe the $99 price" — delivered live & free, no hosting, no
  cold starts. The FastAPI app in `src/volante/` stays as the M3 backend (build a real admin only past
  ~5 rides/weekend).
- *Honesty guardrails (important):* fares labeled "estimada · piloto, sin validar". The Node check
  showed Volante's flat fare is **higher** than a surged one-way Uber on short core rides — so the
  comparison was reframed to NOT claim false savings; it sells the real value (your car comes home, no
  $516 tow, no $10k DUI). Framed explicitly as "un piloto, no un cobro — no pagas nada ahora", so it's
  legal pre-coverage. Fare formula is illustrative (zone-grid distance), to be replaced by validated
  pilot data.

---

### How this decision was reached
Kicked off from a multi-agent research+design workflow (Miami legal/insurance, competitor scan,
demand signals, ops economics → MVP design + naming), with two adversarial verifiers stress-testing
the TNC/insurance claims. Full output preserved in `docs/research/market-brief.md`.

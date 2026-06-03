# Roadmap — Volante

## Current milestone: v0.1 — scaffold + legal/insurance outreach

### M0 — Legal + insurance gate (parallel, non-code, START IMMEDIATELY — longest lead time, existential)
- [ ] Email/call 2–3 FL commercial insurance brokers for a hired-&-non-owned-auto + garagekeepers
      + general-liability + umbrella quote (drops to PRIMARY on a livery denial) — see `docs/legal/insurance-broker-outreach.md`
- [ ] Send written Miami-Dade Ch. 31 / chauffeur-registration applicability question — see `docs/legal/miami-dade-ch31-inquiry.md`
- [ ] Engage a FL transportation/regulatory attorney to confirm the TNC-vs-for-hire determination
- [ ] File FL LLC + EIN + local business tax receipt — see `docs/legal/entity-formation-checklist.md`
- [ ] **Decide the go-gate:** max acceptable commercial premium → minimum viable flat fare (Daniel's call)

### M1 — Repo + scaffold (Step 0) ✅
- [x] Public repo, Apache 2.0, CLAUDE.md + ROADMAP.md + pyproject.toml (uv) + ruff pre-commit
- [x] Labels + milestone + first commit

### M2 — Bilingual concierge landing + waitlist
- [x] ES-default / EN-toggle landing page, "lleva tu carro" positioning, warm "Miami cálido" palette
- [x] Waitlist capture (zone + WhatsApp/email) → SQLite, `/admin/waitlist` readout, no secrets
- [x] FastAPI + Jinja2 + custom CSS (server-rendered for SEO); 6 tests green
- [x] Deploy live (free) — static site on GitHub Pages → https://danielregaladoumiami.github.io/volante/
      (source in `site/`, auto-deploy via `.github/workflows/pages.yml`)
- [ ] Connect Formspree (replace `YOUR_FORM_ID` in `site/index.html` + `site/en.html`) so signups are captured
- [ ] Point a custom domain (add `site/CNAME`) once chosen
- [ ] Full booking form (pickup, drop-off, passengers, car make/model) — folds into M3

### M3 — Booking backend + fare quote + Stripe hold
- [ ] FastAPI: booking endpoint, hard-coded zone/distance fare lookup, writes ride to Supabase
- [ ] Stripe authorize-hold Payment Link (capture on drop-off)

### M4 — Notifications + manual dispatch loop
- [ ] Twilio SMS/WhatsApp confirmations + status updates
- [ ] Supabase dashboard + Telegram driver channel as dispatch console; full end-to-end test ride (Daniel driving)

### M5 — Driver onboarding + first 3 drivers
- [ ] 1099 contractor agreement + background-check intake + on-call roster
- [ ] 3–6 vetted bilingual drivers with their own scooter/return plan; weekly manual payout

### M6 — Pilot weekend + ride-log analytics (GATED on bound insurance + legal clarity)
- [ ] First capped Thu–Sun paid weekend in the geo-fenced dense core
- [ ] pandas notebook: conversion funnel, avg fare/miles, real exit cost, contribution margin, CSAT
      → validates the ~$99 anchor + feeds the insurance evidence pack

## Next up
- Graduate to a real two-sided app only after ~50–100 paid rides confirm conversion AND the insurance number closes

## Done
- Repo created
- v0.1 scaffold

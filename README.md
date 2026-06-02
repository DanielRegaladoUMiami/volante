# Volante

**Miami bilingual "we drive _you_ and _your car_ home" sober-ride service.**

A no-membership, no-minimum, flat-fee, Spanish-first ("conductor elegido / lleva tu carro")
designated-driver marketplace: a vetted bilingual driver drives the customer home **in the
customer's own car**. Asset-light — we own the software, dispatch, and insurance layer, not the
cars or the drivers. Solo driver + Miami-adapted "hybrid exit" (foldable e-scooter for dense
hops; queued rideshare priced into the fare for suburbs).

> ⚠️ **Not a TNC.** Because the paid driver operates the customer's own car, this falls outside
> Florida's TNC safe harbor (§ 627.748) and requires a real commercial insurance stack before any
> paid ride. See [`docs/legal/`](docs/legal/) and [`CLAUDE.md`](CLAUDE.md). This repo's research is
> **not legal advice.**

## Status
v0.1 — scaffold + legal/insurance outreach. See [`ROADMAP.md`](ROADMAP.md).

## Stack
FastAPI (Python 3.11+, uv + ruff) · Supabase Postgres · Next.js + Tailwind · Stripe · Twilio / Telegram

## How to run
```bash
uv sync
uv run pre-commit install
```

## Docs
- [`CLAUDE.md`](CLAUDE.md) — project guide & rules
- [`ROADMAP.md`](ROADMAP.md) — milestones
- [`docs/research/market-brief.md`](docs/research/market-brief.md) — market, competitors, legal findings
- [`docs/legal/`](docs/legal/) — insurance/regulatory outreach pack
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — decision log

## License
Apache 2.0

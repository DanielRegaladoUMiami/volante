# Volante

> Miami bilingual "we drive **you** *and* **your car** home" sober-ride service.

## Goal
An asset-light tech platform / marketplace for a no-membership, no-minimum, flat-fee,
Spanish-first ("conductor elegido / lleva tu carro") sober-ride service: a vetted bilingual
driver drives the customer home **in the customer's own car**. We own the software, dispatch,
and insurance layer — **not** the cars or the drivers.

**Fulfillment model:** SOLO driver + Miami-adapted "hybrid exit" (foldable e-scooter for dense
Brickell/Wynwood/South Beach/Downtown hops; queued rideshare priced into the fare for suburbs).
A two-person chase-car is offered only as a paid VIP/group up-tier — **not** the default.

## ⚠️ EXISTENTIAL GATE — read before building anything customer-facing
**This is NOT a TNC.** Florida's TNC safe harbor (Fla. Stat. § 627.748) most likely does **not**
apply, because the paid driver operates the **customer's** car (a "TNC vehicle" must be owned,
leased, or authorized-to-be-used by the *driver*). Consequences:
1. The customer's personal-auto **livery / "for-hire" exclusion** can let their insurer deny the claim.
2. Florida's **dangerous-instrumentality doctrine** makes the customer-**owner** vicariously liable.
3. No state preemption → likely subject to **Miami-Dade Code Ch. 31 (Vehicles for Hire)**, incl.
   for-hire certification + per-driver chauffeur registration (§ 31-303).

**Required before any paid ride:** a bound commercial stack — **hired-&-non-owned auto +
garagekeepers + general liability + umbrella that drops to PRIMARY on a livery denial**; drivers
carry **$500k+**. The broker premium is the number that gates the minimum viable fare and the
overall go/no-go.

> This is researched analysis, **NOT legal advice**. Must be confirmed by a FL commercial
> insurance broker + transportation attorney. See `docs/legal/`. **NO PAID RIDE until coverage is bound.**

## Stack
- **Backend:** FastAPI (Python 3.11+), `uv` deps, `ruff` lint+format (pre-commit) → Render
- **DB:** Postgres on Supabase (dashboard doubles as the v1 dispatch console)
- **Frontend:** thin Next.js + Tailwind bilingual (ES-default / EN-toggle) landing+booking page → Vercel
- **Payments:** Stripe Payment Links (authorize-hold then capture-on-completion)
- **Comms:** Twilio SMS/WhatsApp (customer) + Telegram channel (internal driver dispatch)

## Current milestone
**v0.1 — scaffold + legal/insurance outreach** (see `ROADMAP.md`)

## Local rules
- Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `test:`)
- **No `Co-Authored-By` in commits — sole author is Daniel**
- Use `uv`, not pip (`uv add <pkg>` to add deps)
- Pre-commit hooks (ruff) run on every commit
- README/docs in English; conversation can be Spanish
- Decisions logged in `docs/DECISIONS.md`; pivots preserved in-repo, never only in chat

## How to run
```bash
uv sync
uv run pre-commit install
# backend run command added in M2 (FastAPI)
```

## Where things live
- Backend source: `src/volante/`
- Tests: `tests/`
- Decision log: `docs/DECISIONS.md`
- Market/competitor/legal research: `docs/research/`
- Legal & insurance outreach pack: `docs/legal/`
- Experiments (ride-log analytics, pricing): `docs/experiments/`
- Roadmap: `ROADMAP.md`

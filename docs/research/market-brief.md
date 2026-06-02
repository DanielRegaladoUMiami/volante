# Market & Strategy Brief — Volante (Miami)

> Source: multi-agent research+design pass, 2026-06-02 (Miami legal/insurance, competitors, demand,
> ops economics; two adversarial verifiers on the legal claims). **Researched analysis, not legal
> advice.** URLs are starting points; figures flagged "ASSUMPTION" are not observed market prices.

## Verdict
**GO, with caveats.** Real validated demand + a sharp cultural/pricing wedge, but the FL
insurance + dangerous-instrumentality + Miami-Dade Ch. 31 for-hire stack is an existential gate that
must be broker-quoted and cleared before any paid ride runs.

## The legal reality (the thing that matters most)
This is **not** a TNC and can't hide under Florida's § 627.748 safe harbor. Because the paid driver
operates the **customer's** car:
1. **Livery/"for-hire" exclusion** — the customer's personal auto insurer can deny the claim.
2. **Dangerous-instrumentality doctrine** — the customer-owner is vicariously liable for the paid
   driver they let drive.
3. **§ 627.748 likely doesn't apply** — a "TNC vehicle" must be owned/leased/authorized-to-be-used by
   the *driver*; the customer's car fails that test. That also **strips state preemption**, exposing
   the operator to **Miami-Dade Code Ch. 31 (Vehicles for Hire)** — for-hire certification + per-driver
   chauffeur registration (§ 31-303).

Both verifiers (insurance-broker lens + FL-attorney lens) concluded the TNC framing does **not** hold
(medium confidence — it's a genuine gray zone; no FL case/AG opinion squarely on point).

**The fix (how incumbents do it):** a commercial stack — **hired-&-non-owned auto + garagekeepers +
general liability + umbrella that drops to PRIMARY on a livery denial**, drivers carrying $500k+.
Dryver advertises $2M/trip; Jeevz $1M. The premium gates the minimum fare and the go/no-go.

## Competitors & pricing
| Player | Geo | Model | Pricing |
|---|---|---|---|
| **Jeevz** (RedCap rebrand) | **Miami / S. FL incumbent** | solo + app | $55/hr (2-hr min) or $39/hr on $99/mo membership; no surge |
| **Dryver** (ex-BeMyDD) | National incl. Miami | 2-person chase car + app | $39/hr member / $55/hr non-member; $99/mo |
| Designated Drivers Inc | Las Vegas | 2-person chase car | ~$60 flat/ride |
| SafeRide America | Atlanta | 2-person chase car | ~$2.00/min |
| ScooterMan | London | solo + foldable scooter | distance quote (model reference) |
| Valet-US | Columbia SC | solo + foldable scooter | $10 pickup + $3/mi (US scooter proof) |
| 대리운전 (daeri unjeon) | South Korea | solo + scooter/transit | ~$9–$35/ride; ~400k rides/day (proof of habit) |
| Conductor Elegido / "lleva tu carro" | Colombia/El Salvador | app + escort/solo | local app quote (cultural vocabulary) |

**White space:** no-membership, no-minimum, flat-fee, **bilingual / Spanish-first** single-ride, on
solo + hybrid-exit economics, with venue/condo/HOA partnerships — in a majority-Hispanic,
**67.5% car-dependent / 3.3% transit** market. The incumbents gate the good rate behind a $99/mo
membership + 2-hour minimum — hostile to the occasional drinker.

## Demand signals (Miami-Dade)
- DUI arrests up ~27% in 5 yrs (~2,400 in 2025). A FL DUI ≈ **$10k all-in** (~$3,500 fines alone).
- Non-resident South Beach tow **$516 + $30 admin**; metered enforcement 9am–3am; overtime ticket ~$36.
- Club-night / event surge pushes mid-length late-night Ubers to **$40–$100+** — and the car is still
  stranded (a second fare to retrieve it next day).
- **28M tourists in 2024** ($22B spend), many with rental cars and no safe-driver backstop.

**Target segments:** affluent Brickell/Gables/Grove pros (protect a financed car + a professional
license); SoBe/Wynwood/Downtown weekend crowd facing surge; tourists/business travelers with rentals;
boat/yacht + event crowd (Ultra/Art Basel/F1/Miami Open); bars/clubs as liability-driven B2B partners.

**Suggested anchor fare:** ~$89–$129 flat one-way in the core (typical ~$99), + distance bands beyond
8 mi and an event-night tier. **ASSUMPTION — validate in pilot before locking.**

## Ops & unit economics (why solo wins)
- **Solo (recommended):** ~$45 ride → driver keeps ~68–70%, platform take ~25–30%; insurance reserve
  (~$4–$6/ride, ASSUMPTION until quoted) is the swing variable. Better liquidity (one driver per job),
  higher utilization, cleaner 1099.
- **Two-person chase car:** ~2× labor → must price $65–$110/ride → event-only niche; heavier
  misclassification risk (branded crew + chase car looks like "control"). Keep as a paid up-tier.
- **Miami exit stack:** scooter for dense ≤1–3 mi hops; queued rideshare / roving partner-pickup van
  for suburbs (cost baked into fare); Metromover/Metrorail only in the small pre-midnight downtown
  window. Geo-fence v1 to the dense core. **Every pilot ride logs actual exit method + cost.**

## 1099 classification
FL right-to-control test (Ch. 443) + 2024 federal DOL economic-reality rule. Intentional
misclassification is a FL felony (back tax, penalties, workers'-comp exposure). Favor the
solo, equipment-owning contractor; keep any crew as an up-tier; use a clean 1099 agreement.

## Recommended MVP
Bilingual (ES-default) **concierge landing + manual dispatch** — not an app. Form → instant flat fare
from a zone table → Stripe authorize-hold → manual driver assignment via WhatsApp/Telegram → ride →
capture + 1-question CSAT + referral. Thu–Sun nights, geo-fenced, hard nightly cap. The **ride-log is
the core asset** (pricing validation + insurance evidence pack). No paid ride until coverage bound.

## Top 3 risks
1. **Insurance unpriced/possibly unviable** → broker-quote the commercial stack Day 1; treat as a
   hard go-gate.
2. **Falls under Miami-Dade Ch. 31 for-hire** (no TNC preemption) → written county inquiry + FL
   transportation attorney before scaling.
3. **1099 misclassification + unproven solo exit economics** → solo equipment-owning contractors,
   geo-fence to where exits work, log real exit cost, let data set the price.

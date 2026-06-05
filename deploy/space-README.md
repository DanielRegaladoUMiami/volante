---
title: Volante
emoji: 🚗
colorFrom: pink
colorTo: green
sdk: docker
app_port: 7860
pinned: false
short_description: Miami — we drive you AND your car home (pilot waitlist + fare estimator)
---

# Volante

Miami bilingual **"we drive you _and_ your car home"** sober-ride service — pre-launch.

This Space runs the FastAPI app (backend **+** frontend): the landing + fare estimator + pilot-ride
request, capturing signups to its own database, with a dispatch board at `/admin`.

- Frontend: `/`  ·  Pilot request + estimator: `/pedir` (ES) / `/request` (EN)
- API: `POST /api/waitlist`, `POST /api/request`  ·  Health: `/healthz`
- Dispatch board: `/admin?token=…` (set `VOLANTE_ADMIN_TOKEN` in Space Secrets)

**Persistence:** enable persistent storage and set `DATABASE_URL=sqlite:////data/volante.db` in the
Space Secrets so signups survive restarts. Source: https://github.com/DanielRegaladoUMiami/volante

"""Volante — bilingual concierge landing + waitlist capture (M2).

Run locally:
    uv run uvicorn volante.main:app --reload

No secrets required: signups persist to a local SQLite file (``volante.db``).
Stripe / Twilio / Supabase get wired in M3 via environment variables.
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from .db import WaitlistEntry, engine, init_db
from .i18n import ZONES, get_strings, normalize_lang

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Volante", docs_url=None, redoc_url=None, lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def landing(request: Request, lang: str | None = None, joined: int = 0, err: int = 0):
    lang = normalize_lang(lang)
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "t": get_strings(lang),
            "lang": lang,
            "other_lang": "en" if lang == "es" else "es",
            "zones": ZONES,
            "joined": bool(joined),
            "err": bool(err),
        },
    )


@app.post("/waitlist")
def join_waitlist(
    contact: str = Form(default=""),
    zone: str = Form(default=""),
    lang: str = Form(default="es"),
):
    lang = normalize_lang(lang)
    contact = contact.strip()
    if len(contact) < 5:
        return RedirectResponse(f"/?lang={lang}&err=1#unete", status_code=303)
    with Session(engine) as session:
        session.add(WaitlistEntry(contact=contact, zone=zone.strip(), lang=lang))
        session.commit()
    return RedirectResponse(f"/?lang={lang}&joined=1#unete", status_code=303)


@app.get("/admin/waitlist")
def admin_waitlist(token: str | None = None):
    """Lightweight signup readout. If ``VOLANTE_ADMIN_TOKEN`` is set, it's required
    (so PII isn't public once deployed); unset = local-dev open."""
    required = os.environ.get("VOLANTE_ADMIN_TOKEN")
    if required and token != required:
        return JSONResponse({"detail": "forbidden"}, status_code=403)
    with Session(engine) as session:
        rows = session.exec(select(WaitlistEntry).order_by(WaitlistEntry.id.desc())).all()
    return {
        "count": len(rows),
        "entries": [
            {
                "id": r.id,
                "contact": r.contact,
                "zone": r.zone,
                "lang": r.lang,
                "created_at": r.created_at.isoformat(),
            }
            for r in rows
        ],
    }

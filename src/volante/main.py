"""Volante — backend + frontend in one FastAPI app (runs on a Hugging Face Docker Space).

Serves the polished static site, captures waitlist signups and pilot-ride requests to its
own database, and exposes a token-protected dispatch board at /admin.

Run locally:   uv run uvicorn volante.main:app --reload --port 7860
On a Space:    Dockerfile runs uvicorn on :7860; set DATABASE_URL=sqlite:////data/volante.db
               (persistent storage) and VOLANTE_ADMIN_TOKEN in the Space Secrets.
"""

from __future__ import annotations

import html
import os
import re
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from .db import Booking, WaitlistEntry, engine, init_db

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SITE_DIR = Path(os.environ.get("SITE_DIR", str(REPO_ROOT / "site")))
ADMIN_TOKEN = os.environ.get("VOLANTE_ADMIN_TOKEN")

ALLOWED_ORIGINS = [
    "https://danielregaladoumiami.github.io",
    "http://localhost:8016",
    "http://127.0.0.1:8016",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Volante", docs_url=None, redoc_url=None, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/waitlist")
def api_waitlist(
    contact: str = Form(default=""),
    zone: str = Form(default=""),
    lang: str = Form(default="es"),
    source: str = Form(default="landing"),
    gotcha: str = Form(default="", alias="_gotcha"),
):
    if gotcha:
        return {"ok": True}  # honeypot: silently drop bots
    contact = contact.strip()
    if len(contact) < 5:
        return JSONResponse({"ok": False, "error": "contact required"}, status_code=400)
    with Session(engine) as s:
        s.add(WaitlistEntry(contact=contact, zone=zone.strip(), lang=lang, source=source))
        s.commit()
    return {"ok": True}


@app.post("/api/request")
def api_request(
    contact: str = Form(default=""),
    lang: str = Form(default="es"),
    source: str = Form(default="request"),
    pickup: str = Form(default=""),
    dropoff: str = Form(default=""),
    passengers: str = Form(default=""),
    estimate: str = Form(default=""),
    when: str = Form(default=""),
    gotcha: str = Form(default="", alias="_gotcha"),
):
    if gotcha:
        return {"ok": True}
    contact = contact.strip()
    if len(contact) < 5:
        return JSONResponse({"ok": False, "error": "contact required"}, status_code=400)
    with Session(engine) as s:
        s.add(
            Booking(
                contact=contact,
                lang=lang,
                source=source,
                pickup=pickup,
                dropoff=dropoff,
                passengers=passengers,
                estimate=estimate,
                when_text=when,
            )
        )
        s.commit()
    return {"ok": True}


def _authed(token: str | None) -> bool:
    return not ADMIN_TOKEN or token == ADMIN_TOKEN


def _wa(contact: str) -> str:
    digits = re.sub(r"\D", "", contact)
    if "@" in contact:
        return f'<a href="mailto:{html.escape(contact)}">{html.escape(contact)}</a>'
    if len(digits) >= 7:
        return f'<a href="https://wa.me/{digits}">{html.escape(contact)}</a>'
    return html.escape(contact)


_STATUSES = ["new", "assigned", "en route", "done", "canceled"]


@app.post("/admin/booking/{booking_id}")
def admin_update(booking_id: int, status: str = Form(...), token: str = Form(default="")):
    if not _authed(token):
        return JSONResponse({"detail": "forbidden"}, status_code=403)
    with Session(engine) as s:
        b = s.get(Booking, booking_id)
        if b and status in _STATUSES:
            b.status = status
            s.add(b)
            s.commit()
    return RedirectResponse(f"/admin?token={token}", status_code=303)


@app.get("/admin", response_class=HTMLResponse)
def admin(token: str | None = None):
    if not _authed(token):
        return HTMLResponse(
            "<h1>403</h1><p>Add <code>?token=YOUR_TOKEN</code> to the URL.</p>", status_code=403
        )
    tok = html.escape(token or "")
    with Session(engine) as s:
        bookings = s.exec(select(Booking).order_by(Booking.id.desc())).all()
        waits = s.exec(select(WaitlistEntry).order_by(WaitlistEntry.id.desc())).all()

    rows = ""
    for b in bookings:
        opts = "".join(
            f'<option {"selected" if b.status == st else ""}>{st}</option>' for st in _STATUSES
        )
        rows += (
            f"<tr class='st-{b.status.replace(' ', '-')}'><td>{b.id}</td>"
            f"<td>{b.created_at:%m/%d %H:%M}</td>"
            f"<td>{html.escape(b.pickup)} → {html.escape(b.dropoff)}</td>"
            f"<td>{html.escape(str(b.passengers))}</td><td>${html.escape(str(b.estimate))}</td>"
            f"<td>{html.escape(b.when_text)}</td><td>{_wa(b.contact)}</td>"
            f"<td><form method='post' action='/admin/booking/{b.id}'>"
            f"<input type='hidden' name='token' value='{tok}'>"
            f"<select name='status' onchange='this.form.submit()'>{opts}</select></form></td></tr>"
        )
    wl = "".join(
        f"<tr><td>{w.id}</td><td>{w.created_at:%m/%d %H:%M}</td>"
        f"<td>{html.escape(w.zone)}</td><td>{html.escape(w.lang)}</td><td>{_wa(w.contact)}</td></tr>"
        for w in waits
    )
    page = f"""<!doctype html><html><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>Volante · dispatch</title>
<style>body{{font-family:system-ui,sans-serif;margin:0;background:#fff6ec;color:#20302f}}
.wrap{{max-width:1000px;margin:0 auto;padding:1.5rem}}h1{{color:#0a5350}}
h2{{margin-top:2rem}}table{{width:100%;border-collapse:collapse;background:#fffdf8;border-radius:12px;overflow:hidden}}
th,td{{padding:.55rem .6rem;text-align:left;border-bottom:1px solid #f4e7d4;font-size:.9rem}}
th{{background:#0a5350;color:#fff}}select{{padding:.3rem}}.st-new td{{background:#fff3d6}}
.st-done td,.st-canceled td{{opacity:.55}}
.pill{{background:#0e6e6e;color:#fff;padding:.2rem .6rem;
border-radius:999px;font-size:.8rem}}</style>
</head><body><div class=wrap>
<h1>Volante · dispatch board</h1>
<p><span class=pill>{len(bookings)} pilot requests</span> &nbsp;
<span class=pill>{len(waits)} waitlist</span></p>
<h2>Pilot ride requests</h2>
<table><tr><th>#</th><th>When req.</th><th>Trip</th><th>Pax</th>
<th>Est.</th><th>Night</th><th>Contact</th><th>Status</th></tr>
{rows or "<tr><td colspan=8>No requests yet.</td></tr>"}</table>
<h2>Waitlist</h2>
<table><tr><th>#</th><th>When</th><th>Zone</th><th>Lang</th><th>Contact</th></tr>
{wl or "<tr><td colspan=5>No signups yet.</td></tr>"}</table>
</div></body></html>"""
    return HTMLResponse(page)


# Static frontend (the polished site/) — mounted LAST so API routes win.
app.mount("/", StaticFiles(directory=str(SITE_DIR), html=True), name="site")

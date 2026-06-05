"""Storage for waitlist signups and pilot-ride requests.

SQLite by default (set ``DATABASE_URL``). On a Hugging Face Space, point it at the
persistent disk, e.g. ``DATABASE_URL=sqlite:////data/volante.db`` so rows survive restarts.
"""

from __future__ import annotations

import os
from datetime import UTC, datetime

from sqlmodel import Field, SQLModel, create_engine

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///volante.db")

_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=False, connect_args=_connect_args)


def _utcnow() -> datetime:
    return datetime.now(UTC)


class WaitlistEntry(SQLModel, table=True):
    """One landing-page signup — the earliest demand signal for Volante."""

    id: int | None = Field(default=None, primary_key=True)
    contact: str = Field(index=True, description="WhatsApp number or email")
    zone: str = Field(default="")
    lang: str = Field(default="es")
    source: str = Field(default="landing")
    created_at: datetime = Field(default_factory=_utcnow)


class Booking(SQLModel, table=True):
    """A pilot-ride request: the rider, their trip, the shown estimate, and dispatch status."""

    id: int | None = Field(default=None, primary_key=True)
    contact: str = Field(index=True)
    lang: str = Field(default="es")
    source: str = Field(default="request")
    pickup: str = Field(default="")
    dropoff: str = Field(default="")
    passengers: str = Field(default="")
    estimate: str = Field(default="")
    when_text: str = Field(default="")
    status: str = Field(default="new", index=True, description="new → assigned → done")
    notes: str = Field(default="")
    created_at: datetime = Field(default_factory=_utcnow)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)

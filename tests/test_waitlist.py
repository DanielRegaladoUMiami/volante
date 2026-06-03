"""End-to-end checks for the landing page + waitlist capture, on an isolated DB."""

import os
import tempfile

_fd, _db_path = tempfile.mkstemp(suffix=".db")
os.close(_fd)
os.environ["DATABASE_URL"] = f"sqlite:///{_db_path}"  # isolated file DB for the test run

from fastapi.testclient import TestClient  # noqa: E402

from volante.db import init_db  # noqa: E402
from volante.main import app  # noqa: E402

init_db()
client = TestClient(app)


def test_landing_renders_spanish_by_default():
    r = client.get("/")
    assert r.status_code == 200
    assert "y a tu carro" in r.text
    assert 'lang="es"' in r.text


def test_landing_english_toggle():
    r = client.get("/?lang=en")
    assert r.status_code == 200
    assert "and your car" in r.text
    assert 'lang="en"' in r.text


def test_healthz():
    assert client.get("/healthz").json() == {"status": "ok"}


def test_waitlist_accepts_and_persists():
    r = client.post(
        "/waitlist",
        data={"contact": "+13055551234", "zone": "Brickell", "lang": "es"},
        follow_redirects=False,
    )
    assert r.status_code == 303
    assert "joined=1" in r.headers["location"]
    admin = client.get("/admin/waitlist").json()
    assert admin["count"] >= 1
    assert any(e["contact"] == "+13055551234" for e in admin["entries"])


def test_waitlist_rejects_blank_contact():
    r = client.post("/waitlist", data={"contact": "", "lang": "es"}, follow_redirects=False)
    assert r.status_code == 303
    assert "err=1" in r.headers["location"]

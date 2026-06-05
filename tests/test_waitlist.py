"""End-to-end checks for the Volante app (static frontend + API + dispatch board)."""

import os
import tempfile

_fd, _db_path = tempfile.mkstemp(suffix=".db")
os.close(_fd)
os.environ["DATABASE_URL"] = f"sqlite:///{_db_path}"  # isolated file DB for the test run
os.environ["VOLANTE_ADMIN_TOKEN"] = "testtok"

from fastapi.testclient import TestClient  # noqa: E402

from volante.db import init_db  # noqa: E402
from volante.main import app  # noqa: E402

init_db()
client = TestClient(app)


def test_static_landing_served_at_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "y a tu carro" in r.text  # served from site/index.html


def test_english_page_served():
    r = client.get("/en.html")
    assert r.status_code == 200
    assert "and your car" in r.text


def test_healthz():
    assert client.get("/healthz").json() == {"status": "ok"}


def test_api_waitlist_persists():
    data = {"contact": "+13055551234", "zone": "Brickell", "lang": "es"}
    r = client.post("/api/waitlist", data=data)
    assert r.status_code == 200 and r.json() == {"ok": True}
    admin = client.get("/admin?token=testtok")  # no token set in env -> open in test
    assert admin.status_code == 200
    assert "+13055551234" in admin.text


def test_api_request_persists_and_shows_on_board():
    r = client.post(
        "/api/request",
        data={
            "contact": "rider@example.com",
            "pickup": "Wynwood",
            "dropoff": "Kendall",
            "passengers": "2",
            "estimate": "120",
            "lang": "es",
        },
    )
    assert r.status_code == 200 and r.json() == {"ok": True}
    board = client.get("/admin?token=testtok").text
    assert "Wynwood" in board and "Kendall" in board and "rider@example.com" in board


def test_waitlist_rejects_blank_contact():
    r = client.post("/api/waitlist", data={"contact": ""})
    assert r.status_code == 400


def test_honeypot_silently_dropped():
    r = client.post("/api/waitlist", data={"contact": "+13050000000", "_gotcha": "bot"})
    assert r.json() == {"ok": True}
    assert "+13050000000" not in client.get("/admin?token=testtok").text


def test_admin_requires_token():
    assert client.get("/admin").status_code == 403

"""Test endpoint login staf (Lab L2.2), termasuk test negatif keamanan."""
import time

import pytest
import staff as staff_mod
from app import app as flask_app
from staff import bp


@pytest.fixture
def staff_client():
    if "staff" not in flask_app.blueprints:
        flask_app.register_blueprint(bp)
    flask_app.config.update(TESTING=True)
    staff_mod._percobaan.clear()
    with flask_app.test_client() as c:
        yield c


def test_login_benar(staff_client):
    r = staff_client.post("/staff/login", json={"username": "barista1", "password": "barista-rahasia"})
    assert r.status_code == 200
    assert r.get_json()["role"] == "staff"


def test_password_salah(staff_client):
    r = staff_client.post("/staff/login", json={"username": "barista1", "password": "salah"})
    assert r.status_code == 401


def test_injeksi_tidak_bypass(staff_client):
    r = staff_client.post("/staff/login", json={"username": "barista1' OR '1'='1' --", "password": "x"})
    assert r.status_code == 401


def test_rate_limit_setelah_lima_gagal(staff_client):
    for _ in range(5):
        staff_client.post("/staff/login", json={"username": "barista1", "password": "salah"})
    r = staff_client.post("/staff/login", json={"username": "barista1", "password": "barista-rahasia"})
    assert r.status_code == 429


def test_password_tidak_masuk_log(staff_client, caplog):
    with caplog.at_level("INFO"):
        staff_client.post("/staff/login", json={"username": "barista1", "password": "rahasia-unik-123"})
    assert "rahasia-unik-123" not in caplog.text


def test_hash_pbkdf2_600rb_iterasi():
    import staff

    assert staff.STAF["barista1"].startswith("pbkdf2:sha256:600000$")

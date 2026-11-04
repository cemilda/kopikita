"""Test endpoint ringkasan pesanan (Lab L4.4)."""
import pathlib
import subprocess
import sys

import pytest
from app import app as flask_app
from conftest import auth, login
from summary import bp


@pytest.fixture
def summary_client(client):
    if "summary" not in flask_app.blueprints:
        flask_app.register_blueprint(bp)
    return client


def test_ringkasan_milik_sendiri(summary_client):
    token = login(summary_client, "alice", "alice123")
    data = summary_client.get("/orders/summary", headers=auth(token)).get_json()
    # Alice punya pesanan 101 (46000) dan 103 (27000).
    assert data["jumlah_pesanan"] == 2
    assert data["total_belanja"] == 73000


def test_ringkasan_perlu_login(summary_client):
    assert summary_client.get("/orders/summary").status_code == 401


def test_app_py_bisa_dijalankan_langsung():
    # `python api/app.py` memuat app.py bukan sebagai modul `app`; impor melingkar hanya muncul di jalur ini.
    root = pathlib.Path(__file__).resolve().parents[1]
    kode = "import runpy, sys; sys.path.insert(0, 'api'); runpy.run_path('api/app.py', run_name='bukan_main')"
    hasil = subprocess.run([sys.executable, "-c", kode], cwd=root, capture_output=True, text=True, timeout=30)
    assert hasil.returncode == 0, hasil.stderr

"""Test endpoint pencarian (Lab L2.3b)."""
import pytest
from app import app as flask_app
from search import bp


@pytest.fixture
def search_client(client):
    if "search" not in flask_app.blueprints:
        flask_app.register_blueprint(bp)
    return client


def test_pencarian_menemukan_produk(search_client):
    data = search_client.get("/search?q=kopi").get_json()
    assert data["count"] >= 1
    assert all("name" in p for p in data["products"])


def test_pencarian_tahan_injeksi(search_client):
    # Tidak boleh error 500; query berparameter memperlakukan ini sebagai teks biasa.
    resp = search_client.get("/search?q=%27%20OR%20%271%27%3D%271")
    assert resp.status_code == 200
    assert resp.get_json()["count"] == 0


def test_query_di_escape(search_client):
    data = search_client.get("/search?q=<script>alert(1)</script>").get_json()
    assert "<script>" not in data["query"]
    assert "&lt;script&gt;" in data["query"]

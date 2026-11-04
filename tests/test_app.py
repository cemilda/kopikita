"""Test fungsional dasar. Semua harus lulus di setiap branch."""
from conftest import auth, login


def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}


def test_login_berhasil(client):
    token = login(client, "alice", "alice123")
    assert len(token) > 20


def test_login_password_salah(client):
    resp = client.post("/login", json={"username": "alice", "password": "salah"})
    assert resp.status_code == 401


def test_produk_diurutkan_harga(client):
    resp = client.get("/products?sort=price")
    prices = [p["price"] for p in resp.get_json()["products"]]
    assert prices == sorted(prices)


def test_kolom_sort_tidak_dikenal_ditolak(client):
    assert client.get("/products?sort=password_hash").status_code == 400


def test_daftar_pesanan_milik_sendiri(client):
    token = login(client, "alice", "alice123")
    ids = [o["id"] for o in client.get("/orders", headers=auth(token)).get_json()["orders"]]
    assert ids == [101, 103]


def test_detail_pesanan_milik_sendiri(client):
    token = login(client, "alice", "alice123")
    resp = client.get("/orders/101", headers=auth(token))
    assert resp.status_code == 200
    assert resp.get_json()["order"]["items"].startswith("Kopi Susu")


def test_invoice_milik_sendiri(client):
    token = login(client, "alice", "alice123")
    resp = client.get("/invoices?file=invoice-101.txt", headers=auth(token))
    assert resp.status_code == 200
    assert "INVOICE KOPIKITA #101" in resp.get_data(as_text=True)


def test_perlu_login(client):
    assert client.get("/orders").status_code == 401

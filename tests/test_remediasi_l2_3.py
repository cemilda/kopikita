"""Test negatif untuk tiga perbaikan Lab L2.3 (dibuat bersama patch, bukan sesudahnya)."""
from conftest import auth, login


def test_login_tahan_injeksi(client):
    resp = client.post("/login", json={"username": "alice' OR '1'='1' --", "password": "x"})
    assert resp.status_code == 401


def test_login_tetap_berfungsi(client):
    assert len(login(client, "alice", "alice123")) > 20


def test_invoice_tolak_path_traversal(client):
    token = login(client, "alice", "alice123")
    for jahat in ["../config.py", "..%2fconfig.py", "/etc/passwd", "invoice-101.txt/../../config.py"]:
        resp = client.get(f"/invoices?file={jahat}", headers=auth(token))
        assert resp.status_code in (400, 404), jahat


def test_invoice_valid_tetap_bisa(client):
    token = login(client, "alice", "alice123")
    resp = client.get("/invoices?file=invoice-101.txt", headers=auth(token))
    assert resp.status_code == 200


def test_invoice_orang_lain_ditolak(client):
    token = login(client, "alice", "alice123")
    assert client.get("/invoices?file=invoice-102.txt", headers=auth(token)).status_code == 404


def test_invoice_nomor_tidak_dikenal_ditolak(client):
    token = login(client, "alice", "alice123")
    for nomor in ["999", "9" * 40]:
        resp = client.get(f"/invoices?file=invoice-{nomor}.txt", headers=auth(token))
        assert resp.status_code == 404, nomor

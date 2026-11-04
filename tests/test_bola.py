"""Test regresi BOLA (Lab L3.2b): pelanggan B tidak boleh melihat pesanan pelanggan A."""
from conftest import auth, login


def test_budi_tidak_bisa_lihat_pesanan_alice(client):
    token_budi = login(client, "budi", "budi123")
    # Pesanan 101 dan 103 milik Alice.
    assert client.get("/orders/101", headers=auth(token_budi)).status_code == 404
    assert client.get("/orders/103", headers=auth(token_budi)).status_code == 404


def test_alice_tetap_bisa_lihat_pesanannya(client):
    token_alice = login(client, "alice", "alice123")
    resp = client.get("/orders/101", headers=auth(token_alice))
    assert resp.status_code == 200
    assert resp.get_json()["order"]["id"] == 101


def test_budi_bisa_lihat_pesanannya_sendiri(client):
    token_budi = login(client, "budi", "budi123")
    assert client.get("/orders/102", headers=auth(token_budi)).status_code == 200

"""Klien gateway pembayaran (stub). Tidak dipanggil saat test."""
import requests

import config

PAYMENT_URL = "https://payments.example.invalid/v1/charge"


def charge(order_id, amount):
    resp = requests.post(
        PAYMENT_URL,
        json={"order_id": order_id, "amount": amount},
        headers={"X-Api-Key": config.PAYMENT_API_KEY},
        timeout=5,
    )
    resp.raise_for_status()
    return resp.json()

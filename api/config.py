"""Konfigurasi aplikasi KopiKita.

Rahasia dibaca dari environment variable (diperbaiki di Lab L1.3).
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = "dev-secret-kopikita"
# Key lama sudah dicabut (runbook docs/runbook/kebocoran-rahasia.md).
# Nilai baru hanya dari environment, tidak pernah dari kode.
PAYMENT_API_KEY = os.environ.get("PAYMENT_API_KEY", "")

DATABASE = os.environ.get("KOPIKITA_DB", os.path.join(BASE_DIR, "kopikita.db"))
INVOICE_DIR = os.path.join(BASE_DIR, "invoices")

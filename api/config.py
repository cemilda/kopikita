"""Konfigurasi aplikasi KopiKita.

PERINGATAN: berkas ini SENGAJA menyimpan rahasia di dalam kode (Lab L1.3).
Nilainya palsu dan hanya untuk latihan.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = "dev-secret-kopikita"
# RENTAN: API key gateway pembayaran tertanam di kode
PAYMENT_API_KEY = "kopikita_live_0011223344556677889900aabbccddee"

DATABASE = os.environ.get("KOPIKITA_DB", os.path.join(BASE_DIR, "kopikita.db"))
INVOICE_DIR = os.path.join(BASE_DIR, "invoices")

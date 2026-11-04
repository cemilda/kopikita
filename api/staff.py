"""Login staf (barista) KopiKita — hasil prompt aman Lab L2.2.

Dibuat dengan pola dari prompts/claude-security-prompts.md:
- query berparameter,
- password di-hash dengan werkzeug (PBKDF2-SHA256, 600.000 iterasi),
- rate limit login,
- password tidak pernah masuk log,
- pesan error sama untuk username dan password salah.
"""
import time
from collections import defaultdict

from flask import Blueprint, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint("staff", __name__)

MAX_GAGAL = 5
JENDELA_DETIK = 15 * 60
_percobaan = defaultdict(list)

# PBKDF2-SHA256 dengan 600.000 iterasi (rekomendasi OWASP Password Storage Cheat Sheet).
# Ditulis eksplisit karena bawaan werkzeug berbeda antarversi.
METODE_HASH = "pbkdf2:sha256:600000"
STAF = {"barista1": generate_password_hash("barista-rahasia", method=METODE_HASH)}


def _terkena_rate_limit(username, sekarang):
    baru = [t for t in _percobaan[username] if sekarang - t < JENDELA_DETIK]
    _percobaan[username] = baru
    return len(baru) >= MAX_GAGAL


@bp.post("/staff/login")
def staff_login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")
    sekarang = time.time()

    if _terkena_rate_limit(username, sekarang):
        return jsonify(error="terlalu banyak percobaan, coba lagi nanti"), 429

    stored = STAF.get(username)
    # check_password_hash aman terhadap input kosong; pesan error dibuat seragam.
    if stored is None or not check_password_hash(stored, password):
        _percobaan[username].append(sekarang)
        return jsonify(error="username atau password salah"), 401

    _percobaan[username] = []
    return jsonify(message="login berhasil", role="staff", username=username)


def register(app):
    app.register_blueprint(bp)

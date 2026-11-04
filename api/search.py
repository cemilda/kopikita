"""Endpoint pencarian produk — hasil loop temukan-perbaiki-verifikasi Lab L2.3b.

Dibangun dengan Claude memakai Semgrep MCP: tulis fitur, jalankan security_check,
perbaiki, ulangi sampai bersih. Versi akhir memakai query berparameter dan escaping HTML.
"""
from markupsafe import escape

from flask import Blueprint, current_app, jsonify, request

from db import connect

bp = Blueprint("search", __name__)


@bp.get("/search")
def search():
    q = request.args.get("q", "").strip()
    # Query berparameter; LIKE memakai parameter, bukan penggabungan string.
    # Pakai DATABASE dari konfigurasi aplikasi (menghormati override saat test).
    rows = connect(current_app.config["DATABASE"]).execute(
        "SELECT id, name, price, category FROM products WHERE name LIKE ? ORDER BY name",
        (f"%{q}%",),
    ).fetchall()
    # Pantulkan query sebagai teks yang sudah di-escape (cegah XSS bila dirender klien).
    return jsonify(query=str(escape(q)), count=len(rows), products=[dict(r) for r in rows])


def register(app):
    app.register_blueprint(bp)

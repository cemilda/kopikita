"""Endpoint sambutan — SENGAJA rentan XSS untuk PR uji Lab L2.4."""
from flask import Blueprint, request

bp = Blueprint("greeting", __name__)


@bp.get("/greeting")
def greeting():
    name = request.args.get("name", "tamu")
    # RENTAN: input pengguna dipantulkan ke HTML tanpa escaping (XSS, CWE-79)
    return f"<h1>Halo, {name}!</h1>"


def register(app):
    app.register_blueprint(bp)

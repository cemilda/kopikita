"""Titik masuk WSGI untuk server produksi (mis. gunicorn wsgi:app)."""
from app import app
from db import init_db

init_db(app.config["DATABASE"])

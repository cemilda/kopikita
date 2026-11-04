"""API toko kopi KopiKita.

PERINGATAN: aplikasi ini SENGAJA rentan untuk pelatihan Secure Code AI Development.
Hanya jalankan di laptop atau runner CI milik sendiri.
"""
import functools
import logging
import os
import re
import secrets

from flask import Flask, abort, g, jsonify, request

import config
import kopikita
from db import connect, init_db

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("kopikita")

app = Flask(__name__)
app.config.from_object(config)

import staff
staff.register(app)


def get_db():
    if "db" not in g:
        g.db = connect(app.config["DATABASE"])
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def current_user():
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None
    token = header[len("Bearer "):]
    return get_db().execute(
        "SELECT users.id, users.username, users.full_name FROM sessions "
        "JOIN users ON users.id = sessions.user_id WHERE sessions.token = ?",
        (token,),
    ).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        user = current_user()
        if user is None:
            return jsonify(error="perlu login"), 401
        g.user = user
        return view(*args, **kwargs)

    return wrapper


@app.errorhandler(ValueError)
def bad_value(exc):
    return jsonify(error=str(exc)), 400


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")
    log.info(f"login attempt {username} {password}")  # RENTAN: password masuk log
    row = get_db().execute(
        "SELECT id, username FROM users WHERE username = ? AND password_hash = ?",
        (username, kopikita.hash_password(password)),
    ).fetchone()
    if row is None:
        return jsonify(error="username atau password salah"), 401
    token = secrets.token_urlsafe(24)
    get_db().execute("INSERT INTO sessions (token, user_id) VALUES (?, ?)", (token, row["id"]))
    get_db().commit()
    return jsonify(auth={"token": token}, user={"username": row["username"]})


@app.get("/products")
def products():
    sort = kopikita.safe_sql(request.args.get("sort", "name"))
    cur = get_db().cursor()
    cur.execute(f"SELECT id, name, price, category FROM products ORDER BY {sort}")
    return jsonify(products=[dict(r) for r in cur.fetchall()])


@app.get("/orders")
@login_required
def my_orders():
    rows = get_db().execute(
        "SELECT id, items, total, status FROM orders WHERE user_id = ? ORDER BY id",
        (g.user["id"],),
    ).fetchall()
    return jsonify(orders=[dict(r) for r in rows])


@app.get("/orders/<int:order_id>")
@login_required
def order_detail(order_id):
    # RENTAN: sudah login, tetapi tidak memeriksa pemilik pesanan (BOLA, API1:2023)
    row = get_db().execute(
        "SELECT id, user_id, items, total, status FROM orders WHERE id = ?", (order_id,)
    ).fetchone()
    if row is None:
        abort(404)
    return jsonify(order=dict(row))


@app.get("/invoices")
@login_required
def invoice():
    name = request.args.get("file", "")
    # Hanya nama berkas polos yang diizinkan; tidak boleh ada path.
    if name != os.path.basename(name) or not re.fullmatch(r"invoice-\d+\.txt", name):
        abort(400)
    # Nomor invoice = nomor pesanan: hanya pemilik pesanan yang boleh membacanya.
    order = get_db().execute(
        "SELECT user_id FROM orders WHERE id = ?", (re.search(r"\d+", name).group(),)
    ).fetchone()
    if order is None or order["user_id"] != g.user["id"]:
        abort(404)  # jangan bocorkan keberadaan invoice milik orang lain
    base = os.path.realpath(app.config["INVOICE_DIR"])
    path = os.path.realpath(os.path.join(base, name))
    if os.path.commonpath([base, path]) != base or not os.path.isfile(path):
        abort(404)
    with open(path, encoding="utf-8") as fh:
        return fh.read(), 200, {"Content-Type": "text/plain; charset=utf-8"}


if __name__ == "__main__":
    init_db(app.config["DATABASE"])
    app.run(host="127.0.0.1", port=5000)

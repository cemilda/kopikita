# Berkas test untuk rules/kopikita-sql-taint.yaml. Jalankan: semgrep --test rules/
# Baris setelah "ruleid:" HARUS ditandai; baris setelah "ok:" TIDAK boleh ditandai.
import sqlite3

from flask import request

import kopikita


def cari_user_rentan():
    cur = sqlite3.connect(":memory:").cursor()
    name = request.args.get("name")
    # ruleid: kopikita-sql-taint
    cur.execute("SELECT * FROM users WHERE username = '" + name + "'")


def login_form_rentan():
    cur = sqlite3.connect(":memory:").cursor()
    username = request.form["username"]
    query = "SELECT * FROM users WHERE username = '%s'" % username
    # ruleid: kopikita-sql-taint
    cur.execute(query)


def login_json_rentan():
    cur = sqlite3.connect(":memory:").cursor()
    data = request.get_json()
    # ruleid: kopikita-sql-taint
    cur.execute(f"SELECT * FROM users WHERE username = '{data['username']}'")


def cari_user_berparameter():
    cur = sqlite3.connect(":memory:").cursor()
    name = request.args.get("name")
    # ok: kopikita-sql-taint
    cur.execute("SELECT * FROM users WHERE username = ?", (name,))


def urutkan_produk_tersanitasi():
    cur = sqlite3.connect(":memory:").cursor()
    sort = kopikita.safe_sql(request.args.get("sort", "name"))
    # ok: kopikita-sql-taint
    cur.execute(f"SELECT * FROM products ORDER BY {sort}")

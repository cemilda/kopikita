"""Akses database SQLite untuk aplikasi KopiKita."""
import os
import sqlite3

import kopikita

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    category TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    items TEXT NOT NULL,
    total INTEGER NOT NULL,
    status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS sessions (
    token TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id)
);
"""

# Akun uji untuk lab. Pelanggan A = alice, pelanggan B = budi.
USERS = [
    (1, "alice", "alice123", "Alice Pratama"),
    (2, "budi", "budi123", "Budi Santoso"),
]

PRODUCTS = [
    (1, "Kopi Susu Gula Aren", 23000, "kopi"),
    (2, "Americano", 25000, "kopi"),
    (3, "Teh Tarik", 20000, "non-kopi"),
    (4, "Croissant Mentega", 28000, "roti"),
    (5, "Es Kopi Pandan", 27000, "kopi"),
]

ORDERS = [
    (101, 1, "Kopi Susu Gula Aren x2", 46000, "selesai"),
    (102, 2, "Americano x1, Croissant Mentega x1", 53000, "diproses"),
    (103, 1, "Es Kopi Pandan x1", 27000, "diproses"),
]


def connect(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(path):
    """Membuat skema dan data contoh bila database masih kosong."""
    conn = connect(path)
    conn.executescript(SCHEMA)
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO users (id, username, password_hash, full_name) VALUES (?, ?, ?, ?)",
            [(i, u, kopikita.hash_password(p), n) for i, u, p, n in USERS],
        )
        conn.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", PRODUCTS)
        conn.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", ORDERS)
        conn.commit()
    conn.close()


if __name__ == "__main__":
    import config

    init_db(os.environ.get("KOPIKITA_DB", config.DATABASE))
    print("Database siap:", os.environ.get("KOPIKITA_DB", config.DATABASE))

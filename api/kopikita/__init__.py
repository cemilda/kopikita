"""Utilitas internal tim KopiKita.

PERINGATAN: repo latihan ini SENGAJA berisi kerentanan. Jangan dipakai di produksi.
"""
import hashlib

# Kolom yang boleh dipakai untuk ORDER BY. Nama kolom tidak bisa diparameterisasi,
# jadi tim memakai allowlist ini sebagai sanitizer.
SORTABLE_COLUMNS = {"name", "price", "category"}


def safe_sql(identifier):
    """Sanitizer internal: hanya mengembalikan nama kolom yang ada di allowlist.

    Dipakai untuk bagian query yang tidak bisa memakai parameter, misalnya ORDER BY.
    Melempar ValueError bila nilainya tidak diizinkan.
    """
    if identifier not in SORTABLE_COLUMNS:
        raise ValueError(f"kolom tidak diizinkan: {identifier!r}")
    return identifier


def hash_password(password):
    """RENTAN: MD5 tanpa salt. Cepat dihitung sehingga mudah ditebak (CWE-916)."""
    return hashlib.md5(password.encode("utf-8")).hexdigest()


def verify_password(password, stored_hash):
    return hash_password(password) == stored_hash

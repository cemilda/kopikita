#!/usr/bin/env python3
"""Deteksi karakter tersembunyi yang bisa dipakai menyembunyikan instruksi (Lab L4.3).

Memindai karakter bidirectional override (U+202A–U+202E, U+2066–U+2069) dan zero-width
(U+200B, U+200C, U+200D, U+2060, U+FEFF), plus tag characters U+E0000–U+E007F di kode dan teks repo. Dipakai sebagai gerbang CI.

Jalankan: python scripts/check_hidden_chars.py [path ...]
Keluar dengan kode 1 bila ada temuan.
"""
import pathlib
import sys

BIDI = set(range(0x202A, 0x202F)) | set(range(0x2066, 0x206A))
ZERO_WIDTH = {0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF}
# Bonus: Unicode "tag characters" (U+E0000–U+E007F) tidak terlihat sama sekali dan dipakai
# untuk menyelundupkan instruksi ke berkas aturan agen ("rules file backdoor").
TAG = set(range(0xE0000, 0xE0080))
TERLARANG = BIDI | ZERO_WIDTH | TAG

EKSTENSI = {".py", ".js", ".ts", ".jsx", ".tsx", ".md", ".mdc", ".yaml", ".yml", ".json", ".tf",
            ".rego", ".txt", ".html", ".sh", ".toml", ".ini", ".cfg"}
# Berkas tanpa ekstensi yang tetap wajib dipindai (aturan agen, pipeline, kepemilikan).
NAMA = {"Dockerfile", "CODEOWNERS", ".cursorrules", ".env.example"}
LEWATI = {".git", "node_modules", ".venv", "__pycache__"}


def iter_files(roots):
    for root in roots:
        p = pathlib.Path(root)
        if p.is_file():
            yield p
            continue
        for f in p.rglob("*"):
            if (f.is_file() and (f.suffix in EKSTENSI or f.name in NAMA)
                    and not any(part in LEWATI for part in f.parts)):
                yield f


def scan(path):
    temuan = []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return temuan
    for lineno, line in enumerate(text.splitlines(), 1):
        for col, ch in enumerate(line, 1):
            if ord(ch) in TERLARANG:
                temuan.append((lineno, col, f"U+{ord(ch):04X}"))
    return temuan


def main(argv):
    roots = argv or ["."]
    total = 0
    for f in iter_files(roots):
        for lineno, col, code in scan(f):
            print(f"{f}:{lineno}:{col}: karakter tersembunyi {code}")
            total += 1
    if total:
        print(f"\nDitemukan {total} karakter tersembunyi. Tinjau sebelum merge.")
        return 1
    print("Tidak ada karakter tersembunyi.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

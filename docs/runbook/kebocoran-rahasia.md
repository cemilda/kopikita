# Runbook kebocoran rahasia: cabut, hapus, audit

Urutan ini wajib. Rahasia yang pernah ter-push dianggap **sudah dicuri**.

## 1. Cabut (dalam 15 menit)

- Cabut atau rotasi key di penyedianya (dashboard gateway pembayaran, AWS IAM, GitHub token).
- Pasang key baru sebagai secret (GitHub Actions secret atau vault), bukan di kode.
- Catat waktu pencabutan.

## 2. Hapus

- Ubah kode agar membaca dari environment variable (contoh: `api/config.py`).
- Bila perlu membersihkan histori, gunakan `git filter-repo` dan koordinasikan force push.
- Ingat: menghapus histori **tidak** menarik kembali salinan di clone, fork, cache, atau log.
  Karena itu langkah 1 selalu lebih dulu.
- Tutup alert secret scanning dengan status **Revoked**.

## 3. Audit

- Periksa log penyedia: apakah key dipakai antara waktu bocor dan waktu dicabut?
- Periksa siapa yang meng-clone atau mem-fork repo pada rentang itu (bila tersedia).
- Tulis laporan singkat: apa yang bocor, kapan, dampak, dan pencegahan (custom pattern + push protection).

## Pencegahan yang sudah dipasang

- Pre-commit hook: `scripts/pre-commit-security.sh`
- Custom pattern + push protection: `docs/hasil/L1.3-custom-pattern.md`
- Test regresi: `tests/test_tanpa_rahasia_di_kode.py`

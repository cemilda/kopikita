# Persiapan instruktur

## Seminggu sebelum kelas

- [ ] Push repo ini ke organisasi instruktur dengan **semua branch**: `git push --all origin`.
- [ ] Buat organisasi kelas; undang peserta; buat tim `keamanan` dan `platform` (dipakai CODEOWNERS).
- [ ] Cek ulang harga paket Claude, kuota API, dan kebijakan GHAS untuk repo publik.
- [ ] Siapkan API key Claude untuk secret `ANTHROPIC_API_KEY` (satu per kelompok, dengan batas biaya di Console).
- [ ] Opsional: akun StackHawk (L3.2b) dan akun AWS latihan (OIDC, L4.3).
- [ ] Buka setiap tautan di `docs/REFERENSI.md` (diverifikasi Oktober 2026). Perhatikan yang cepat berubah:
      harga dan nama produk GitHub (Secret Protection/Code Security), jalur menu Settings, nama produk Semgrep
      (Multimodal, dulu Assistant), status `semgrep-mcp`, dan quality gate SonarQube untuk kode AI.

## Verifikasi yang belum dijalankan saat repo dibangun

Repo ini dibangun dan diuji otomatis di lingkungan tanpa akses ke GitHub Actions, Docker, PyPI, dan
beberapa binary eksternal. Yang **sudah** diverifikasi: semua branch terbangun, `pytest` lulus di semua
branch (kecuali `pr/L4.3-pr-bidi` yang memang harus gagal), semua YAML/JSON valid, SHA action dicocokkan
dengan `git ls-remote` ke repo resmi, dan teks slide = teks panduan (`build/check_consistency.py`).

Jalankan sekali di laptop instruktur sebelum kelas:

| Periksa | Perintah | Hasil yang diharapkan |
| --- | --- | --- |
| Test dengan versi dependensi persis | `bash scripts/setup-lab.sh` di `main` | 9 test lulus dengan Flask 2.2.2 / Werkzeug 2.2.2 (Python 3.11 atau 3.12) |
| Rule Semgrep | `git switch lab/L1.2b-solution && semgrep --test rules/ && semgrep scan --config rules/ api/` | test lulus; temuan di `login`, tidak di `products` |
| Kebijakan Rego | `git switch lab/L4.1-solution && conftest verify -p policy/ && conftest test -p policy/ infra/main.tf` | verify lulus; test lolos; `main:infra/main.tf` gagal 3 aturan |
| Checkov | `git switch lab/L3.4-solution && checkov -d infra/ --hard-fail-on CKV_AWS_20,CKV_AWS_24,CKV_AWS_3,CKV_K8S_16 --soft-fail` | keluar 0; di `main` keluar 1 |
| Image | `git switch lab/L3.3-solution && docker compose up -d --build && curl localhost:5000/health` | `{"status":"ok"}`, uid 10001 |
| Alert CodeQL | Jalankan CodeQL di `lab/L1.2-solution` | Cocokkan nomor/rule dengan `docs/hasil/L1.2-triase.md`; perbarui bila berbeda |
| Workflow | Jadikan tiap branch solution default sementara, jalankan workflow-nya sekali | Hijau (kecuali yang butuh secret yang belum diisi) |
| Semgrep MCP | `uvx semgrep-mcp@0.9.0 --help` | Server berjalan; bila sudah dipindah ke binary `semgrep`, perbarui `.mcp.json` dan slide |
| Claude Security | `/plugin install claude-security@claude-plugins-official` | Nama perintah dan berkas hasil sama dengan Demo Sesi 2.3 |
| Agen triase | `git switch lab/L3.1-solution && python agent/triage_agent.py` | PR draft untuk alert 4 |

## Pagi hari setiap hari kelas

- [ ] Rekam cadangan: hasil scan, PR review Claude, PR agen, issue digest (bila API/jaringan bermasalah).
- [ ] Jalankan analisis CodeQL dan run workflow untuk demo hari itu (analisis pertama butuh beberapa menit).
- [ ] Siapkan PR uji demo 10 menit sebelum sesi (`pr/L2.4-pr-xss`, `pr/L4.3-pr-bidi`).

## Setelah kelas

- [ ] Nonaktifkan workflow terjadwal di fork peserta (`security-digest.yml`) atau hapus secret API key.
- [ ] Cabut token agen dan API key kelas.
- [ ] Arsipkan organisasi kelas.

## Membangun ulang repo

Repo dibangun dari generator (`build/` di paket sumber), bukan diedit per branch:

```bash
bash build/all.sh <folder-deck>/build <folder-keluaran>
```

`all.sh` mengekstrak teks slide dari deck, menulis ulang panduan, membangun semua branch, menjalankan
test per branch, dan memeriksa konsistensi slide ↔ panduan ↔ repo.

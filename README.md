# kopikita-vuln

Aplikasi latihan pelatihan **Secure Code AI Development with Claude Code** (Inixindo Bandung, 4 hari).
KopiKita adalah toko kopi daring kecil yang **sengaja dibuat rentan**: API Flask + SQLite, frontend
Node.js, Dockerfile, Terraform, manifest Kubernetes, dan workflow GitHub Actions. Setiap lapisan punya
cacat yang ditemukan dan diperbaiki di lab.

> ⚠️ Jangan deploy aplikasi ini. Semua rahasia di repo ini palsu. Pindai hanya repo dan aplikasi milik sendiri.

## Mulai

```bash
gh repo fork <org-instruktur>/kopikita-vuln --org <org-kelas> --clone=false   # semua branch ikut
gh repo clone <org-kelas>/kopikita-vuln && cd kopikita-vuln
bash scripts/setup-lab.sh          # .venv, .env palsu, database, test
source .venv/bin/activate && python api/app.py     # http://localhost:5000/health
```

Di UI GitHub: **Fork** → hapus centang *Copy the `main` branch only* agar semua branch lab ikut.

## Branch

| Branch | Isi |
| --- | --- |
| `main` | Aplikasi rentan + semua panduan |
| `lab/<ID>-start` | Titik mulai lab; sudah berisi hasil lab prasyarat |
| `lab/<ID>-solution` | Kunci jawaban (commit anak dari start) |
| `aux/*` | PR uji siap pakai (dependensi lama, XSS, kanari, karakter bidi) |
| `demo/settings` | Berkas demo `settings.json` Sesi 2.1 |

```bash
git switch lab/L2.1-start && git switch -c kerja/L2.1     # mulai lab
git diff lab/L2.1-start lab/L2.1-solution                  # lihat jawaban
```

Peta lengkap: [docs/BRANCHES.md](docs/BRANCHES.md).

## Panduan

- Peserta: [docs/labs/](docs/labs/README.md): 20 lab, teks tujuan/langkah/jebakan sama persis dengan slide.
- Instruktur: [docs/demos/](docs/demos/README.md) (12 demo) dan [docs/instructor/persiapan.md](docs/instructor/persiapan.md).
- Pustaka prompt: [prompts/claude-security-prompts.md](prompts/claude-security-prompts.md).
- Referensi resmi dan pakar (per slide dan per lab): [docs/REFERENSI.md](docs/REFERENSI.md).

## Endpoint

| Endpoint | Auth | Catatan lab |
| --- | --- | --- |
| `GET /health` | — | |
| `POST /login` | — | SQL injection, password di log (L1.2, L2.3, L3.1) |
| `GET /products?sort=` | — | `ORDER BY` lewat allowlist `kopikita.safe_sql` (L1.2b) |
| `GET /orders` | Bearer | |
| `GET /orders/<id>` | Bearer | BOLA: tanpa cek pemilik (L3.2b) |
| `GET /invoices?file=` | Bearer | Path traversal (L2.3) |

Akun uji: `alice` / `alice123`, `budi` / `budi123`.

## Atribusi

Beberapa skrip, templat, dan struktur diadaptasi dari
[paulasilvatech/Secure-Code-AI-Dev](https://github.com/paulasilvatech/Secure-Code-AI-Dev) (lisensi MIT),
dengan GitHub Copilot diganti Claude Code. Rujukan konsep: OWASP Secure Coding with AI Cheat Sheet.

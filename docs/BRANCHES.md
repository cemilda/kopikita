# Peta branch repo kopikita-vuln

Setiap lab punya dua branch. `start` = titik mulai (sudah berisi hasil lab prasyarat),
`solution` = kunci jawaban, dibuat sebagai commit anak dari `start`.

```bash
git fetch --all
git switch lab/L2.1-start                         # mulai lab
git diff lab/L2.1-start lab/L2.1-solution          # lihat jawaban lengkap
git diff lab/L2.1-start lab/L2.1-solution -- .claude/settings.json   # satu berkas saja
git restore --source lab/L2.1-solution -- .claude/hooks/          # ambil sebagian jawaban
```

## Lab

| Lab | Hari | Menit | Judul | Branch mulai | Kunci jawaban | Berisi hasil lab |
| --- | --- | --- | --- | --- | --- | --- |
| [L1.1](labs/L1.1.md) | 1 | 30 | Peta aset dan batas kepercayaan | `lab/L1.1-start` | `lab/L1.1-solution` | — |
| [L1.2](labs/L1.2.md) | 1 | 35 | Aktifkan GHAS dan triase alert | `lab/L1.2-start` | `lab/L1.2-solution` | — |
| [L1.2b](labs/L1.2b.md) | 1 | 20 | Rule Semgrep kustom | `lab/L1.2b-start` | `lab/L1.2b-solution` | L1.2 |
| [L1.3](labs/L1.3.md) | 1 | 30 | Uji push protection | `lab/L1.3-start` | `lab/L1.3-solution` | — |
| [L1.4](labs/L1.4.md) | 1 | 35 | Dependabot dan dependency review | `lab/L1.4-start` | `lab/L1.4-solution` | — |
| [L2.1](labs/L2.1.md) | 2 | 40 | Pasang pagar Claude Code | `lab/L2.1-start` | `lab/L2.1-solution` | — |
| [L2.2](labs/L2.2.md) | 2 | 35 | Prompt naif vs prompt aman | `lab/L2.2-start` | `lab/L2.2-solution` | L1.2 |
| [L2.3](labs/L2.3.md) | 2 | 40 | Remediasi alert dengan Claude | `lab/L2.3-start` | `lab/L2.3-solution` | L1.2, L2.1, L2.2 |
| [L2.3b](labs/L2.3b.md) | 2 | 25 | Loop temukan-perbaiki-verifikasi | `lab/L2.3b-start` | `lab/L2.3b-solution` | L1.2, L1.2b, L2.1, L2.2 |
| [L2.4](labs/L2.4.md) | 2 | 35 | Review keamanan otomatis di PR | `lab/L2.4-start` | `lab/L2.4-solution` | L1.2, L2.1, L2.2 |
| [L3.1](labs/L3.1.md) | 3 | 50 | Bangun agen triase | `lab/L3.1-start` | `lab/L3.1-solution` | L1.2, L2.1, L2.2 |
| [L3.2](labs/L3.2.md) | 3 | 30 | Keraskan workflow repo lab | `lab/L3.2-start` | `lab/L3.2-solution` | L1.2 |
| [L3.2b](labs/L3.2b.md) | 3 | 30 | DAST terautentikasi pada PR | `lab/L3.2b-start` | `lab/L3.2b-solution` | — |
| [L3.3](labs/L3.3.md) | 3 | 35 | Scan dan keraskan image | `lab/L3.3-start` | `lab/L3.3-solution` | — |
| [L3.3b](labs/L3.3b.md) | 3 | 25 | SBOM, provenance, tanda tangan | `lab/L3.3b-start` | `lab/L3.3b-solution` | L3.3 |
| [L3.4](labs/L3.4.md) | 3 | 35 | Gerbang IaC di CI | `lab/L3.4-start` | `lab/L3.4-solution` | L2.1, L1.2, L2.2 |
| [L4.1](labs/L4.1.md) | 4 | 35 | Kebijakan organisasi | `lab/L4.1-start` | `lab/L4.1-solution` | L2.1, L1.2, L2.2, L3.4 |
| [L4.2](labs/L4.2.md) | 4 | 30 | Laporan risiko mingguan | `lab/L4.2-start` | `lab/L4.2-solution` | — |
| [L4.3](labs/L4.3.md) | 4 | 35 | Terapkan zero-trust di repo lab | `lab/L4.3-start` | `lab/L4.3-solution` | L1.2, L3.2, L2.1, L2.2, L3.4 |
| [L4.4](labs/L4.4.md) | 4 | 90 | Capstone: pipeline end-to-end | `lab/L4.4-start` | `lab/L4.4-solution` | semua lab Hari 1–4 |

## Branch bantu (PR uji)

Dibuat sebagai commit di atas branch induknya. Buka PR dari branch bantu **ke** branch induk,
maka diff PR hanya berisi perubahan uji itu.

| Branch | Induk (base PR) | Dipakai di | Isi |
| --- | --- | --- | --- |
| `pr/L1.4-pr-dependensi-lama` | `lab/L1.4-solution` | L1.4 langkah 3 | Menambah `urllib3==1.26.4` (punya advisory high) ke `api/requirements.txt` |
| `pr/L2.2-contoh-naif` | `lab/L2.2-start` | L2.2 (cadangan) | Contoh hasil prompt naif `api/staff.py` untuk dibandingkan bila Claude tidak tersedia |
| `pr/L2.4-pr-xss` | `lab/L2.4-solution` | L2.4 langkah 2 | Endpoint `GET /greeting` yang rentan XSS |
| `pr/L3.1-komentar-kanari` | `lab/L3.1-solution` | L3.1 langkah 4 | Komentar kode tidak tepercaya berisi instruksi kanari `KANARI-L31` |
| `pr/L4.3-pr-bidi` | `lab/L4.3-solution` | L4.3 langkah 2 | Berkas berisi karakter bidi dan zero-width tersembunyi |

## Alias demo

| Branch | Sama dengan |
| --- | --- |
| `demo/settings` | `lab/L2.1-solution` |

## Riwayat main

`main` berisi tiga commit. Commit kedua ("Tambah integrasi gateway pembayaran") menanam
API key palsu `kopikita_live_0011…ddee` yang hanya ada di histori, untuk latihan alert
secret scanning di Lab L1.3.

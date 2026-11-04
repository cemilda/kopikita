# Panduan lab

## Cara mengerjakan setiap lab

Satu pola untuk semua lab, supaya peserta yang tertinggal bisa langsung menyusul.

```bash
git fetch origin
git switch lab/<ID>-start            # titik mulai lab (sudah berisi hasil lab prasyarat)
git switch -c kerja/<ID>             # branch kerja Anda sendiri
# ... kerjakan langkah lab ...
git push -u origin kerja/<ID>
```

**Lab yang memakai fitur GitHub** (code scanning, Dependabot, workflow terjadwal, ruleset,
CODEOWNERS): jadikan `lab/<ID>-start` sebagai *default branch* fork Anda dulu, lalu buka PR
`kerja/<ID>` → `lab/<ID>-start`.

> **Settings → General → Default branch → ⇄ → pilih `lab/<ID>-start` → Update.**

Alasannya: beberapa fitur GitHub hanya membaca default branch. Dependabot memakai manifest dan
`dependabot.yml` di default branch. Workflow terjadwal dan tombol *Run workflow* butuh berkas
workflow di default branch. Ruleset `~DEFAULT_BRANCH` juga mengikuti default branch. Pindah
default branch tidak menghapus apa pun dan bisa dikembalikan kapan saja.

**Mencocokkan jawaban.**

```bash
git diff lab/<ID>-start lab/<ID>-solution               # seluruh jawaban
git diff kerja/<ID> lab/<ID>-solution -- api/app.py     # bandingkan hasil Anda per berkas
```

Hasil Claude tidak akan identik dengan kunci jawaban. Yang dinilai adalah sifatnya:
apakah kerentanannya tertutup, test negatifnya ada, test lama tidak dilemahkan, dan izinnya minimal.

**Prasyarat laptop:** Git, Python 3.10+ (CI memakai 3.11), Node.js 18+, Docker, GitHub CLI `gh`
yang sudah login, dan Claude Code. Pengguna Windows memakai WSL2. Pertama kali clone, jalankan
`bash scripts/setup-lab.sh` (membuat `.venv`, `.env` palsu, database, dan menjalankan test).

**Secret repo yang dipakai di beberapa lab** (Settings → Secrets and variables → Actions):
`ANTHROPIC_API_KEY` (L2.4, L3.2, capstone), dan opsional `HAWK_API_KEY` + `HAWK_APP_ID` (L3.2b).
Memakai API key berarti biaya token; matikan workflow yang tidak dipakai setelah kelas.

## Daftar lab

| Lab | Sesi | Menit | Format | Judul |
| --- | --- | --- | --- | --- |
| [L1.1](L1.1.md) | Sesi 1.1 | 30 | Berpasangan | Peta aset dan batas kepercayaan |
| [L1.2](L1.2.md) | Sesi 1.2 | 35 | Individu | Aktifkan GHAS dan triase alert |
| [L1.2b](L1.2b.md) | Sesi 1.2 | 20 | Berpasangan | Rule Semgrep kustom |
| [L1.3](L1.3.md) | Sesi 1.3 | 30 | Individu | Uji push protection |
| [L1.4](L1.4.md) | Sesi 1.4 | 35 | Individu | Dependabot dan dependency review |
| [L2.1](L2.1.md) | Sesi 2.1 | 40 | Individu | Pasang pagar Claude Code |
| [L2.2](L2.2.md) | Sesi 2.2 | 35 | Berpasangan | Prompt naif vs prompt aman |
| [L2.3](L2.3.md) | Sesi 2.3 | 40 | Individu | Remediasi alert dengan Claude |
| [L2.3b](L2.3b.md) | Sesi 2.3 | 25 | Individu | Loop temukan-perbaiki-verifikasi |
| [L2.4](L2.4.md) | Sesi 2.4 | 35 | Individu | Review keamanan otomatis di PR |
| [L3.1](L3.1.md) | Sesi 3.1 | 50 | Berpasangan | Bangun agen triase |
| [L3.2](L3.2.md) | Sesi 3.2 | 30 | Individu | Keraskan workflow repo lab |
| [L3.2b](L3.2b.md) | Sesi 3.2 | 30 | Berpasangan | DAST terautentikasi pada PR |
| [L3.3](L3.3.md) | Sesi 3.3 | 35 | Individu | Scan dan keraskan image |
| [L3.3b](L3.3b.md) | Sesi 3.3 | 25 | Individu | SBOM, provenance, tanda tangan |
| [L3.4](L3.4.md) | Sesi 3.4 | 35 | Individu | Gerbang IaC di CI |
| [L4.1](L4.1.md) | Sesi 4.1 | 35 | Berkelompok | Kebijakan organisasi |
| [L4.2](L4.2.md) | Sesi 4.2 | 30 | Individu | Laporan risiko mingguan |
| [L4.3](L4.3.md) | Sesi 4.3 | 35 | Individu | Terapkan zero-trust di repo lab |
| [L4.4](L4.4.md) | Capstone | 90 | Berkelompok | Capstone: pipeline end-to-end |

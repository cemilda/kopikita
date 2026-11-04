# Rubrik penilaian capstone (Lab L4.4)

Empat bagian, masing-masing 25%.

| Bagian | Kriteria | Nilai |
| --- | --- | --- |
| Pagar aktif (25%) | Kanari `KANARI-L44` di issue tidak dijalankan; deny rule `.env` dan sandbox aktif; bukti di log hook dan diff PR | |
| Alur PR (25%) | PR lewat CodeQL, review Claude, Trivy, Checkov, dependency review, hidden-chars, policy | |
| Agen triase aman (25%) | PR draft dibuat agen, token tanpa hak merge, test lulus, direview manusia | |
| Presentasi & bukti (25%) | Checklist OWASP 14 bagian diisi; bukti konkret ditunjukkan | |

## Checklist OWASP Secure Coding with AI (14 bagian)

- [ ] §1 Dependensi halusinasi diverifikasi
- [ ] §2 Dependensi usang ber-CVE ditangani (Dependabot + review)
- [ ] §3 Prompt injection ditahan (issue beracun)
- [ ] §4 MCP/tool dibatasi allowlist
- [ ] §5 Sandbox aktif
- [ ] §6 `CLAUDE.md`/rules files di bawah CODEOWNERS
- [ ] §7 Edit di luar scope ditinjau per berkas
- [ ] §8 Test tidak dilemahkan/dihapus
- [ ] §9 `.env` dan rahasia tidak terbaca agen
- [ ] §10 Berkas build/CI ditinjau ketat + pin SHA
- [ ] §11 Agen CI berizin minimal
- [ ] §12 Karakter bidi/zero-width dipindai
- [ ] §13 Batas sub-agen dijaga
- [ ] §14 Setiap patch AI punya pemilik manusia

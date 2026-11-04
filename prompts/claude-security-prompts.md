# Pustaka prompt aman untuk Claude

Dipakai di Lab L2.2 dan seterusnya. Diadaptasi dari pustaka prompt Copilot di Modul 04 repo
paulasilvatech/Secure-Code-AI-Dev (lisensi MIT), lalu diubah menjadi prompt Claude: lebih panjang,
berkonteks, menyebut ancaman, dan meminta test.

## Pola umum (pakai di setiap kategori)

1. Mulai di **plan mode** (Shift+Tab sampai mode Plan). Setujui rencana dulu, baru izinkan edit.
2. Sebut ancaman yang relevan secara eksplisit.
3. Beri contoh buruk yang tidak boleh ditiru di dalam tag `<contoh_buruk>`.
4. Minta **test negatif**: input jahat, token kedaluwarsa, payload rusak.
5. Minta penjelasan: "sebutkan keputusan keamanan dan alasannya".

Kerangka:

```text
<konteks>
Repo kopikita-vuln, API Flask di api/, test pytest di tests/. Ikuti aturan di CLAUDE.md.
</konteks>
<tugas>...</tugas>
<batasan>
- Query SQL selalu berparameter (tanda ?), tidak pernah disusun dengan string.
- Input dari request tidak tepercaya; validasi di batas sistem.
- Jangan menulis password, token, atau isi .env ke log maupun respons.
</batasan>
<contoh_buruk>
cur.execute("SELECT * FROM users WHERE username = '" + username + "'")
</contoh_buruk>
<kriteria_selesai>
- Test fungsional dan test negatif lulus (pytest -q).
- Sebutkan keputusan keamanan dan alasannya.
</kriteria_selesai>
```

## Prompt per kategori

| Kategori | Prompt untuk Claude |
| --- | --- |
| Validasi input | Validasi form registrasi; cegah SQL injection dan XSS; tulis test input jahat. |
| Auth & otorisasi | Middleware JWT dengan refresh token; tolak token kedaluwarsa; tulis test-nya. |
| Data sensitif | Redaksi PII sebelum logging; buktikan dengan test log. |
| Kriptografi | Hash password dengan algoritme lambat (argon2, bcrypt, scrypt, atau PBKDF2-SHA256 600.000 iterasi); jangan buat algoritme sendiri. |
| Keamanan API | Rate limit login untuk mencegah brute force; uji batasnya. |
| Error handling | Log detail di server, pesan aman ke klien; tanpa stack trace. |

## Contoh lengkap: endpoint login staf (Lab L2.2, branch aman)

```text
<konteks>Repo kopikita-vuln. Tambahkan blueprint baru api/staff.py untuk login staf (barista).</konteks>
<tugas>Buat endpoint POST /staff/login yang menerima JSON {"username", "password"}.</tugas>
<batasan>
- Query berparameter; jangan menyusun SQL dengan string.
- Simpan dan verifikasi password dengan werkzeug.security (PBKDF2-SHA256, 600.000 iterasi).
- Rate limit: maksimal 5 percobaan gagal per username per 15 menit, lalu 429.
- Jangan mencatat password ke log; pesan error sama untuk username dan password yang salah.
</batasan>
<contoh_buruk>
log.info(f"login {username} {password}")
</contoh_buruk>
<kriteria_selesai>
Test: login benar 200, password salah 401, injeksi "' OR '1'='1' --" 401, percobaan ke-6 429,
password tidak muncul di log (pakai caplog). Jelaskan keputusan keamanannya.
</kriteria_selesai>
```

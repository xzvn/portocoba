# Deploy Portofolio Flask ke Vercel

Proyek ini memakai Flask, TiDB Cloud, Cloudinary, dan Resend. Database harus sudah dibuat dan diisi sebelum halaman utama digunakan.

## 1. Uji lokal

Di Windows PowerShell:

```powershell
cd E:\path\ke\portfolio_stitch
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy .env.example .env
```

Isi `.env`, kemudian:

```powershell
python scripts\check_connection.py
python scripts\init_db.py
python -m pytest -q
python app.py
```

## 2. Push versi siap deploy ke GitHub

```powershell
git status
git add .
git commit -m "Siapkan deployment Vercel"
git push origin main
```

Pastikan `.env` tidak muncul pada `git status` dan tidak ada di GitHub.

## 3. Deploy lewat Dashboard Vercel

1. Buka Vercel dan pilih **Add New → Project**.
2. Import repository `nelvinjovanm-oss/portofolio-nelvin`.
3. Root Directory: folder yang berisi `app.py` dan `vercel.json`.
4. Framework Preset: biarkan terdeteksi sebagai Flask/Python atau pilih **Other**.
5. Jangan isi Build Command dan Output Directory.
6. Tambahkan semua Environment Variables pada bagian berikut.
7. Klik **Deploy**.

## 4. Environment Variables wajib

Tambahkan untuk Production. Untuk Preview, gunakan database terpisah bila tersedia.

```text
SECRET_KEY
TIDB_HOST
TIDB_PORT
TIDB_USERNAME
TIDB_PASSWORD
TIDB_DATABASE
ADMIN_EMAIL
ADMIN_PASSWORD
CLOUDINARY_CLOUD_NAME
CLOUDINARY_API_KEY
CLOUDINARY_API_SECRET
RESEND_API_KEY
RESEND_FROM
CONTACT_RECEIVER_EMAIL
```

Buat `SECRET_KEY` dengan:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Set `FLASK_ENV=production` bila ingin menjalankan konfigurasi produksi secara eksplisit. Vercel juga otomatis menyediakan `VERCEL_ENV=production` pada deployment produksi.

## 5. Deploy lewat CLI (opsional)

Karena PowerShell Anda sebelumnya memblokir file `.ps1`, gunakan executable `.cmd`:

```powershell
npm.cmd install -g vercel
vercel.cmd login
vercel.cmd link
vercel.cmd deploy
vercel.cmd deploy --prod
```

Environment Variables lebih aman dimasukkan melalui Dashboard Vercel daripada ditempel langsung ke command history.

## 6. Pemeriksaan setelah deployment

Buka:

```text
https://NAMA-PROJECT.vercel.app/health
```

Respons yang benar:

```json
{"app":"minimalist-portfolio","status":"ok"}
```

Kemudian periksa halaman utama, `/admin/login`, upload gambar, upload CV, penyimpanan pesan, dan email Resend.

## 7. Jika terjadi error

- `500` saat halaman utama: biasanya Environment Variables TiDB belum lengkap, database belum diinisialisasi, atau koneksi TiDB ditolak.
- `FUNCTION_INVOCATION_TIMEOUT`: cek koneksi TiDB/Cloudinary/Resend. Fungsi telah diberi batas 30 detik.
- `FUNCTION_PAYLOAD_TOO_LARGE`: file upload melewati batas Vercel 4,5 MB; aplikasi membatasi upload menjadi 4 MB.
- CSS/gambar tidak tampil: pastikan folder `public/` berada di root proyek.
- Login gagal: jalankan kembali `scripts/init_db.py` dengan database yang sama, atau ubah password hash admin di database.

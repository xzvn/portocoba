# Minimalist Professional Portfolio

Proyek Flask satu halaman yang mengikuti mockup `stitch_minimalist_professional_portfolio_web_design`: hero editorial, about, skill cards, timeline pengalaman, project cards, contact form, dan CMS admin.

## Teknologi

- Flask + Jinja
- TiDB Cloud melalui SQLAlchemy dan PyMySQL
- Cloudinary untuk foto profil, gambar about, gambar proyek, dan CV PDF
- Resend untuk notifikasi formulir kontak
- Vercel Python Runtime

## Struktur penting

```text
app.py                         entrypoint lokal dan Vercel
portfolio/                     kode backend Flask
portfolio/templates/           halaman publik, login, dan admin
public/                        CSS, JavaScript, dan gambar statis untuk CDN Vercel
scripts/init_db.py             membuat tabel, admin, dan data awal mockup
.env.example                   contoh variabel lingkungan
vercel.json                    batas waktu fungsi Vercel
```

## Menjalankan lokal

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Isi `.env`, lalu jalankan:

```powershell
python scripts\init_db.py
python app.py
```

Buka `http://127.0.0.1:5000` dan admin di `http://127.0.0.1:5000/admin/login`.

## Urutan setup layanan

1. Buat cluster TiDB Cloud dan database bernama `portfolio`.
2. Salin host, port, username, dan password ke `.env`.
3. Buat akun Cloudinary dan salin cloud name, API key, serta API secret.
4. Buat API key Resend. Untuk produksi, verifikasi domain dan gunakan alamat pengirim dari domain tersebut.
5. Jalankan `python scripts\init_db.py` satu kali dengan koneksi TiDB aktif.
6. Login ke admin dan ganti seluruh data contoh serta unggah foto dan CV.

## Deploy Vercel

1. Push folder proyek ke GitHub.
2. Import repository dari dashboard Vercel.
3. Tambahkan semua variabel dari `.env` pada Project Settings → Environment Variables.
4. Deploy. Vercel menemukan instance Flask bernama `app` dari `app.py`.
5. Periksa `/health`, halaman utama, login admin, upload Cloudinary, dan formulir kontak.

Catatan: direktori `public/` dipakai agar CSS, JavaScript, dan gambar statis dilayani oleh CDN Vercel.

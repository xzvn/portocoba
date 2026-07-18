# Panduan Lengkap: Portofolio Flask + TiDB + Cloudinary + Resend + Vercel

Panduan ini memakai Windows PowerShell atau Command Prompt. Proyek sudah dibuat mengikuti mockup Stitch: navbar fixed, hero dua kolom, bagian about, kartu skill, timeline, proyek, kontak, dan footer.

## 1. Persiapan

Pastikan tersedia:

- Python 3.12 atau 3.13
- Git
- VS Code
- akun GitHub
- akun TiDB Cloud
- akun Cloudinary
- akun Resend
- akun Vercel

Cek instalasi:

```powershell
python --version
git --version
```

## 2. Membuka proyek

Ekstrak ZIP, lalu buka terminal pada folder proyek:

```powershell
cd path\ke\portfolio_stitch
```

Buat virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Instal dependency:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Menyiapkan TiDB Cloud

1. Masuk ke TiDB Cloud.
2. Buat cluster Starter atau gunakan cluster yang sudah ada.
3. Buka cluster, lalu pilih **Connect**.
4. Pilih Public Endpoint dan General.
5. Salin host, port, username, dan password.
6. Buat database:

```sql
CREATE DATABASE portfolio
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Anda dapat menjalankan SQL tersebut lewat SQL Editor TiDB Cloud.

## 4. Menyiapkan file `.env`

Salin contoh konfigurasi:

```powershell
copy .env.example .env
```

Isi nilai berikut:

```env
SECRET_KEY=random-string-yang-panjang-dan-rahasia
FLASK_ENV=development

TIDB_HOST=host-dari-tidb
TIDB_PORT=4000
TIDB_USERNAME=username-dari-tidb
TIDB_PASSWORD=password-dari-tidb
TIDB_DATABASE=portfolio

ADMIN_EMAIL=email-admin-anda
ADMIN_PASSWORD=password-admin-yang-kuat
```

Untuk membuat `SECRET_KEY`:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Jangan upload `.env` ke GitHub.

## 5. Menguji koneksi TiDB

```powershell
python scripts\check_connection.py
```

Hasil yang benar:

```text
Koneksi database berhasil. Hasil SELECT 1 = 1
```

Jika gagal, periksa host, username, password, database, dan izin koneksi publik pada TiDB.

## 6. Membuat tabel dan admin

Jalankan satu kali:

```powershell
python scripts\init_db.py
```

Script ini membuat tabel:

- users
- profiles
- skills
- experiences
- projects
- contact_messages

Script juga memasukkan data awal sesuai mockup dan membuat akun admin dari `.env`.

## 7. Menjalankan website lokal

```powershell
python app.py
```

Buka:

```text
Website: http://127.0.0.1:5000
Admin:   http://127.0.0.1:5000/admin/login
Health:  http://127.0.0.1:5000/health
```

Login menggunakan `ADMIN_EMAIL` dan `ADMIN_PASSWORD` dari `.env`.

## 8. Mengatur Cloudinary

1. Masuk ke Cloudinary Console.
2. Buka dashboard produk Programmable Media.
3. Salin Cloud Name, API Key, dan API Secret.
4. Masukkan ke `.env`:

```env
CLOUDINARY_CLOUD_NAME=nama-cloud
CLOUDINARY_API_KEY=api-key
CLOUDINARY_API_SECRET=api-secret
```

Upload yang tersedia pada halaman admin:

- foto hero
- foto about
- gambar proyek
- CV PDF

Gambar contoh lokal hanya digunakan sebelum Anda mengunggah gambar sendiri.

## 9. Mengatur Resend

1. Masuk ke Resend.
2. Buat API key.
3. Untuk produksi, tambahkan dan verifikasi domain Anda.
4. Isi `.env`:

```env
RESEND_API_KEY=re_xxxxxxxxx
RESEND_FROM=Portfolio <hello@domain-anda.com>
CONTACT_RECEIVER_EMAIL=email-penerima@gmail.com
```

Saat pengunjung mengirim formulir kontak:

1. pesan disimpan ke tabel `contact_messages`;
2. pesan tampil pada dashboard admin;
3. Resend mengirim notifikasi ke `CONTACT_RECEIVER_EMAIL`.

Jika Resend belum dikonfigurasi, pesan tetap disimpan ke database tetapi notifikasi email tidak terkirim.

## 10. Mengganti isi portofolio

Login admin lalu ubah:

### Profil

- nama brand
- nama lengkap
- headline
- ipsi hero
- about
- lokasi
- pendidikan
- status kerja
- email dan telepon
- GitHub dan LinkedIn
- foto hero dan about
- CV PDF

### Skills

Setiap kartu skill memiliki:

- kategori
- ikon Material Symbols
- daftar kemampuan
- urutan

Contoh nama ikon:

```text
code
database
brush
construction
settings_ethernet
```

### Experience & Education

Isi periode, jabatan atau pendidikan, organisasi, deskripsi, tipe, dan urutan.

### Projects

Isi judul, deskripsi, teknologi, gambar, live URL, source-code URL, featured, dan urutan.

## 11. Push ke GitHub

Pastikan `.env` tidak ikut:

```powershell
git status
```

Lalu:

```powershell
git init
git add .
git commit -m "Initial portfolio project"
git branch -M main
git remote add origin https://github.com/USERNAME/NAMA-REPO.git
git push -u origin main
```

## 12. Deploy ke Vercel

1. Masuk ke Vercel.
2. Pilih **Add New → Project**.
3. Import repository GitHub.
4. Biarkan framework menggunakan deteksi otomatis.
5. Tambahkan Environment Variables berikut untuk Production, Preview, dan Development:

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

6. Klik **Deploy**.

Vercel membaca objek `app` dari `app.py`. File CSS, JavaScript, dan gambar berada pada folder `public/` agar dilayani sebagai aset statis Vercel.

## 13. Pemeriksaan setelah deploy

Buka:

```text
https://domain-vercel-anda.vercel.app/health
```

Harus menghasilkan:

```json
{"app":"minimalist-portfolio","status":"ok"}
```

Lalu uji:

1. halaman utama terbuka;
2. CSS dan gambar terbaca;
3. `/admin/login` dapat digunakan;
4. data admin berasal dari TiDB;
5. upload gambar masuk ke Cloudinary;
6. formulir kontak tersimpan;
7. email notifikasi masuk melalui Resend;
8. tampilan mobile tidak terpotong.

## 14. Menggunakan domain sendiri

1. Buka Vercel Project Settings.
2. Pilih Domains.
3. Tambahkan domain.
4. Ikuti konfigurasi DNS dari Vercel.
5. Pastikan domain pengirim Resend juga sudah diverifikasi.
6. Ubah `RESEND_FROM` agar memakai domain tersebut.

## 15. Masalah umum

### `Access denied` atau `Missing user name prefix`

Gunakan username TiDB lengkap yang ditampilkan di menu Connect. Jangan menghapus prefix cluster.

### `Lost connection to MySQL server during query`

Proyek sudah mengaktifkan `pool_pre_ping` dan `pool_recycle=280`, tetapi tetap periksa status cluster dan kredensial.

### CSS tidak terbaca di Vercel

Pastikan folder bernama tepat `public/css`, dan template memakai `/css/main.css`, bukan path lokal Windows.

### Upload Cloudinary gagal

Periksa ketiga variable Cloudinary. Format gambar yang diterima: JPG, JPEG, PNG, WEBP, dan GIF. Batas file proyek adalah 8 MB.

### Resend gagal mengirim

Pastikan API key aktif, domain terverifikasi, dan alamat pada `RESEND_FROM` berasal dari domain yang diizinkan.

### Login admin gagal

Pastikan `scripts/init_db.py` dijalankan menggunakan database TiDB yang sama dengan Vercel. Jika password di `.env` diganti setelah admin dibuat, password di database tidak otomatis berubah.

Untuk mengganti password admin melalui Python shell:

```powershell
python
```

```python
from app import app
from portfolio.extensions import db
from portfolio.models import User

with app.app_context():
    user = User.query.filter_by(email="email-admin-anda").first()
    user.set_password("PasswordBaruYangKuat123!")
    db.session.commit()
```

## 16. File yang paling sering diedit

```text
portfolio/templates/public/home.html   struktur halaman publik
public/css/main.css                    tampilan desktop
public/css/responsive.css              tampilan tablet dan mobile
portfolio/routes/public.py             halaman dan formulir kontak
portfolio/routes/admin.py              fitur CMS admin
portfolio/models.py                    struktur tabel
scripts/init_db.py                     data awal
```

# Backend — Socket App

Backend aplikasi Socket App berbasis **Flask (Python)**, mengimplementasikan:
- REST API untuk autentikasi (register, login, verifikasi email)
- **TCP Socket Server** untuk upload file
- **UDP Socket Server** untuk streaming video

---

## Struktur Folder

```
backend/
├── app.py                  # Entry point: jalankan Flask + TCP server + UDP server
├── config.py               # Konfigurasi port, path folder, environment variable
├── requirements.txt
├── .env                    # Kredensial (tidak di-commit ke Git)
│
├── routes/
│   ├── auth_routes.py      # Endpoint: /api/auth/register, /login, /verify
│   └── file_routes.py      # Endpoint: /api/file/upload, /list, /videos, /stream
│
├── sockets/
│   ├── tcp_server.py       # Raw TCP socket server (terima file upload)
│   └── udp_server.py       # Raw UDP socket server (kirim video chunk)
│
├── models/
│   └── user.py             # Setup SQLite & helper fungsi database
│
├── utils/
│   ├── auth_utils.py       # Hash password, generate token verifikasi
│   └── email_utils.py      # Kirim email verifikasi via SMTP Gmail
│
└── storage/
    ├── uploads/            # Hasil file dari TCP upload (auto-generated)
    ├── videos/             # Video sumber untuk UDP streaming (isi manual)
    └── app.db              # Database SQLite (auto-generated)
```

---

## Requirement

- Python 3.9+
- pip

---

## Setup & Menjalankan

### 1. Clone / masuk ke folder backend

```bash
cd backend
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Buat file `.env`

Buat file `.env` di dalam folder `backend/` dengan isi:

```env
SECRET_KEY=ganti-dengan-string-acak-bebas
EMAIL_USER=emailkamu@gmail.com
EMAIL_PASS=app-password-16-digit-dari-google
FRONTEND_URL=http://localhost:3000
```

> **Catatan Gmail App Password:** buka [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords), buat App Password baru, salin 16 digit yang muncul ke `EMAIL_PASS`. Ini bukan password akun Gmail biasa.

### 4. Buat folder storage (jika belum ada)

```bash
mkdir -p storage/uploads storage/videos
```

### 5. Taruh video untuk streaming

Salin minimal 1 file video (`.mp4`) ke folder `storage/videos/` secara manual. Video ini yang akan disajikan di halaman streaming.

### 6. Jalankan server

```bash
python app.py
```

Saat berhasil, terminal akan menampilkan:

```
TCP server listening di 0.0.0.0:9001
UDP server listening di 0.0.0.0:9002
Flask jalan di http://localhost:5000
```

Ketiga server (Flask, TCP, UDP) berjalan sekaligus dalam satu proses.

---

## Port yang Digunakan

| Server | Port | Protokol |
|---|---|---|
| Flask (Web API) | 5000 | HTTP |
| TCP Server | 9001 | TCP |
| UDP Server | 9002 | UDP |

---

## Endpoint API

### Auth

| Method | Endpoint | Keterangan |
|---|---|---|
| POST | `/api/auth/register` | Daftar akun baru, kirim email verifikasi |
| POST | `/api/auth/login` | Login dengan email & password |
| GET | `/api/auth/verify?token=xxx` | Verifikasi akun lewat token dari email |

### File & Stream

| Method | Endpoint | Keterangan |
|---|---|---|
| POST | `/api/file/upload` | Upload file lewat TCP |
| GET | `/api/file/list` | Daftar file yang sudah diupload |
| GET | `/api/file/videos` | Daftar video yang tersedia untuk streaming |
| GET | `/api/file/stream/<filename>` | Stream video lewat UDP |

---

## Catatan

- Database SQLite (`storage/app.db`) dibuat otomatis saat pertama kali `python app.py` dijalankan.
- Jika muncul error `Address already in use` pada port TCP/UDP, pastikan tidak ada proses Python lain yang masih jalan di background.
- Karena Flask dijalankan dengan `debug=True`, hindari menggunakan `use_reloader=True` bersamaan dengan thread TCP/UDP karena akan menyebabkan port bentrok. Jika perlu matikan reloader: ubah `app.run(..., debug=True)` menjadi `app.run(..., debug=True, use_reloader=False)`.

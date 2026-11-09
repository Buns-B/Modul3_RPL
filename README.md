# Sistem Manajemen Perpustakaan

Aplikasi desktop manajemen koleksi buku perpustakaan yang dibangun dengan Python menggunakan pola arsitektur **Model-View-Controller (MVC)**. Antarmuka dibuat dengan **CustomTkinter** dan data disimpan di basis data **MySQL**.

## Deskripsi Singkat

Aplikasi ini membantu petugas perpustakaan mengelola data buku dan membatasi akses sesuai peran pengguna.

Fitur utama:

- **Autentikasi pengguna**: login dengan username dan password. Password tidak disimpan sebagai teks biasa, melainkan di-hash dengan SHA-256, dan verifikasi memakai *parameterized query* untuk mencegah SQL Injection.
- **Otorisasi berbasis peran (RBAC)**:
  - `admin` dapat menambah, memperbarui, dan menghapus data buku.
  - `anggota` hanya dapat melihat daftar koleksi (read-only). Form input serta tombol Simpan, Update, dan Hapus dinonaktifkan.
- **Manajemen data buku (CRUD)**: judul, penulis, dan tahun terbit.
- **Logout**: menutup jendela utama dan kembali ke jendela login.
- **CI/CD**: pengujian otomatis dengan pytest dan pengecekan kode dengan flake8 melalui GitHub Actions, serta pemaketan menjadi berkas `.exe` dengan PyInstaller.

## Struktur Direktori MVC

```
Modul3_RPL/
├── .github/
│   └── workflows/
│       └── ci_pipeline.yml      # Pipeline CI GitHub Actions
├── config/
│   └── database.py              # Konfigurasi dan koneksi MySQL
├── models/                      # MODEL: akses data dan logika bisnis
│   ├── buku_model.py            # Operasi CRUD tabel buku
│   └── user_model.py            # Hashing password dan autentikasi
├── views/                       # VIEW: tampilan antarmuka
│   ├── login_view.py            # Jendela login
│   └── buku_view.py             # Jendela utama data buku
├── controllers/                 # CONTROLLER: penghubung model dan view
│   ├── auth_controller.py       # Alur login
│   └── buku_controller.py       # Alur data buku dan otorisasi role
├── tests/                       # Pengujian unit (pytest)
│   ├── test_auth.py
│   └── test_buku.py
├── main.py                      # Titik masuk aplikasi
├── requirements.txt             # Daftar dependensi
└── README.md
```

Pembagian tanggung jawab:

| Komponen | Tanggung jawab |
|---|---|
| Model | Menjalankan query ke MySQL dan mengembalikan data (termasuk role pengguna). |
| View | Menampilkan antarmuka dan menyediakan widget (entry, tombol, tabel). |
| Controller | Menghubungkan view dengan model, mengatur alur aplikasi, dan menerapkan otorisasi berdasarkan role. |

## Panduan Instalasi dan Konfigurasi Database MySQL

### 1. Prasyarat

- Python 3.11 atau lebih baru
- MySQL Server (misalnya melalui [Laragon](https://laragon.org/)) dan layanan MySQL sedang berjalan
- Git

### 2. Mengunduh Proyek

```bash
git clone https://github.com/Buns-B/Modul3_RPL.git
cd Modul3_RPL
```

### 3. Membuat Virtual Environment dan Memasang Dependensi

```powershell
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
```

### 4. Membuat Basis Data dan Tabel

Masuk ke MySQL:

```bash
mysql -u root -p
```

Lalu jalankan:

```sql
CREATE DATABASE IF NOT EXISTS perpustakaan;
USE perpustakaan;

CREATE TABLE IF NOT EXISTS buku (
    id_buku INT PRIMARY KEY AUTO_INCREMENT,
    judul VARCHAR(255) NOT NULL,
    penulis VARCHAR(255) NOT NULL,
    tahun_terbit INT NOT NULL
);

CREATE TABLE IF NOT EXISTS anggota (
    id_anggota INT PRIMARY KEY AUTO_INCREMENT,
    nama VARCHAR(100) NOT NULL,
    alamat VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS peminjaman (
    id_pinjam INT PRIMARY KEY AUTO_INCREMENT,
    id_buku INT NOT NULL,
    id_anggota INT NOT NULL,
    tanggal_pinjam DATE NOT NULL,
    tanggal_kembali DATE NULL
);

CREATE TABLE IF NOT EXISTS users (
    id_user INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'anggota') NOT NULL DEFAULT 'anggota'
);

-- Akun uji coba (password disimpan dalam bentuk hash SHA-256)
INSERT INTO users (username, password, role) VALUES
('petugas', SHA2('admin123', 256), 'admin'),
('mahasiswa', SHA2('user123', 256), 'anggota');
```

### 5. Mengatur Koneksi Database

Pengaturan koneksi berada di `config/database.py`, di dalam class `Database`. Nilai bawaannya cocok untuk instalasi Laragon standar:

| Pengaturan | Nilai bawaan |
|---|---|
| `host` | `localhost` |
| `db_name` | `perpustakaan` |
| `username` | `root` |
| `password` | (kosong) |

Jika MySQL di komputer Anda memakai user atau password yang berbeda, ubah nilai tersebut di `config/database.py`. Port yang dipakai adalah port bawaan MySQL (`3306`).

## Cara Menjalankan Aplikasi

Pastikan MySQL sudah menyala, lalu jalankan dari root proyek:

```bash
python main.py
```

Jendela login akan muncul. Akun uji coba:

| Username | Password | Role |
|---|---|---|
| `petugas` | `admin123` | admin |
| `mahasiswa` | `user123` | anggota |

> Akun di atas hanya untuk uji coba. Ganti password sebelum aplikasi dipakai sungguhan.

### Menjalankan Pengujian

```bash
python -m pytest tests -v
```

### Membuat Berkas Eksekusi (.exe)

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --name "AplikasiPerpustakaan" main.py
```

Hasilnya berada di `dist/AplikasiPerpustakaan.exe`. Berkas tersebut tetap membutuhkan MySQL yang menyala dan basis data `perpustakaan` yang sudah dibuat.

Berkas siap pakai juga tersedia di halaman **Releases** repositori ini.

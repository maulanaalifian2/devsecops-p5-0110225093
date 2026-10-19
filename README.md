# Task Manager API (devsecops-p5-NIM)

## 1. Nama Aplikasi & Fungsi
**Task Manager API** adalah REST API sederhana untuk mengelola daftar tugas
(membuat, melihat, mengubah, menghapus, dan memfilter tugas berdasarkan status
selesai) dilengkapi **antarmuka web** interaktif di `http://127.0.0.1:5000/`.
Data disimpan di memori sehingga mudah dijalankan untuk keperluan praktikum
DevSecOps.

## 2. Bahasa / Framework
- Python 3.11
- Flask 3.0 (web framework)
- pytest (unit test)
- Bandit (SAST tool)
- GitHub Actions (CI/CD)

## 3. Cara Menjalankan
```bash
# 1. Buat virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependensi
pip install -r requirements.txt

# 3. Jalankan aplikasi, lalu buka http://127.0.0.1:5000 di browser
python -m app.main

# 4. Jalankan unit test
python -m pytest -v
```

Contoh pemakaian:
```bash
curl -X POST http://127.0.0.1:5000/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "Belajar DevSecOps"}'
curl http://127.0.0.1:5000/tasks
```

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | / | Halaman antarmuka web |
| GET | /health | Cek status aplikasi |
| GET | /tasks?done=true | Daftar tugas (filter opsional) |
| POST | /tasks | Buat tugas baru |
| GET | /tasks/<id> | Detail tugas |
| PUT | /tasks/<id> | Ubah tugas |
| DELETE | /tasks/<id> | Hapus tugas |

## 4. Overview Pipeline CI/CD
File: `.github/workflows/devsecops.yml`

**Trigger:** `push` dan `pull_request` ke branch `main`.

| Job | Runner | Fungsi |
|---|---|---|
| `build` | ubuntu-latest | Install dependensi dan jalankan unit test (pytest) |
| `sast-scan` | ubuntu-latest | Jalankan Bandit pada folder `app/`, unggah laporan, terapkan Quality Gate |

`sast-scan` memakai `needs: build`, sehingga hanya berjalan jika build dan test
berhasil.

**Quality Gate:** pipeline GAGAL jika Bandit menemukan kerentanan dengan
severity **HIGH**. Laporan lengkap (semua severity) tersimpan sebagai artifact
`bandit-report`.

Catatan: pengujian trigger pull_request.

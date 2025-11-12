📄 PDF OCR Streaming to JSON Tree
Aplikasi ini mengekstrak teks dari PDF menggunakan OCR (Tesseract + Poppler), lalu menampilkan hasilnya secara real-time per halaman melalui SSE (Server-Sent Events). Cocok untuk digitalisasi dokumen besar seperti SOTK, struktur organisasi, laporan teknis, atau arsip pemerintahan.

🚀 Fitur Utama
📤 Upload file PDF

🧠 OCR per halaman menggunakan Tesseract

🔄 Streaming hasil OCR via SSE (real-time)

🌳 Output JSON bertingkat (struktur per halaman)

📥 Unduh hasil JSON lengkap

🖼️ Tampilan HTML interaktif dengan progress bar

🛠️ Persiapan di PC
Sebelum menjalankan aplikasi, pastikan Anda sudah menginstal:

Python 3.11+ Unduh dari python.org.

Tesseract OCR

Windows: install dari UB Mannheim Tesseract installer.

Linux:

bash
sudo apt-get install tesseract-ocr
MacOS:

bash
brew install tesseract
Poppler (untuk konversi PDF ke image)

Windows: unduh Poppler for Windows, lalu set path di config.py.

Linux:

bash
sudo apt-get install poppler-utils
MacOS:

bash
brew install poppler
Dependensi Python Install dari requirements.txt:

bash
pip install -r requirements.txt
📦 Struktur Folder
Code
pdf-ocr-page/
├── app.py              # Flask backend
├── config.py           # Konfigurasi modular
├── templates/
│   └── index.html      # Frontend SSE + upload
├── requirements.txt    # Dependensi Python
├── Dockerfile          # Container build
└── docker-compose.yml  # Deployment stack
⚙️ Konfigurasi
Atur di config.py atau environment variable:

python
POPPLER_PATH = "/usr/bin"
TESSERACT_PATH = "/usr/bin/tesseract"
OCR_LANG = "ind"
BATCH_SIZE = 100
STREAM_DELAY = 0.05
FLASK_PORT = 5000
FLASK_HOST = "0.0.0.0"
DEBUG = True
LOG_FILE = "ocr_app.log"
📥 Cara Menjalankan
Opsi 1: Lokal
bash
python app.py
Lalu buka browser ke http://localhost:5000.

Opsi 2: Docker
bash
docker-compose up --build
Lalu buka http://localhost:8080.

📤 Format Output JSON
json
{
  "filename": "dokumen.pdf",
  "page_count": 3,
  "pages": [
    { "page": 1, "text": "...", "progress": 33 },
    { "page": 2, "text": "...", "progress": 66 },
    { "page": 3, "text": "...", "progress": 100 }
  ]
}
📚 Catatan Tambahan
Untuk parsing struktur organisasi dari hasil OCR, gunakan fungsi build_tree(lines) di Python atau replace \n → <br> di frontend.

Untuk membersihkan noise OCR, gunakan cleanOCRText(text) dengan modifikasi agar newline/tab tetap dipertahankan.

Pastikan path Tesseract dan Poppler sudah benar di config.py.

📜 Lisensi
Proyek ini bebas digunakan untuk keperluan edukasi, pemerintahan, dan pengembangan internal. Untuk distribusi komersial, sesuaikan dengan kebijakan instansi Anda.

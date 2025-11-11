# Konfigurasi aplikasi OCR Streaming

# Lokasi Poppler (untuk pdf2image)
POPPLER_PATH = r"D:\poppler-25.07.0\Library\bin"

# Lokasi Tesseract (opsional, jika tidak ada di PATH)
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Bahasa OCR default (bisa multi: "ind+eng")
OCR_LANG = "ind"

# Ukuran batch halaman (untuk PDF besar)
BATCH_SIZE = 100

# Delay antar halaman saat streaming (ms → 0.05 detik)
STREAM_DELAY = 0.05

# Port Flask
FLASK_PORT = 5000

# Host Flask (0.0.0.0 agar bisa diakses dari jaringan lokal)
FLASK_HOST = "0.0.0.0"

# Mode debug
DEBUG = True

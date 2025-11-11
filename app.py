from flask import Flask, request, Response, render_template, send_file, abort
from pdf2image import convert_from_path
import pytesseract
import os, tempfile, json, time

app = Flask(__name__)

# Dictionary untuk menyimpan path file berdasarkan token
UPLOADS = {}      # token -> pdf_path
DOWNLOADS = {}    # token_pageX -> json_path
FULL_JSON = {}    # token -> full_json_path

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("pdf")
    if not file:
        return "No file uploaded", 400

    # Simpan file PDF ke folder sementara
    tmpdir = tempfile.mkdtemp()
    pdf_path = os.path.join(tmpdir, file.filename)
    file.save(pdf_path)

    # Gunakan nama folder tmpdir sebagai token unik
    token = os.path.basename(tmpdir)
    UPLOADS[token] = pdf_path
    return {"token": token}

@app.route("/stream/<token>")
def stream(token):
    def generate():
        pdf_path = UPLOADS.get(token)
        if not pdf_path or not os.path.exists(pdf_path):
            yield f"data: {json.dumps({'error': 'File not found'})}\n\n"
            return

        # Konversi PDF ke gambar
        pages = convert_from_path(pdf_path, poppler_path=r"D:\poppler-25.07.0\Library\bin")
        results = []
        total = len(pages)
        tmpdir = os.path.dirname(pdf_path)

        for i, page in enumerate(pages, start=1):
            text = pytesseract.image_to_string(page, lang="ind")
            result = {"page": i, "text": text.strip(), "progress": int(i/total*100)}
            results.append(result)

            # Simpan JSON per halaman
            out_path = os.path.join(tmpdir, f"{os.path.basename(pdf_path)}.page{i}.json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            DOWNLOADS[f"{token}_page{i}"] = out_path

            # Kirim hasil ke browser via SSE
            yield f"data: {json.dumps(result, ensure_ascii=False)}\n\n"
            time.sleep(0.1)

        # Simpan JSON lengkap setelah semua halaman selesai
        full_output = {
            "filename": os.path.basename(pdf_path),
            "page_count": total,
            "pages": results
        }
        full_path = os.path.join(tmpdir, os.path.basename(pdf_path) + ".json")
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(full_output, f, indent=2, ensure_ascii=False)
        FULL_JSON[token] = full_path

    return Response(generate(), mimetype="text/event-stream")

@app.route("/download/<token>/page/<int:page>")
def download_page(token, page):
    key = f"{token}_page{page}"
    json_path = DOWNLOADS.get(key)
    if not json_path or not os.path.exists(json_path):
        abort(404)
    return send_file(json_path, as_attachment=True,
                     download_name=os.path.basename(json_path))

@app.route("/download/<token>")
def download_full(token):
    json_path = FULL_JSON.get(token)
    if not json_path or not os.path.exists(json_path):
        abort(404)
    return send_file(json_path, as_attachment=True,
                     download_name=os.path.basename(json_path))

if __name__ == "__main__":
    # Default port Flask: 5000
    # Bisa diubah sesuai kebutuhan, misalnya port 8080
    app.run(host="0.0.0.0", port=5000, debug=True)

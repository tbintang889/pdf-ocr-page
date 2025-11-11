from flask import Flask, request, Response, render_template, send_file, abort
from pdf2image import convert_from_path, pdfinfo_from_path
import pytesseract
import os, tempfile, json, time

# Import config
import config

app = Flask(__name__)

UPLOADS = {}
DOWNLOADS = {}
FULL_JSON = {}

# Set path Tesseract jika perlu
pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_PATH

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("pdf")
    if not file:
        return "No file uploaded", 400

    tmpdir = tempfile.mkdtemp()
    pdf_path = os.path.join(tmpdir, file.filename)
    file.save(pdf_path)

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

        info = pdfinfo_from_path(pdf_path, poppler_path=config.POPPLER_PATH)
        total_pages = info["Pages"]
        results = []

        for start in range(1, total_pages + 1, config.BATCH_SIZE):
            end = min(start + config.BATCH_SIZE - 1, total_pages)
            pages = convert_from_path(
                pdf_path,
                first_page=start,
                last_page=end,
                poppler_path=config.POPPLER_PATH
            )

            for i, page in enumerate(pages, start=start):
                text = pytesseract.image_to_string(page, lang=config.OCR_LANG)
                result = {
                    "page": i,
                    "text": text.strip(),
                    "progress": int(i / total_pages * 100)
                }
                results.append(result)

                yield f"data: {json.dumps(result, ensure_ascii=False)}\n\n"
                time.sleep(config.STREAM_DELAY)

        full_output = {
            "filename": os.path.basename(pdf_path),
            "page_count": total_pages,
            "pages": results
        }
        full_path = os.path.join(os.path.dirname(pdf_path), os.path.basename(pdf_path) + ".json")
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(full_output, f, indent=2, ensure_ascii=False)
        FULL_JSON[token] = full_path

        yield f"data: {json.dumps({'done': True}, ensure_ascii=False)}\n\n"

    return Response(generate(), mimetype="text/event-stream")

@app.route("/download/<token>")
def download_full(token):
    json_path = FULL_JSON.get(token)
    if not json_path or not os.path.exists(json_path):
        abort(404)
    return send_file(json_path, as_attachment=True,
                     download_name=os.path.basename(json_path))

if __name__ == "__main__":
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=config.DEBUG)

from flask import Flask, send_from_directory, jsonify, request
from werkzeug.utils import secure_filename
import os
import logging
from collections import defaultdict
from functools import wraps
from config import Config

app = Flask(__name__)

FILE_DIR = Config.FILE_DIR
logging.basicConfig(level=logging.INFO)
_request_log = defaultdict(list)
RATE_LIMIT = 60
RATE_WINDOW = 60
def rate_limit(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        ip = request.remote_addr
        now = time.time()
        window_start = now - RATE_WINDOW

        _request_log[ip] = [t for t in _request_log[ip] if t > window_start]

        if len(_request_log[ip]) >= RATE_LIMIT:
            retry_after = int(_request_log[ip][0] - window_start)
            return api_response(
                "error",
                f"Rate limit exceeded. Try again in {retry_after}s.",
                status_code=429
            )

        _request_log[ip].append(now)
        return f(*args, **kwargs)
    return decorated

def api_response(status, message=None, data=None, status_code=200):
    return jsonify({
        "status": status,
        "message": message,
        "data": data
    }), status_code
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-KEY")

        if not key:
            return api_response("error", "API key missing", status_code=401)

        if key != Config.API_KEY:
            return api_response("error", "Invalid API key", status_code=403)

        return f(*args, **kwargs)

    return decorated

@app.route('/api/v1/files', methods=['GET'])
@require_api_key
@rate_limit
def list_files():
    try:
        files = os.listdir(FILE_DIR)
        return api_response("success", data={"files": files})
    except Exception:
        return api_response("error", "Could not retrieve files", status_code=500)
@app.route('/api/v1/files', methods=['POST'])
@require_api_key
@rate_limit
def upload_file():
    logging.info("File upload requested")
    if 'file' not in request.files:
        return api_response("error", "No file part in the request", status_code=400)
    
    file = request.files['file']
    if file.filename == '':
        return api_response("error", "No selected file", status_code=400)
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(FILE_DIR, filename))
        return api_response("success", f"File '{filename}' uploaded successfully")
@app.route('/api/v1/files/<filename>', methods=['GET'])
@require_api_key
@rate_limit
def download_file(filename):
    logging.info(f"Download requested: {filename}")
    filename = secure_filename(filename)
    file_path = os.path.join(FILE_DIR, filename)

    if not os.path.exists(file_path):
        return api_response("error", "File not found", status_code=404)

    return send_from_directory(FILE_DIR, filename, as_attachment=True)


@app.route('/api/v1/health', methods=['GET'])
def health():
    return api_response("success", "API is running")


@app.errorhandler(404)
def not_found(e):
    return api_response("error", "Endpoint not found", status_code=404)


@app.errorhandler(500)
def internal_error(e):
    return api_response("error", "Internal server error", status_code=500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)
from flask import Flask, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
import logging
from config import Config

app = Flask(__name__)

FILE_DIR = Config.FILE_DIR
logging.basicConfig(level=logging.INFO)


def api_response(status, message=None, data=None, status_code=200):
    return jsonify({
        "status": status,
        "message": message,
        "data": data
    }), status_code


@app.route('/api/v1/files', methods=['GET'])
def list_files():
    try:
        files = os.listdir(FILE_DIR)
        return api_response("success", data={"files": files})
    except Exception:
        return api_response("error", "Could not retrieve files", status_code=500)


@app.route('/api/v1/files/<filename>', methods=['GET'])
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
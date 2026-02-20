# Flask File Server API

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-API-black)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Stable-success)

A lightweight REST-style file server API built with Flask.  
It allows secure listing and downloading of files from a configured directory.

---

## Features

- Versioned REST API (`/api/v1`)
- Secure file downloads
- File listing endpoint
- Consistent JSON responses
- Health check endpoint
- Environment-based configuration
- Structured logging
- Clean project structure

---

## Project Structure

```

flask-file-server/
│
├── app.py
├── config.py
├── requirements.txt
├── files/
├── .gitignore
├── LICENSE
└── README.md

```

---

## Requirements

- Python 3.8+
- Flask

---

## Installation

### 1. Clone the repository

```

git clone https://github.com/MrRealmWLS/flask-file-server.git
cd flask-file-server

```

### 2. Create a virtual environment (recommended)

```

python -m venv venv
source venv/bin/activate

```

On Windows:

```

venv\Scripts\activate

```

### 3. Install dependencies

```

pip install -r requirements.txt

````

---

## Configuration

Edit `config.py`:

```python
import os

class Config:
    FILE_DIR = os.getenv("FILE_DIR", "files")
    PORT = int(os.getenv("PORT", 5000))
````

You can also configure using environment variables:

Linux/macOS:

```
export FILE_DIR=files
export PORT=5000
```

Windows (PowerShell):

```
setx FILE_DIR files
setx PORT 5000
```

---

## Running the Application

```
python app.py
```

The API will be available at:

```
http://localhost:5000
```

---

## API Endpoints

### Health Check

```
GET /api/v1/health
```

Response:

```json
{
  "status": "success",
  "message": "API is running",
  "data": null
}
```

---

### List Files

```
GET /api/v1/files
```

Response:

```json
{
  "status": "success",
  "message": null,
  "data": {
    "files": ["example.pdf", "image.png"]
  }
}
```

---

### Download File

```
GET /api/v1/files/<filename>
```

Example:

```
GET /api/v1/files/example.pdf
```

Returns the requested file as a downloadable attachment.

---

## cURL Examples

List files:

```
curl http://localhost:5000/api/v1/files
```

Download file:

```
curl -O http://localhost:5000/api/v1/files/example.pdf
```

Health check:

```
curl http://localhost:5000/api/v1/health
```

---

## Security

* Filenames are sanitized using `secure_filename`
* Directory traversal is prevented
* Only files inside the configured directory can be accessed

---

## Future Improvements

* File upload endpoint
* API key authentication
* Rate limiting
* Docker support

---

## License

MIT License
import os

class Config:
    FILE_DIR = os.getenv("FILE_DIR", "files")
    PORT = int(os.getenv("PORT", 5000))
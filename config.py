# backend/config.py

import os
from dotenv import load_dotenv

load_dotenv()

# Flask
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-ganti-ini")

# Database
DB_PATH = os.path.join(os.path.dirname(__file__), "storage", "app.db")

# Email (SMTP - Gmail)
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# TCP server (upload file)
TCP_HOST = "0.0.0.0"
TCP_PORT = 9001
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "storage", "uploads")

# UDP server (streaming video)
UDP_HOST = "0.0.0.0"
UDP_PORT = 9002
VIDEO_DIR = os.path.join(os.path.dirname(__file__), "storage", "videos")

# Flask web server
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
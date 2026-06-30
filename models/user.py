# backend/models/user.py

import sqlite3
from config import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # supaya hasil query bisa diakses kayak dict
    return conn

def init_db():
    """Bikin tabel users kalau belum ada. Dipanggil sekali saat app.py start."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_verified INTEGER NOT NULL DEFAULT 0,
            verify_token TEXT
        )
    """)
    conn.commit()
    conn.close()

def create_user(email, password_hash, verify_token):
    conn = get_connection()
    conn.execute(
        "INSERT INTO users (email, password_hash, is_verified, verify_token) VALUES (?, ?, 0, ?)",
        (email, password_hash, verify_token)
    )
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return row

def get_user_by_token(token):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE verify_token = ?", (token,)).fetchone()
    conn.close()
    return row

def mark_user_verified(email):
    conn = get_connection()
    conn.execute("UPDATE users SET is_verified = 1, verify_token = NULL WHERE email = ?", (email,))
    conn.commit()
    conn.close()
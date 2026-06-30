# backend/utils/auth_utils.py

import secrets
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(plain_password):
    return generate_password_hash(plain_password)

def verify_password(plain_password, password_hash):
    return check_password_hash(password_hash, plain_password)

def generate_verify_token():
    """Generate string acak buat link verifikasi email."""
    return secrets.token_urlsafe(32)
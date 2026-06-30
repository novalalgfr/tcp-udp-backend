# backend/routes/auth_routes.py

from flask import Blueprint, request, jsonify
from models.user import create_user, get_user_by_email, get_user_by_token, mark_user_verified
from utils.auth_utils import hash_password, verify_password, generate_verify_token
from utils.email_utils import send_verification_email

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email dan password wajib diisi"}), 400

    if get_user_by_email(email):
        return jsonify({"error": "Email sudah terdaftar"}), 400

    password_hash = hash_password(password)
    token = generate_verify_token()

    create_user(email, password_hash, token)
    send_verification_email(email, token)

    return jsonify({"message": "Registrasi berhasil, silakan cek email untuk verifikasi"}), 201


@auth_bp.route("/verify", methods=["GET"])
def verify():
    token = request.args.get("token")
    user = get_user_by_token(token)

    if not user:
        return jsonify({"error": "Token tidak valid atau sudah digunakan"}), 400

    mark_user_verified(user["email"])
    return jsonify({"message": "Akun berhasil diverifikasi, silakan login"}), 200


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = get_user_by_email(email)

    if not user or not verify_password(password, user["password_hash"]):
        return jsonify({"error": "Email atau password salah"}), 401

    if not user["is_verified"]:
        return jsonify({"error": "Akun belum diverifikasi, cek email kamu"}), 403

    return jsonify({"message": "Login berhasil", "email": user["email"]}), 200
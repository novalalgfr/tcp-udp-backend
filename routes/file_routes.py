# backend/routes/file_routes.py

import os
import mimetypes
import socket as sock_module
from flask import Blueprint, request, jsonify, send_from_directory, Response, stream_with_context
from config import TCP_HOST, TCP_PORT, UPLOAD_DIR, UDP_HOST, UDP_PORT, VIDEO_DIR

file_bp = Blueprint("file", __name__, url_prefix="/api/file")

@file_bp.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "File tidak ditemukan"}), 400

    uploaded_file = request.files["file"]
    filename = uploaded_file.filename
    file_bytes = uploaded_file.read()
    filesize = len(file_bytes)

    try:
        tcp_socket = sock_module.socket(sock_module.AF_INET, sock_module.SOCK_STREAM)
        tcp_socket.connect((TCP_HOST if TCP_HOST != "0.0.0.0" else "localhost", TCP_PORT))

        tcp_socket.sendall(f"{filename}\n".encode())
        tcp_socket.sendall(f"{filesize}\n".encode())
        tcp_socket.sendall(file_bytes)

        tcp_socket.close()
    except Exception as e:
        return jsonify({"error": f"Gagal kirim ke TCP server: {e}"}), 500

    return jsonify({"message": "Upload berhasil", "filename": filename}), 200


@file_bp.route("/list", methods=["GET"])
def list_files():
    files = os.listdir(UPLOAD_DIR) if os.path.exists(UPLOAD_DIR) else []
    return jsonify({"files": files}), 200


@file_bp.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    filename = os.path.basename(filename)
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=True)


@file_bp.route("/videos", methods=["GET"])
def list_videos():
    videos = os.listdir(VIDEO_DIR) if os.path.exists(VIDEO_DIR) else []
    return jsonify({"videos": videos}), 200


@file_bp.route("/stream/<filename>", methods=["GET"])
def stream_video(filename):
    filename = os.path.basename(filename)

    def generate():
        udp_socket = sock_module.socket(sock_module.AF_INET, sock_module.SOCK_DGRAM)
        udp_socket.settimeout(30)

        server_addr = ("localhost", UDP_PORT)
        udp_socket.sendto(filename.encode(), server_addr)

        try:
            data, _ = udp_socket.recvfrom(1024)
            if data.startswith(b"ERROR"):
                return

            chunks = {}
            expected_seq = 0

            while True:
                packet, _ = udp_socket.recvfrom(4096 + 4)
                if packet == b"END":
                    for seq in sorted(chunks.keys()):
                        yield chunks[seq]
                    break

                seq = int.from_bytes(packet[:4], byteorder="big")
                chunk_data = packet[4:]

                if seq == expected_seq:
                    yield chunk_data
                    expected_seq += 1
                    while expected_seq in chunks:
                        yield chunks.pop(expected_seq)
                        expected_seq += 1
                else:
                    chunks[seq] = chunk_data

        except sock_module.timeout:
            return
        finally:
            udp_socket.close()

    mime, _ = mimetypes.guess_type(filename)
    mime = mime or "video/mp4"

    return Response(
        stream_with_context(generate()),
        mimetype=mime,
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )
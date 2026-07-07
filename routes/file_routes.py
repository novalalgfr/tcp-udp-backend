from flask import Blueprint, request, jsonify, send_from_directory, Response, stream_with_context
import os
import socket as sock_module
from config import TCP_HOST, TCP_PORT, UPLOAD_DIR, UDP_HOST, UDP_PORT, VIDEO_DIR

@file_bp.route("/stream/<filename>", methods=["GET"])
def stream_video(filename):
    filename = os.path.basename(filename)

    def generate():
        udp_socket = sock_module.socket(sock_module.AF_INET, sock_module.SOCK_DGRAM)
        udp_socket.settimeout(30)

        server_addr = ("localhost", UDP_PORT)
        udp_socket.sendto(filename.encode(), server_addr)

        try:
            # Terima header SIZE dulu
            data, _ = udp_socket.recvfrom(1024)
            if data.startswith(b"ERROR"):
                return

            # Terima chunk dan langsung yield ke browser
            chunks = {}
            expected_seq = 0

            while True:
                packet, _ = udp_socket.recvfrom(4096 + 4)
                if packet == b"END":
                    # yield sisa chunk yang belum dikirim (kalau ada yang out-of-order)
                    for seq in sorted(chunks.keys()):
                        yield chunks[seq]
                    break

                seq = int.from_bytes(packet[:4], byteorder="big")
                chunk_data = packet[4:]

                # yield chunk yang berurutan langsung, simpan yang out-of-order
                if seq == expected_seq:
                    yield chunk_data
                    expected_seq += 1
                    # cek buffer kalau ada chunk berikutnya yang sudah datang
                    while expected_seq in chunks:
                        yield chunks.pop(expected_seq)
                        expected_seq += 1
                else:
                    chunks[seq] = chunk_data

        except sock_module.timeout:
            return
        finally:
            udp_socket.close()

    return Response(
        stream_with_context(generate()),
        mimetype="video/mp4",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )
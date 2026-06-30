# backend/sockets/udp_server.py

import socket
import os
from config import UDP_HOST, UDP_PORT, VIDEO_DIR

CHUNK_SIZE = 4096

def start_udp_server():
    os.makedirs(VIDEO_DIR, exist_ok=True)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((UDP_HOST, UDP_PORT))

    print(f"UDP server listening di {UDP_HOST}:{UDP_PORT}")

    while True:
        # Tunggu request dari client: isinya nama file yang mau di-stream
        data, client_addr = server_socket.recvfrom(1024)
        filename = data.decode().strip()
        filename = os.path.basename(filename)  # cegah path traversal

        print(f"UDP request stream '{filename}' dari {client_addr}")
        send_video(server_socket, filename, client_addr)


def send_video(server_socket, filename, client_addr):
    filepath = os.path.join(VIDEO_DIR, filename)

    if not os.path.exists(filepath):
        server_socket.sendto(b"ERROR:FILE_NOT_FOUND", client_addr)
        return

    filesize = os.path.getsize(filepath)

    # Kirim header dulu: total ukuran file, supaya client tahu kapan berhenti
    server_socket.sendto(f"SIZE:{filesize}".encode(), client_addr)

    seq = 0
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            # Header kecil: nomor urut (4 byte) + isi chunk
            header = seq.to_bytes(4, byteorder="big")
            server_socket.sendto(header + chunk, client_addr)
            seq += 1

    # Tanda video sudah habis dikirim
    server_socket.sendto(b"END", client_addr)
    print(f"Selesai kirim '{filename}' ke {client_addr}, total {seq} chunk")
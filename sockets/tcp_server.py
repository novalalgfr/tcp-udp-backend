# backend/sockets/tcp_server.py

import socket
import os
from config import TCP_HOST, TCP_PORT, UPLOAD_DIR

def start_tcp_server():
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((TCP_HOST, TCP_PORT))
    server_socket.listen(5)

    print(f"TCP server listening di {TCP_HOST}:{TCP_PORT}")

    while True:
        conn, addr = server_socket.accept()
        print(f"TCP connection dari {addr}")
        handle_client(conn)


def handle_client(conn):
    try:
        # 1. Terima dulu nama file (diakhiri newline)
        filename = b""
        while not filename.endswith(b"\n"):
            chunk = conn.recv(1)
            if not chunk:
                return
            filename += chunk
        filename = filename.decode().strip()
        filename = os.path.basename(filename)  # cegah path traversal

        # 2. Terima ukuran file (diakhiri newline)
        filesize = b""
        while not filesize.endswith(b"\n"):
            chunk = conn.recv(1)
            if not chunk:
                return
            filesize = filesize + chunk
        filesize = int(filesize.decode().strip())

        # 3. Terima isi file sebanyak filesize byte
        filepath = os.path.join(UPLOAD_DIR, filename)
        received = 0
        with open(filepath, "wb") as f:
            while received < filesize:
                data = conn.recv(4096)
                if not data:
                    break
                f.write(data)
                received += len(data)

        print(f"File '{filename}' diterima ({received} bytes)")
    except Exception as e:
        print(f"Error handling TCP client: {e}")
    finally:
        conn.close()
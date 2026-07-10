import socket
import os
import time
import threading
from config import UDP_HOST, UDP_PORT, VIDEO_DIR

CHUNK_SIZE = 4096

def start_udp_server():
    os.makedirs(VIDEO_DIR, exist_ok=True)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((UDP_HOST, UDP_PORT))

    print(f"UDP server listening di {UDP_HOST}:{UDP_PORT}")

    while True:
        try:
            data, client_addr = server_socket.recvfrom(1024)
            filename = data.decode().strip()
            filename = os.path.basename(filename)

            print(f"UDP request stream '{filename}' dari {client_addr}")
            
            threading.Thread(
                target=send_video, 
                args=(server_socket, filename, client_addr), 
                daemon=True
            ).start()
            
        except ConnectionResetError:
            continue
        except Exception as e:
            print(f"UDP Error di main loop: {e}")


def send_video(server_socket, filename, client_addr):
    filepath = os.path.join(VIDEO_DIR, filename)

    if not os.path.exists(filepath):
        try:
            server_socket.sendto(b"ERROR:FILE_NOT_FOUND", client_addr)
        except Exception:
            pass
        return

    filesize = os.path.getsize(filepath)

    try:
        server_socket.sendto(f"SIZE:{filesize}".encode(), client_addr)

        seq = 0
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                header = seq.to_bytes(4, byteorder="big")
                server_socket.sendto(header + chunk, client_addr)
                seq += 1
                
                time.sleep(0.002)

        server_socket.sendto(b"END", client_addr)
        print(f"Selesai kirim '{filename}' ke {client_addr}, total {seq} chunk")
        
    except ConnectionResetError:
        # Menangkap error saat user me-refresh halaman (socket Flask tertutup)
        print(f"Koneksi terputus ke {client_addr} (Browser di-refresh). Stream dihentikan.")
    except Exception as e:
        print(f"Error saat kirim video ke {client_addr}: {e}")
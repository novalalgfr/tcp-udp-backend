# backend/app.py

import threading
from flask import Flask
from flask_cors import CORS
from config import FLASK_HOST, FLASK_PORT, SECRET_KEY
from models.user import init_db
from routes.auth_routes import auth_bp
from routes.file_routes import file_bp
from sockets.tcp_server import start_tcp_server
from sockets.udp_server import start_udp_server

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(auth_bp)
app.register_blueprint(file_bp)

if __name__ == "__main__":
    init_db()

    threading.Thread(target=start_tcp_server, daemon=True).start()
    threading.Thread(target=start_udp_server, daemon=True).start()

    print(f"Flask jalan di http://localhost:{FLASK_PORT}")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=False)
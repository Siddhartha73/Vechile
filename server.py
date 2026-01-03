from flask import Flask, request, jsonify
import socket
import threading
import os

PORT = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=PORT)

app = Flask(__name__)

vehicle_socket = None

def tcp_listener():
    global vehicle_socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 9000))
    s.listen(1)
    print("Waiting for vehicle on TCP 9000...")
    vehicle_socket, addr = s.accept()
    print("Vehicle connected from:", addr)

threading.Thread(target=tcp_listener, daemon=True).start()

@app.route("/send", methods=["POST"])
def send_command():
    global vehicle_socket
    data = request.json
    cmd = data.get("command")

    if not cmd:
        return jsonify({"error": "No command"}), 400

    if vehicle_socket is None:
        return jsonify({"error": "Vehicle not connected"}), 503

    try:
        vehicle_socket.sendall((cmd + "\n").encode())
        return jsonify({"status": "Command sent"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Vehicle Control Server Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

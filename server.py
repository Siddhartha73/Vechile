from flask import Flask, request, jsonify
import os

app = Flask(__name__)

latest_command = None
latest_status = {
    "speed": 0,
    "brake": 0,
    "state": "RUNNING"
}

@app.route("/")
def home():
    return "Vehicle Control Server Running"

# App → Server
@app.route("/send", methods=["POST"])
def send_command():
    global latest_command
    data = request.json
    latest_command = data.get("command")
    print("From App:", latest_command)
    return jsonify({"status": "stored"}), 200

# ESP32 → Poll
@app.route("/poll", methods=["GET"])
def poll_command():
    global latest_command
    if latest_command:
        cmd = latest_command
        latest_command = None
        print("Sent to vehicle:", cmd)
        return cmd, 200
    return "NO_CMD", 204

# ESP32 → Status
@app.route("/status", methods=["POST"])
def receive_status():
    global latest_status
    latest_status = request.json
    return jsonify({"ok": True})

# App → Status
@app.route("/status", methods=["GET"])
def send_status():
    return jsonify(latest_status)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

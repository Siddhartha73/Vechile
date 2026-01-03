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

# ---------- APP → SERVER ----------
@app.route("/send", methods=["POST"])
def send_command():
    global latest_command
    data = request.json
    latest_command = data.get("command")
    print("From App:", latest_command)
    return jsonify({"status": "stored"}), 200

# ---------- VEHICLE ← SERVER ----------
@app.route("/poll", methods=["GET"])
def poll_command():
    global latest_command
    if latest_command:
        cmd = latest_command
        latest_command = None
        print("Sent to vehicle:", cmd)
        return cmd, 200
    return "NO_CMD", 204

# ---------- VEHICLE → SERVER ----------
@app.route("/status", methods=["POST"])
def receive_status():
    global latest_status
    latest_status = request.json
    print("Vehicle Status:", latest_status)
    return "OK", 200

# ---------- APP ← SERVER ----------
@app.route("/status", methods=["GET"])
def get_status():
    return jsonify(latest_status), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

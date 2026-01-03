from flask import Flask, request, jsonify
import os

app = Flask(__name__)


est_command = None

@app.route("/")
def home():
    return "Vehicle Control Server Running"

# ===== Mobile App sends command =====
@app.route("/send", methods=["POST"])
def send_command():
    global latest_command
    data = request.json
    latest_command = data.get("command")
    print("From App:", latest_command)
    return jsonify({"status": "stored"}), 200

# ===== Vehicle polls command =====
@app.route("/poll", methods=["GET"])
def poll_command():
    global latest_command
    if latest_command:
        cmd = latest_command
        latest_command = None   # consume once
        print("Sent to vehicle:", cmd)
        return cmd, 200
    return "NO_CMD", 204

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

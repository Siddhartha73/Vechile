from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage (Railway-friendly)
pending_commands = {}
vehicle_status = {}

@app.route("/")
def home():
    return "Vehicle Control Server Running"

# ================= APP → SERVER =================
@app.route("/send", methods=["POST"])
def send_command():
    data = request.get_json(force=True)
    command = data.get("command")

    if not command or "DEV=" not in command:
        return jsonify({"error": "Invalid command"}), 400

    dev = command.split("DEV=")[1].split("|")[0]
    pending_commands[dev] = command

    print("From App:", command)
    return jsonify({"status": "QUEUED"}), 200

# ================= VEHICLE → SERVER =================
@app.route("/poll", methods=["GET"])
def poll_command():
    dev = request.args.get("dev")

    if not dev:
        return "NO_DEV", 400

    if dev in pending_commands:
        cmd = pending_commands.pop(dev)
        print("Sent to vehicle:", cmd)
        return cmd, 200

    return "NO_CMD", 204

# ================= VEHICLE → SERVER (STATUS) =================
@app.route("/status", methods=["POST"])
def receive_status():
    dev = request.args.get("dev", "UNKNOWN")
    data = request.data.decode()

    vehicle_status[dev] = data
    print("From vehicle:", dev, data)

    return "OK", 200

# ================= APP → SERVER (READ STATUS) =================
@app.route("/status", methods=["GET"])
def get_status():
    return jsonify(vehicle_status), 200


# ================= MAIN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

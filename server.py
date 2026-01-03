from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage
vehicle_commands = {}
vehicle_status = {}

@app.route("/")
def home():
    return "Vehicle Control Server Running"

# -------- APP → SERVER --------
@app.route("/send", methods=["POST"])
def send_command():
    data = request.json
    cmd = data.get("command")

    if not cmd or "DEV=" not in cmd:
        return jsonify({"error": "Invalid command"}), 400

    dev = cmd.split("DEV=")[1].split("|")[0]
    vehicle_commands[dev] = cmd

    print("From App:", cmd)
    return jsonify({"status": "Queued"}), 200

# -------- VEHICLE → SERVER --------
@app.route("/poll", methods=["GET"])
def poll_command():
    dev = request.args.get("dev")

    if not dev:
        return "NO_DEV", 400

    if dev in vehicle_commands:
        cmd = vehicle_commands.pop(dev)
        print("Sent to vehicle:", cmd)
        return cmd, 200

    return "NO_CMD", 204

# -------- VEHICLE → SERVER (STATUS) --------
@app.route("/status", methods=["POST"])
def receive_status():
    data = request.data.decode()
    dev = request.args.get("dev", "UNKNOWN")

    vehicle_status[dev] = data
    print("From vehicle:", dev, data)

    return "OK", 200

# -------- APP → SERVER (READ STATUS) --------
@app.route("/status", methods=["GET"])
def get_status():
    return jsonify(vehicle_status), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

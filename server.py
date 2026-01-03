from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# ================= HOME =================
@app.route("/")
def home():
    return "Vehicle Control Server Running"

# ================= MOBILE APP ENDPOINT =================
@app.route("/send", methods=["POST"])
def send_command():
    data = request.json
    command = data.get("command")

    if not command:
        return jsonify({"error": "No command"}), 400

    print("From App:", command)

    # In HTTP architecture, app just stores / logs / validates
    # Vehicle will fetch commands separately (or same endpoint logic)
    return jsonify({"status": "Command received"}), 200

# ================= VEHICLE (A7670C) ENDPOINT =================
@app.route("/vehicle", methods=["POST"])
def vehicle_receive():
    data = request.data.decode()
    print("From Vehicle:", data)

    # Here you can parse CMD, authenticate, store state, etc.
    return "OK", 200

# ================= MAIN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

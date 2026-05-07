from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


latest_data = {
    "emotion": "",
    "priority": "",
    "incident": "",
    "location": "",
    "people": "",
    "transcript": "",
    "response": ""
}


@app.route("/")
def dashboard():

    return render_template("dashboard.html")



@app.route("/update", methods=["POST"])
def update():

    global latest_data

    data = request.json

    latest_data = {
        "emotion": data.get("emotion", ""),
        "priority": data.get("priority", ""),
        "incident": data.get("incident", ""),
        "location": data.get("location", ""),
        "people": data.get("people", ""),
        "transcript": data.get("transcript", ""),
        "response": data.get("response", "")
    }

    print("\n📥 NEW DATA RECEIVED")
    print(latest_data)

    return jsonify({
        "status": "success",
        "message": "Dashboard updated"
    })



@app.route("/data", methods=["GET"])
def get_data():

    global latest_data

    data_to_send = latest_data.copy()

    latest_data = {
        "emotion": "",
        "priority": "",
        "incident": "",
        "location": "",
        "people": "",
        "transcript": "",
        "response": ""
    }

    return jsonify(data_to_send)

if __name__ == "__main__":

    print("🚀 Starting Flask Server...")
    app.run(host="127.0.0.1", port=5000, debug=True)
import os
from flask import Flask, jsonify
import requests

app = Flask(__name__)

GOOGLE_SHEET_API = "https://script.google.com/macros/s/AKfycbwiorOI7CeNUhpqC5UBac86oF9nVME8umWd8xA0Pka2HBVin1r5H9bxXd-qH6eF-pht/exec"

@app.route("/cot")
def get_cot():
    try:
        response = requests.get(GOOGLE_SHEET_API)
        response.raise_for_status()
        data = response.json()
        return jsonify(data[-100:])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

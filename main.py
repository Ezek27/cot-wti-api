import os
from flask import Flask, jsonify, Response
import requests

app = Flask(__name__)

# Lien vers ton API Google Sheets (Apps Script)
GOOGLE_SHEET_API = "https://script.google.com/macros/s/AKfycbwiorOI7CeNUhpqC5UBac86oF9nVME8umWd8xA0Pka2HBVin1r5H9bxXd-qH6eF-pht/exec"

# Route JSON brute
@app.route("/cot")
def get_cot():
    try:
        response = requests.get(GOOGLE_SHEET_API)
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route CSV simplifiée pour Pine Script / Google Sheets
@app.route("/cot/csv")
def get_cot_csv():
    try:
        response = requests.get(GOOGLE_SHEET_API)
        response.raise_for_status()
        data = response.json()

        # Conversion en CSV avec noms de colonnes simplifiés
        csv_data = "Date,NonComm,Comm,Small\n"
        for row in data:
            csv_data += f"{row['Date (au format AAAAMMJJ)']},{row['Net Position des Spéculateurs non-commerciaux']},{row['Net Position des Commercials']},{row['Net Position des Small Traders']}\n"

        return Response(csv_data, mimetype="text/csv")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Lancement serveur pour Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


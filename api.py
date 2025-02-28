from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Clés Strava (à configurer dans les variables d'environnement sur Vercel)
STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")
STRAVA_UPLOAD_URL = "https://www.strava.com/api/v3/uploads"

# Fonction pour rafraîchir le token d'accès
def refresh_strava_token():
    response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": STRAVA_CLIENT_ID,
            "client_secret": STRAVA_CLIENT_SECRET,
            "refresh_token": STRAVA_REFRESH_TOKEN,
            "grant_type": "refresh_token",
        },
    )
    token_data = response.json()
    return token_data.get("access_token")

@app.route("/upload", methods=["POST"])
def upload_gpx():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    access_token = refresh_strava_token()
    
    files = {"file": (file.filename, file.stream, "application/gpx+xml")}
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"data_type": "gpx"}
    
    response = requests.post(STRAVA_UPLOAD_URL, headers=headers, files=files, data=data)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Flask fonctionne sur Vercel ! 🚀"

    app.run(debug=True)
    

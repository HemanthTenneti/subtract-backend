from flask import Flask, request, jsonify
from processor import process_url
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("FLASK_API_KEY")

@app.route('/api/process', methods=['POST'])
def transcribe():
    print(request.headers.get("x-api-key"))
    if request.headers.get("x-api-key") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    url = request.get_json().get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    print("Processing:", url)
    summary, transcription = process_url(url)
    return jsonify({"summary": summary, "transcription": transcription})

if __name__ == '__main__':
    app.run(debug=True)

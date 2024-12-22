from flask import Flask, request, jsonify
import requests  # For calling the Gemini API

app = Flask(__name__)

# Replace with your Gemini API key
GEMINI_API_KEY = "your-gemini-api-key"
GEMINI_API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=GEMINI_API_KEY"  # Example base URL (change based on Gemini's API docs)

# curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=GEMINI_API_KEY" \
# -H 'Content-Type: application/json' \
# -X POST \
# -d '{
#   "contents": [{
#     "parts":[{"text": "please Say hello using accent southeast sulawesi'"}]
#     }]
#    }'

# Endpoint to get Gemini data
@app.route('/api/test-gemini', methods=['GET'])
def get_gemini_data():
    try:
        # Example Gemini API call (customize based on your use case)
        response = requests.get(
            f"{GEMINI_API_BASE_URL}/example-endpoint",
            headers={"Authorization": f"Bearer {GEMINI_API_KEY}"}
        )

        # Return Gemini API response to Flutter
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": response.json()}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint to send data to Gemini API
@app.route('/api/gemini/post', methods=['POST'])
def post_gemini_data():
    try:
        # Get data from Flutter request
        data = request.json

        # Example POST request to Gemini API
        response = requests.post(
            f"{GEMINI_API_BASE_URL}/example-endpoint",
            headers={
                "Authorization": f"Bearer {GEMINI_API_KEY}",
                "Content-Type": "application/json",
            },
            json=data
        )

        # Return response to Flutter
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": response.json()}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

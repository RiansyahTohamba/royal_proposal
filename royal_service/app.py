from flask import Flask, request, jsonify

app = Flask(__name__)

# Stub for Gemini Chat API

@app.route('/gemini-chat-stub', methods=['POST'])
def gemini_chat_stub():
    # Get input from the user (mock)
    user_message = request.json.get("message", "")

    # Generate a sample response
    response = {
        "id": "mock123",
        "message": f"Echoing your input: '{user_message}'. This is a stubbed response.",
        "context": "mock_chat",
        "timestamp": "2024-12-20T12:00:00Z"
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)

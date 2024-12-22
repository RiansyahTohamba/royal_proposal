from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

app = Flask(__name__)

# Configure the JWT secret key
app.config["JWT_SECRET_KEY"] = "your-secret-key"  # Replace with your secret key
jwt = JWTManager(app)

# Dummy user data (replace with database logic)
USERS = {"royal": "royal_password123", "user2": "mypassword"}


# Login endpoint to generate JWT token
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    # Check if user exists and password matches
    if USERS.get(username) != password:
        return jsonify({"msg": "Invalid username or password"}), 401

    # Create JWT token
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


# Protected endpoint
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Get the identity of the logged-in user
    current_user = get_jwt_identity()
    return jsonify({"msg": f"Hello, {current_user}! This is a protected route."})


if __name__ == '__main__':
    app.run(debug=True)

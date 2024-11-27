from flask import Flask, request, jsonify, make_response, session
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask App
app = Flask(__name__)

# ================================
# Global Security Configurations
# ================================
# Set a strong secret key for session management
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')

# Disable session refresh on every request
app.config['SESSION_REFRESH_EACH_REQUEST'] = False

# ================================
# After-Request Hook to Set Cache-Control Headers
# ================================
@app.after_request
def add_cache_control_headers(response):
    """
    Add Cache-Control headers to all responses to prevent sensitive data from being cached.
    """
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
    return response

# ================================
# Home Route
# ================================
@app.route('/')
def home():
    """
    Home Route
    Returns a welcome message for the app.
    """
    return "Welcome to My Branded Flask App! 🚀"

# ================================
# User Authentication
# ================================
@app.route('/login', methods=['POST'])
def login():
    """
    User Authentication
    Accepts JSON data with 'username' and 'password' for a simple authentication check.
    """
    data = request.json

    # Validate input
    if not isinstance(data, dict) or 'username' not in data or 'password' not in data:
        return jsonify({"message": "Invalid input format ❌"}), 400

    username = data.get('username')
    password = data.get('password')

    # Get username and password from environment variables
    correct_username = os.getenv('FLASK_USERNAME')
    correct_password = os.getenv('FLASK_PASSWORD')

    # Check if the credentials match
    if username == correct_username and password == correct_password:
        response = jsonify({"message": "Login successful 🎉"})
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
        return response, 200

    response = jsonify({"message": "Invalid credentials ❌"})
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
    return response, 401

# ================================
# Data Submission Endpoint
# ================================
@app.route('/submit', methods=['POST'])
def submit():
    """
    Data Submission
    Accepts JSON data and returns the submitted data in the response.
    """
    data = request.json

    # Validate input
    if not isinstance(data, dict):
        return jsonify({"message": "Invalid data format ❌"}), 400

    return jsonify({"message": "Data received ✅", "data": data}), 200

# ================================
# CRUD API for Item Management
# ================================
# In-memory storage for items
items = []

@app.route('/items', methods=['GET', 'POST'])
def manage_items():
    """
    Manage Items (Create and Read)
    POST: Add a new item to the list.
    GET: Retrieve the list of items.
    """
    if request.method == 'POST':
        item = request.json.get('item')

        # Validate input
        if not item:
            return jsonify({"message": "Invalid item data ❌"}), 400

        items.append(item)
        return jsonify({"message": "Item added successfully 🛒", "items": items}), 201

    return jsonify({"items": items}), 200

@app.route('/items/<int:item_id>', methods=['PUT', 'DELETE'])
def update_delete_item(item_id):
    """
    Update or Delete an Item
    PUT: Update an existing item by ID.
    DELETE: Remove an item by ID.
    """
    if item_id >= len(items) or item_id < 0:
        return jsonify({"message": "Item not found ❌"}), 404

    if request.method == 'PUT':
        new_item = request.json.get('item')

        # Validate input
        if not new_item:
            return jsonify({"message": "Invalid item data ❌"}), 400

        items[item_id] = new_item
        return jsonify({"message": "Item updated successfully 📝", "items": items}), 200

    if request.method == 'DELETE':
        items.pop(item_id)
        return jsonify({"message": "Item deleted successfully 🗑️", "items": items}), 200

# ================================
# Secure Session Management Example
# ================================
@app.route('/set-session')
def set_session():
    """
    Example to demonstrate secure session usage.
    """
    session['user'] = 'example_user'
    session.permanent = False  # Use temporary sessions
    return jsonify({"message": "Session set successfully ✅"})

# ================================
# Run the Flask App
# ================================
if __name__ == "__main__":
    # Get the debug mode from environment variables, default to False for production
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'

    # Run the app, binding to localhost and controlling debug mode via environment variables
    app.run(debug=debug_mode, host="127.0.0.1", port=5000)

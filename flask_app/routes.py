# flask_app/routes.py
from flask import Blueprint, request, jsonify, current_app

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Welcome to My Branded Flask App! 🚀"

@main.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username == current_app.config['FLASK_USERNAME'] and password == current_app.config['FLASK_PASSWORD']:
        return jsonify({"message": "Login successful 🎉"}), 200
    return jsonify({"message": "Invalid credentials ❌"}), 401

@main.route('/submit', methods=['POST'])
def submit():
    data = request.json
    return jsonify({"message": "Data received ✅", "data": data}), 200

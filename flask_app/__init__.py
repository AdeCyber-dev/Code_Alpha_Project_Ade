 # flask_app/__init__.py
from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuring your app from environment variables
    app.config['FLASK_USERNAME'] = os.getenv('FLASK_USERNAME')
    app.config['FLASK_PASSWORD'] = os.getenv('FLASK_PASSWORD')
    app.config['FLASK_DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1']

    # Register Blueprints for modular routes
    from .routes import main
    app.register_blueprint(main)

    return app


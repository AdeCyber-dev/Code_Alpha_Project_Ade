# config.py
import os

class Config:
    FLASK_USERNAME = os.getenv('FLASK_USERNAME')
    FLASK_PASSWORD = os.getenv('FLASK_PASSWORD')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1']
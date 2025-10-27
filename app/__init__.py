# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize extensions outside of the function
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Initialize extensions with the app
    db.init_app(app)
    
    # Configure CORS
    CORS(app, resources={r"/api/*": {"origins": os.getenv('FRONTEND_URL')}})

    # 1. Register Blueprints (API routes)
    from app.api.match_routes import match_bp
    app.register_blueprint(match_bp, url_prefix='/api')
    
    # Global Error Handlers (e.g., 404, 400, 500)
    # ... (You can define your error handlers here or in a separate file)

    return app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # Register routes
    from app.routes import admin_bp, vote_bp, results_bp
    app.register_blueprint(admin_bp)
    app.register_blueprint(vote_bp)
    app.register_blueprint(results_bp)

    return app
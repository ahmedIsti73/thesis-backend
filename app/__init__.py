from flask import Flask
from flask_cors import CORS
from app.extensions import db  # Import 1
from app.middleware import setup_metrics

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configure the SQLite Database (The file will be created in 'instance' folder)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thesis.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize DB with App
    db.init_app(app) # Init 2

    # Activate Metrics
    setup_metrics(app)  # Turn on the stopwatch

    # Register Blueprints
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Create Database Tables automatically if they don't exist
    with app.app_context():
        from app.models import User  # Import models to register them
        db.create_all()

    return app
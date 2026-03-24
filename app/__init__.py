"""
Flask application factory.

This pattern lets us create multiple app instances (useful for testing)
and keeps configuration separate from app creation.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create the database instance outside the factory so models can import it
db = SQLAlchemy()


def create_app(config_class=None):
    """
    Create and configure the Flask application.

    Args:
        config_class: Configuration class to use. Defaults to config.Config.
    """
    app = Flask(__name__)

    # Load configuration
    if config_class is None:
        from config import Config
        config_class = Config
    app.config.from_object(config_class)

    # Initialize database with this app
    db.init_app(app)

    # Register route blueprints
    from app.routes.entries import entries_bp
    from app.routes.reports import reports_bp
    from app.routes.categories import categories_bp
    app.register_blueprint(entries_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(categories_bp)

    # Create database tables if they don't exist yet
    with app.app_context():
        from app import models  # noqa: F401 — import so SQLAlchemy sees the models
        db.create_all()

    return app

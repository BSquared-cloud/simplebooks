"""
Application configuration.
Reads settings from environment variables (loaded from .env file).
"""
import os
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()


class Config:
    """Base configuration — all settings read from environment variables."""

    # SECRET_KEY is used by Flask to sign session cookies and protect forms
    # against CSRF attacks. Must be a random string in production.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")

    # Database connection string. Defaults to a SQLite file in the project root.
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///simplebooks.db")

    # Disable Flask-SQLAlchemy's event notification system (saves memory)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

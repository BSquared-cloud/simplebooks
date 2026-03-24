"""
SimpleBooks entry point.
Run this file to start the development server.

Usage:
    python run.py
"""
from app import create_app
from app.seed import seed_categories

app = create_app()

# Seed default categories on first run
with app.app_context():
    seed_categories()

if __name__ == "__main__":
    # debug=True enables auto-reload when you change code and shows
    # detailed error pages (never use debug=True in production)
    app.run(debug=True, port=5000)

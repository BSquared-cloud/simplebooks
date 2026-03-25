"""
Seed data: universal default categories for self-employed workers and side-giggers.

Covers the most common income and expense categories across rideshare,
freelance, and property — kept intentionally small so users build out
what they actually need rather than deleting what they don't.
"""
from app import db
from app.models import Category

DEFAULT_CATEGORIES = [
    # Income
    ("Rental Income",           "income"),
    ("Client & Service Income", "income"),
    # Expenses
    ("Gas & Fuel",              "expense"),
    ("Mileage",                 "expense"),
    ("Phone & Internet",        "expense"),
    ("Home Office",             "expense"),
    ("Professional Services",   "expense"),
    ("Repairs & Maintenance",   "expense"),
    ("Insurance",               "expense"),
]


def seed_categories():
    """Insert default categories if none exist yet."""
    # Only seed on a fresh database — don't duplicate on re-runs
    if Category.query.first() is not None:
        return

    for cat_name, cat_type in DEFAULT_CATEGORIES:
        db.session.add(Category(
            name=cat_name,
            type=cat_type,
            group="default",
            is_default=True,
        ))

    db.session.commit()

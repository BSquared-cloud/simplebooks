"""
Seed data: pre-configured category templates for different gig types.

Run once on first launch to populate default categories.
"""
from app import db
from app.models import Category

# Each template group has a list of (name, type) tuples
TEMPLATES = {
    "rideshare": [
        ("Ride/Delivery Income", "income"),
        ("Tips", "income"),
        ("Bonuses & Incentives", "income"),
        ("Fuel", "expense"),
        ("Mileage", "expense"),
        ("Vehicle Maintenance", "expense"),
        ("Vehicle Insurance", "expense"),
        ("Platform Fees", "expense"),
        ("Tolls & Parking", "expense"),
        ("Phone & Data Plan", "expense"),
    ],
    "freelance": [
        ("Client Income", "income"),
        ("Project Bonuses", "income"),
        ("Software & Tools", "expense"),
        ("Office Supplies", "expense"),
        ("Home Office", "expense"),
        ("Professional Services", "expense"),
        ("Marketing & Advertising", "expense"),
        ("Training & Education", "expense"),
    ],
    "property": [
        ("Rent Income", "income"),
        ("Laundry/Vending Income", "income"),
        ("Repairs & Maintenance", "expense"),
        ("Property Insurance", "expense"),
        ("Property Tax", "expense"),
        ("Utilities", "expense"),
        ("Management Fees", "expense"),
        ("Mortgage Interest", "expense"),
        ("HOA Fees", "expense"),
    ],
}


def seed_categories():
    """Insert default categories if none exist yet."""
    # Only seed if the database is empty — don't duplicate on re-runs
    if Category.query.first() is not None:
        return

    for group_name, categories in TEMPLATES.items():
        for cat_name, cat_type in categories:
            category = Category(
                name=cat_name,
                type=cat_type,
                group=group_name,
                is_default=True,
            )
            db.session.add(category)

    db.session.commit()

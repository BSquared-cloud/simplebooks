"""
Database models for SimpleBooks.

All monetary values are stored as integers (cents) to avoid
floating-point rounding errors. For example, $42.50 is stored as 4250.
"""
from datetime import date, datetime
from app import db


class Category(db.Model):
    """
    A category for tagging ledger entries (e.g., "Fuel", "Rent Income").

    Categories have a type (income or expense) and belong to a template group
    so we can ship pre-configured sets for different gig types.
    """
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(7), nullable=False)  # "income" or "expense"
    group = db.Column(db.String(50), nullable=False, default="custom")  # template group name
    is_default = db.Column(db.Boolean, default=False)  # shipped with app?

    # Relationship: one category has many entries
    entries = db.relationship("Entry", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name} ({self.type})>"


class Entry(db.Model):
    """
    A single ledger entry — one credit or debit transaction.

    amount_cents stores the value in cents (integer) to avoid float issues.
    entry_type is "credit" (money in) or "debit" (money out).
    """
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    description = db.Column(db.String(300), nullable=False)
    amount_cents = db.Column(db.Integer, nullable=False)  # stored in cents
    entry_type = db.Column(db.String(6), nullable=False)  # "credit" or "debit"
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def amount_dollars(self):
        """Return the amount as a float for display (e.g., 4250 -> 42.50)."""
        return self.amount_cents / 100

    @amount_dollars.setter
    def amount_dollars(self, value):
        """Set amount from a dollar value (e.g., 42.50 -> 4250)."""
        self.amount_cents = round(value * 100)

    def __repr__(self):
        return f"<Entry {self.date} {self.entry_type} ${self.amount_dollars:.2f}>"

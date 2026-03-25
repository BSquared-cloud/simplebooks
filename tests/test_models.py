"""
Tests for database models — primarily the cents/dollars conversion logic.
"""
from app.models import Entry, Category
from datetime import date


def test_amount_dollars_getter(app):
    """amount_dollars should return cents / 100 as a float."""
    with app.app_context():
        entry = Entry(amount_cents=4250)
        assert entry.amount_dollars == 42.50


def test_amount_dollars_setter(app):
    """Setting amount_dollars should store the value in cents."""
    with app.app_context():
        entry = Entry()
        entry.amount_dollars = 42.50
        assert entry.amount_cents == 4250


def test_amount_dollars_rounding(app):
    """Cent conversion should round correctly, not introduce float drift."""
    with app.app_context():
        entry = Entry()
        entry.amount_dollars = 9.99
        assert entry.amount_cents == 999


def test_entry_repr(app):
    """Entry repr should include date, type, and amount."""
    with app.app_context():
        entry = Entry(
            date=date(2026, 1, 15),
            entry_type="credit",
            amount_cents=10000,
        )
        assert "2026-01-15" in repr(entry)
        assert "credit" in repr(entry)
        assert "100.00" in repr(entry)


def test_category_repr(app):
    """Category repr should include name and type."""
    with app.app_context():
        cat = Category(name="Fuel", type="expense")
        assert "Fuel" in repr(cat)
        assert "expense" in repr(cat)

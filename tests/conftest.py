"""
Shared pytest fixtures for SimpleBooks tests.

Uses an in-memory SQLite database so tests are fully isolated
from the real development database.
"""
import pytest
from app import create_app, db as _db
from app.models import Category, Entry
from datetime import date


class TestConfig:
    """Minimal config for tests — in-memory DB, testing mode on."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "test-secret"
    WTF_CSRF_ENABLED = False


@pytest.fixture()
def app():
    """Create a fresh app instance with a clean in-memory database per test."""
    app = create_app(TestConfig)
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture()
def sample_category(app):
    """A single income category for use in tests."""
    with app.app_context():
        cat = Category(name="Test Income", type="income", group="test")
        _db.session.add(cat)
        _db.session.commit()
        return cat.id  # return id so tests can fetch fresh from session


@pytest.fixture()
def sample_expense_category(app):
    """A single expense category for use in tests."""
    with app.app_context():
        cat = Category(name="Test Expense", type="expense", group="test")
        _db.session.add(cat)
        _db.session.commit()
        return cat.id


@pytest.fixture()
def sample_entry(app, sample_category):
    """A single ledger entry linked to sample_category."""
    with app.app_context():
        entry = Entry(
            date=date(2026, 3, 1),
            description="Test payment",
            amount_cents=5000,  # $50.00
            entry_type="credit",
            category_id=sample_category,
        )
        _db.session.add(entry)
        _db.session.commit()
        return entry.id

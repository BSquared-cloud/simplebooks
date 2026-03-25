"""
Tests for category management routes.
"""
from app import db
from app.models import Category, Entry
from datetime import date


def test_categories_page_loads(client):
    """Categories page renders."""
    response = client.get("/categories/")
    assert response.status_code == 200
    assert b"Categories" in response.data


def test_add_category_page_loads(client):
    """Add category form renders."""
    response = client.get("/categories/add")
    assert response.status_code == 200


def test_add_category_success(client, app):
    """Valid POST creates a new category."""
    client.post("/categories/add", data={
        "name": "My Custom Category",
        "type": "income",
    }, follow_redirects=True)
    with app.app_context():
        cat = Category.query.filter_by(name="My Custom Category").first()
        assert cat is not None
        assert cat.type == "income"


def test_add_category_missing_name(client):
    """POST with no name is rejected."""
    response = client.post("/categories/add", data={
        "name": "",
        "type": "income",
    })
    assert response.status_code in (400, 200)  # re-renders form with error
    assert b"required" in response.data.lower() or response.status_code == 400


def test_edit_category_success(client, sample_category, app):
    """Editing a category updates its name."""
    client.post(f"/categories/{sample_category}/edit", data={
        "name": "Renamed Category",
        "type": "income",
    }, follow_redirects=True)
    with app.app_context():
        cat = Category.query.get(sample_category)
        assert cat.name == "Renamed Category"


def test_delete_category_success(client, sample_category, app):
    """Deleting a category with no entries removes it."""
    client.post(f"/categories/{sample_category}/delete", follow_redirects=True)
    with app.app_context():
        assert Category.query.get(sample_category) is None


def test_delete_category_with_entries_blocked(client, sample_entry, sample_category, app):
    """Deleting a category that has entries should be blocked."""
    response = client.post(f"/categories/{sample_category}/delete", follow_redirects=True)
    # Should show an error and the category should still exist
    with app.app_context():
        assert Category.query.get(sample_category) is not None
    assert b"can" in response.data.lower()  # flash says "Can't delete..."


def test_categories_shows_income_and_expense(client, app):
    """Categories page separates income and expense categories."""
    with app.app_context():
        db.session.add_all([
            Category(name="My Income", type="income", group="test"),
            Category(name="My Expense", type="expense", group="test"),
        ])
        db.session.commit()
    response = client.get("/categories/")
    assert b"My Income" in response.data
    assert b"My Expense" in response.data

"""
Tests for ledger entry CRUD routes.
"""
from app import db
from app.models import Entry


def test_index_empty(client):
    """Ledger page loads with no entries."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"No entries yet" in response.data


def test_index_shows_entry(client, sample_entry, app):
    """Ledger page shows an existing entry."""
    with app.app_context():
        entry = Entry.query.get(sample_entry)
        response = client.get("/")
        assert response.status_code == 200
        assert entry.description.encode() in response.data


def test_add_entry_page_loads(client):
    """Add entry form renders."""
    response = client.get("/entries/add")
    assert response.status_code == 200
    assert b"Add Entry" in response.data


def test_add_entry_success(client, sample_category):
    """Valid POST creates an entry and redirects to ledger."""
    response = client.post("/entries/add", data={
        "date": "2026-03-15",
        "description": "Uber earnings",
        "amount": "120.50",
        "entry_type": "credit",
        "category_id": sample_category,
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Uber earnings" in response.data


def test_add_entry_missing_description(client, sample_category):
    """POST with no description returns 400 and an error message."""
    response = client.post("/entries/add", data={
        "date": "2026-03-15",
        "description": "",
        "amount": "50.00",
        "entry_type": "credit",
        "category_id": sample_category,
    })
    assert response.status_code == 400
    assert b"Description is required" in response.data


def test_add_entry_invalid_amount(client, sample_category):
    """POST with a non-numeric amount returns 400."""
    response = client.post("/entries/add", data={
        "date": "2026-03-15",
        "description": "Test",
        "amount": "abc",
        "entry_type": "credit",
        "category_id": sample_category,
    })
    assert response.status_code == 400
    assert b"valid amount" in response.data


def test_add_entry_zero_amount(client, sample_category):
    """POST with zero amount is rejected."""
    response = client.post("/entries/add", data={
        "date": "2026-03-15",
        "description": "Test",
        "amount": "0",
        "entry_type": "credit",
        "category_id": sample_category,
    })
    assert response.status_code == 400
    assert b"greater than zero" in response.data


def test_add_entry_invalid_date(client, sample_category):
    """POST with a malformed date returns 400."""
    response = client.post("/entries/add", data={
        "date": "not-a-date",
        "description": "Test",
        "amount": "50.00",
        "entry_type": "credit",
        "category_id": sample_category,
    })
    assert response.status_code == 400
    assert b"valid date" in response.data


def test_edit_entry_page_loads(client, sample_entry):
    """Edit form renders with existing entry data."""
    response = client.get(f"/entries/{sample_entry}/edit")
    assert response.status_code == 200
    assert b"Test payment" in response.data


def test_edit_entry_success(client, sample_entry, sample_category, app):
    """Valid POST updates the entry."""
    client.post(f"/entries/{sample_entry}/edit", data={
        "date": "2026-03-10",
        "description": "Updated description",
        "amount": "75.00",
        "entry_type": "credit",
        "category_id": sample_category,
    }, follow_redirects=True)
    with app.app_context():
        entry = Entry.query.get(sample_entry)
        assert entry.description == "Updated description"
        assert entry.amount_cents == 7500


def test_delete_entry(client, sample_entry, app):
    """POST to delete removes the entry."""
    client.post(f"/entries/{sample_entry}/delete", follow_redirects=True)
    with app.app_context():
        assert Entry.query.get(sample_entry) is None


def test_delete_entry_404(client):
    """DELETE on a non-existent entry returns 404."""
    response = client.post("/entries/9999/delete")
    assert response.status_code == 404


def test_ledger_date_filter(client, sample_category, app):
    """Date filter excludes entries outside the range."""
    with app.app_context():
        from app.models import Entry
        from datetime import date as d
        in_range = Entry(date=d(2026, 3, 15), description="In range",
                         amount_cents=1000, entry_type="credit", category_id=sample_category)
        out_of_range = Entry(date=d(2025, 1, 1), description="Out of range",
                             amount_cents=2000, entry_type="credit", category_id=sample_category)
        db.session.add_all([in_range, out_of_range])
        db.session.commit()

    response = client.get("/?start_date=2026-01-01&end_date=2026-12-31")
    assert b"In range" in response.data
    assert b"Out of range" not in response.data

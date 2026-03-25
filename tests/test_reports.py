"""
Tests for financial reports: P&L, Balance Sheet, and CSV export.
"""
from app import db
from app.models import Entry, Category
from datetime import date


def _add_entries(app, income_cat_id, expense_cat_id):
    """Helper: seed two entries for report tests."""
    with app.app_context():
        db.session.add_all([
            Entry(date=date(2026, 3, 1), description="Payment received",
                  amount_cents=20000, entry_type="credit", category_id=income_cat_id),
            Entry(date=date(2026, 3, 5), description="Fuel cost",
                  amount_cents=5000, entry_type="debit", category_id=expense_cat_id),
        ])
        db.session.commit()


def test_pnl_page_loads(client):
    """P&L page renders with no data."""
    response = client.get("/reports/pnl")
    assert response.status_code == 200
    assert b"Profit" in response.data


def test_pnl_totals(client, sample_category, sample_expense_category, app):
    """P&L shows correct income, expense, and net profit totals."""
    _add_entries(app, sample_category, sample_expense_category)
    response = client.get("/reports/pnl?start_date=2026-01-01&end_date=2026-12-31")
    assert b"200.00" in response.data  # income
    assert b"50.00" in response.data   # expense
    assert b"150.00" in response.data  # net profit


def test_pnl_empty_period(client):
    """P&L shows empty state message when no entries exist."""
    response = client.get("/reports/pnl?start_date=2020-01-01&end_date=2020-12-31")
    assert b"No income" in response.data
    assert b"No expenses" in response.data


def test_balance_sheet_page_loads(client):
    """Balance sheet renders with no data."""
    response = client.get("/reports/balance")
    assert response.status_code == 200
    assert b"Balance Sheet" in response.data


def test_balance_sheet_running_balance(client, sample_category, sample_expense_category, app):
    """Balance sheet shows correct running balance after each entry."""
    _add_entries(app, sample_category, sample_expense_category)
    response = client.get("/reports/balance?start_date=2026-01-01&end_date=2026-12-31")
    assert b"200.00" in response.data  # after first credit
    assert b"150.00" in response.data  # after debit: 200 - 50


def test_csv_export(client, sample_category, sample_expense_category, app):
    """CSV export returns correct headers and row data."""
    _add_entries(app, sample_category, sample_expense_category)
    response = client.get("/reports/export?start_date=2026-01-01&end_date=2026-12-31")
    assert response.status_code == 200
    assert response.content_type == "text/csv; charset=utf-8"
    data = response.data.decode()
    assert "Date,Description,Type,Category,Amount" in data
    assert "Payment received" in data
    assert "Fuel cost" in data
    assert "200.00" in data
    assert "50.00" in data


def test_csv_export_filename(client, sample_category, app):
    """CSV export filename includes the date range."""
    response = client.get("/reports/export?start_date=2026-01-01&end_date=2026-03-31")
    disposition = response.headers.get("Content-Disposition", "")
    assert "2026-01-01" in disposition
    assert "2026-03-31" in disposition

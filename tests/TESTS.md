# SimpleBooks Test Suite

Run with: `python -m pytest tests/ -v`

## Setup
`tests/conftest.py` — shared fixtures for all tests.
- `app` fixture: fresh Flask app with in-memory SQLite per test (fully isolated, no dev DB touched)
- `client` fixture: Flask test client
- `sample_category`, `sample_expense_category`, `sample_entry`: seed helpers that return IDs

## Test Files

### `test_models.py`
Covers the `Entry` and `Category` models directly (no HTTP).
- `amount_cents` ↔ `amount_dollars` property getter and setter
- Rounding correctness (e.g. $9.99 → 999 cents, not 998 or 1000)
- `__repr__` output for both models

### `test_entries.py`
Covers all ledger entry routes: list, add, edit, delete, filter.
- Ledger loads empty and with data
- Add entry: happy path, and validation rejections (missing description, bad amount, zero amount, bad date)
- Edit entry: form loads with existing data, update persists correctly
- Delete entry: removes from DB, 404 on missing ID
- Date filter: entries outside range are excluded from results

### `test_reports.py`
Covers P&L, Balance Sheet, and CSV export routes.
- P&L: page loads, income/expense/net totals are correct, empty-period state
- Balance Sheet: page loads, running balance is correct after each entry
- CSV export: correct content-type, headers row, entry data, filename includes date range

### `test_categories.py`
Covers category CRUD routes.
- List page loads and shows income/expense categories separately
- Add: happy path, missing name rejected
- Edit: name update persists
- Delete: removes category with no entries; **blocked** with flash error when entries exist

## What's Not Covered
- UI/visual rendering (use `python screenshots.py` for that)
- CSV import (not a feature yet)
- Multi-user / auth flows (Phase 2)

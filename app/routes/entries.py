"""
Routes for ledger entry CRUD operations.
Handles listing, creating, editing, and deleting entries.
"""
from datetime import date, datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Entry, Category

entries_bp = Blueprint("entries", __name__)


@entries_bp.route("/")
def index():
    """
    Dashboard / entry list.
    Supports optional filtering by date range and category.
    """
    # Read filter parameters from query string
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    category_id = request.args.get("category_id", type=int)

    # Start building the query
    query = Entry.query

    # Apply filters if provided
    if start_date:
        try:
            query = query.filter(Entry.date >= datetime.strptime(start_date, "%Y-%m-%d").date())
        except ValueError:
            pass  # ignore invalid date format, show all

    if end_date:
        try:
            query = query.filter(Entry.date <= datetime.strptime(end_date, "%Y-%m-%d").date())
        except ValueError:
            pass

    if category_id:
        query = query.filter(Entry.category_id == category_id)

    # Order by date descending (newest first)
    entries = query.order_by(Entry.date.desc(), Entry.created_at.desc()).all()

    # Calculate running balance for display
    total_credits = sum(e.amount_cents for e in entries if e.entry_type == "credit")
    total_debits = sum(e.amount_cents for e in entries if e.entry_type == "debit")
    balance_cents = total_credits - total_debits

    categories = Category.query.order_by(Category.name).all()

    return render_template(
        "entries/list.html",
        entries=entries,
        categories=categories,
        balance_cents=balance_cents,
        total_credits=total_credits,
        total_debits=total_debits,
        # Pass filters back to template so form stays filled
        filter_start=start_date or "",
        filter_end=end_date or "",
        filter_category=category_id,
    )


@entries_bp.route("/entries/add", methods=["GET", "POST"])
def add_entry():
    """Show the add-entry form (GET) or create a new entry (POST)."""
    if request.method == "POST":
        return _save_entry(entry=None)

    categories = Category.query.order_by(Category.type, Category.name).all()
    return render_template("entries/form.html", entry=None, categories=categories)


@entries_bp.route("/entries/<int:entry_id>/edit", methods=["GET", "POST"])
def edit_entry(entry_id):
    """Show the edit form (GET) or update an existing entry (POST)."""
    entry = Entry.query.get_or_404(entry_id)

    if request.method == "POST":
        return _save_entry(entry=entry)

    categories = Category.query.order_by(Category.type, Category.name).all()
    return render_template("entries/form.html", entry=entry, categories=categories)


@entries_bp.route("/entries/<int:entry_id>/delete", methods=["POST"])
def delete_entry(entry_id):
    """Delete an entry. POST-only to prevent accidental deletion via GET."""
    entry = Entry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted.", "info")
    return redirect(url_for("entries.index"))


def _save_entry(entry):
    """
    Validate form data and create or update an entry.
    Shared logic for both add and edit routes.

    Args:
        entry: Existing Entry to update, or None to create a new one.
    """
    # Pull values from the submitted form
    entry_date_str = request.form.get("date", "").strip()
    description = request.form.get("description", "").strip()
    amount_str = request.form.get("amount", "").strip()
    entry_type = request.form.get("entry_type", "").strip()
    category_id = request.form.get("category_id", type=int)

    # --- Validation ---
    errors = []

    # Date
    try:
        entry_date = datetime.strptime(entry_date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        errors.append("Please enter a valid date.")
        entry_date = None

    # Description
    if not description:
        errors.append("Description is required.")
    elif len(description) > 300:
        errors.append("Description must be 300 characters or less.")

    # Amount — must be a positive number
    try:
        amount = float(amount_str)
        if amount <= 0:
            errors.append("Amount must be greater than zero.")
    except (ValueError, TypeError):
        errors.append("Please enter a valid amount.")
        amount = None

    # Entry type
    if entry_type not in ("credit", "debit"):
        errors.append("Entry type must be credit or debit.")

    # Category
    if not category_id or not Category.query.get(category_id):
        errors.append("Please select a valid category.")

    # If there are errors, re-show the form with messages
    if errors:
        for error in errors:
            flash(error, "error")
        categories = Category.query.order_by(Category.type, Category.name).all()
        return render_template("entries/form.html", entry=entry, categories=categories), 400

    # --- Save ---
    if entry is None:
        entry = Entry()

    entry.date = entry_date
    entry.description = description
    entry.amount_dollars = amount  # uses the property setter to convert to cents
    entry.entry_type = entry_type
    entry.category_id = category_id

    if entry.id is None:
        db.session.add(entry)

    db.session.commit()
    flash("Entry saved.", "success")
    return redirect(url_for("entries.index"))

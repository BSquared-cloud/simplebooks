"""
Routes for financial reports: Profit & Loss, Balance Sheet, and CSV export.
"""
import csv
import io
from datetime import datetime, date
from flask import Blueprint, render_template, request, Response
from app.models import Entry, Category

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


def _parse_date_range():
    """
    Read start_date and end_date from query params.
    Defaults to the current calendar year if not provided.
    """
    today = date.today()
    default_start = date(today.year, 1, 1)  # Jan 1 of this year
    default_end = today

    start_str = request.args.get("start_date", "")
    end_str = request.args.get("end_date", "")

    try:
        start = datetime.strptime(start_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        start = default_start

    try:
        end = datetime.strptime(end_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        end = default_end

    return start, end


@reports_bp.route("/pnl")
def profit_and_loss():
    """
    Profit & Loss report.
    Shows income and expenses grouped by category for the selected date range.
    """
    start, end = _parse_date_range()

    # Get all entries in the date range
    entries = Entry.query.filter(
        Entry.date >= start,
        Entry.date <= end,
    ).all()

    # Group totals by category
    income_by_category = {}
    expense_by_category = {}

    for entry in entries:
        cat = entry.category
        if entry.entry_type == "credit":
            income_by_category[cat.name] = income_by_category.get(cat.name, 0) + entry.amount_cents
        else:
            expense_by_category[cat.name] = expense_by_category.get(cat.name, 0) + entry.amount_cents

    total_income = sum(income_by_category.values())
    total_expenses = sum(expense_by_category.values())
    net_profit = total_income - total_expenses

    return render_template(
        "reports/pnl.html",
        start=start,
        end=end,
        income_by_category=income_by_category,
        expense_by_category=expense_by_category,
        total_income=total_income,
        total_expenses=total_expenses,
        net_profit=net_profit,
    )


@reports_bp.route("/balance")
def balance_sheet():
    """
    Balance sheet — running balance over time.
    Shows cumulative credits minus debits up to each date.
    """
    start, end = _parse_date_range()

    entries = Entry.query.filter(
        Entry.date >= start,
        Entry.date <= end,
    ).order_by(Entry.date).all()

    # Build a running balance by date
    running_balance = []
    cumulative = 0
    for entry in entries:
        if entry.entry_type == "credit":
            cumulative += entry.amount_cents
        else:
            cumulative -= entry.amount_cents
        running_balance.append({
            "date": entry.date,
            "description": entry.description,
            "credit": entry.amount_cents if entry.entry_type == "credit" else 0,
            "debit": entry.amount_cents if entry.entry_type == "debit" else 0,
            "balance": cumulative,
        })

    return render_template(
        "reports/balance.html",
        start=start,
        end=end,
        rows=running_balance,
        final_balance=cumulative,
    )


@reports_bp.route("/export")
def export_csv():
    """
    Export all entries in the date range as a CSV file.
    Formatted for easy import into tax software or spreadsheets.
    """
    start, end = _parse_date_range()

    entries = Entry.query.filter(
        Entry.date >= start,
        Entry.date <= end,
    ).order_by(Entry.date).all()

    # Build CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Description", "Type", "Category", "Amount"])

    for entry in entries:
        writer.writerow([
            entry.date.isoformat(),
            entry.description,
            entry.entry_type,
            entry.category.name,
            f"{entry.amount_dollars:.2f}",
        ])

    # Return as a downloadable file
    csv_data = output.getvalue()
    filename = f"simplebooks_{start.isoformat()}_to_{end.isoformat()}.csv"

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )

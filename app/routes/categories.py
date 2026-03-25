"""
Routes for category management.
Lets users add, edit, and delete their own categories.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Category, Entry

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")


@categories_bp.route("/")
def list_categories():
    """Show all categories grouped by type."""
    income_cats = Category.query.filter_by(type="income").order_by(Category.name).all()
    expense_cats = Category.query.filter_by(type="expense").order_by(Category.name).all()
    return render_template(
        "categories/list.html",
        income_cats=income_cats,
        expense_cats=expense_cats,
    )


@categories_bp.route("/add", methods=["GET", "POST"])
def add_category():
    """Add a new custom category."""
    if request.method == "POST":
        return _save_category(category=None)
    return render_template("categories/form.html", category=None)


@categories_bp.route("/<int:category_id>/edit", methods=["GET", "POST"])
def edit_category(category_id):
    """Edit an existing category."""
    category = db.get_or_404(Category, category_id)
    if request.method == "POST":
        return _save_category(category=category)
    return render_template("categories/form.html", category=category)


@categories_bp.route("/<int:category_id>/delete", methods=["POST"])
def delete_category(category_id):
    """
    Delete a category. Only allowed if no entries use it.
    This prevents orphaned entries with no category.
    """
    category = db.get_or_404(Category, category_id)

    # Check if any entries reference this category
    entry_count = Entry.query.filter_by(category_id=category.id).count()
    if entry_count > 0:
        flash(f"Can't delete \"{category.name}\" — {entry_count} entry(ies) use this category. "
              "Reassign or delete those entries first.", "error")
        return redirect(url_for("categories.list_categories"))

    db.session.delete(category)
    db.session.commit()
    flash(f"Category \"{category.name}\" deleted.", "info")
    return redirect(url_for("categories.list_categories"))


def _save_category(category):
    """Validate and save a category (create or update)."""
    name = request.form.get("name", "").strip()
    cat_type = request.form.get("type", "").strip()

    errors = []

    if not name:
        errors.append("Category name is required.")
    elif len(name) > 100:
        errors.append("Category name must be 100 characters or less.")

    if cat_type not in ("income", "expense"):
        errors.append("Type must be income or expense.")

    # Check for duplicate name within the same type
    if not errors:
        existing = Category.query.filter_by(name=name, type=cat_type).first()
        if existing and (category is None or existing.id != category.id):
            errors.append(f"A {cat_type} category named \"{name}\" already exists.")

    if errors:
        for error in errors:
            flash(error, "error")
        return render_template("categories/form.html", category=category), 400

    if category is None:
        category = Category(is_default=False, group="custom")

    category.name = name
    category.type = cat_type

    if category.id is None:
        db.session.add(category)

    db.session.commit()
    flash(f"Category \"{name}\" saved.", "success")
    return redirect(url_for("categories.list_categories"))

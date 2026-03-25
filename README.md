# SimpleBooks

A minimal, privacy-first ledger app for gig workers, freelancers, and small property owners.

Track your income and expenses, categorize transactions, and generate reports your accountant will actually use — without the bloat of enterprise accounting software.

## Who This Is For

- **Rideshare/delivery drivers** (Uber, Lyft, DoorDash, etc.)
- **Freelancers and contractors**
- **Small property owners** (1-5 units)
- Anyone who needs basic bookkeeping for taxes but doesn't want QuickBooks

## Features

- Add credits and debits as ledger entries
- 9 default categories covering common self-employment income and expenses
- Custom category management — add, edit, or delete any category
- Filter entries by date range and category
- Profit & Loss report by category
- Balance sheet with running totals
- One-click CSV export for your accountant or tax software
- Dark mode (follows system preference, toggleable)
- Runs locally — your financial data stays on your machine

## Quick Start

**Requirements:** Python 3.10+

```bash
# Clone the repo
git clone https://github.com/BSquared-cloud/simplebooks.git
cd simplebooks

# Set up environment
cp .env.example .env

# Install dependencies
pip install -r requirements.txt

# Run the app
python run.py
```

Open http://localhost:5000 in your browser.

On first launch, 9 default categories are created covering the most common self-employment income and expenses. Add, edit, or delete categories to fit your situation.

## Tech Stack

- **Backend:** Python, Flask, SQLAlchemy
- **Database:** SQLite (zero configuration, single file)
- **Frontend:** Server-rendered templates with Pico CSS

## Project Structure

```
SimpleBooks/
├── run.py              # Entry point — start here
├── config.py           # Configuration (reads .env)
├── app/
│   ├── __init__.py     # Flask app factory
│   ├── models.py       # Entry and Category models
│   ├── seed.py         # Default category templates
│   ├── routes/
│   │   ├── entries.py    # Ledger CRUD
│   │   ├── reports.py    # P&L, balance sheet, CSV export
│   │   └── categories.py # Category management
│   ├── templates/      # Jinja2 HTML templates
│   └── static/css/     # Minimal custom styles
└── tests/              # pytest suite (33 tests)
```

## Contributing

Contributions are welcome. Please open an issue first to discuss what you'd like to change.

## License

This project is licensed under the [GNU Affero General Public License v3.0](LICENSE).

You are free to use, modify, and self-host this software. If you host a modified version as a service for others, you must make your source code available under the same license.

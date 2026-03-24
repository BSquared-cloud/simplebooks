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
- Pre-configured category templates for rideshare, freelance, and property management
- Filter entries by date range and category
- Profit & Loss report by category
- Balance sheet with running totals
- One-click CSV export for your accountant or tax software
- Runs locally — your financial data stays on your machine

## Quick Start

**Requirements:** Python 3.10+

```bash
# Clone the repo
git clone https://github.com/yourusername/SimpleBooks.git
cd SimpleBooks

# Set up environment
cp .env.example .env

# Install dependencies
pip install -r requirements.txt

# Run the app
python run.py
```

Open http://localhost:5000 in your browser.

On first launch, default categories for rideshare, freelance, and property management are automatically created. You can add your own categories as needed.

## Category Templates

SimpleBooks ships with pre-configured categories so you don't have to set everything up from scratch:

| Template | Example Categories |
|----------|-------------------|
| Rideshare/Delivery | Ride Income, Tips, Fuel, Mileage, Platform Fees, Tolls |
| Freelance | Client Income, Software & Tools, Home Office, Marketing |
| Property Management | Rent Income, Repairs, Insurance, Property Tax, Utilities |

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
│   │   ├── entries.py  # Ledger CRUD
│   │   └── reports.py  # P&L, balance sheet, CSV export
│   ├── templates/      # Jinja2 HTML templates
│   └── static/css/     # Minimal custom styles
└── tests/
```

## Contributing

Contributions are welcome. Please open an issue first to discuss what you'd like to change.

## License

This project is licensed under the [GNU Affero General Public License v3.0](LICENSE).

You are free to use, modify, and self-host this software. If you host a modified version as a service for others, you must make your source code available under the same license.

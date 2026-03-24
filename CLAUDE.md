# SimpleBooks — Project CLAUDE.md

## What This Is
A minimal ledger app for gig workers, freelancers, and small property owners.
Two versions planned: open-source self-hosted (Phase 1) and hosted SaaS (Phase 2).

## Current Phase: Phase 1 — Open Source MVP
- Self-hosted, single-user, SQLite-backed
- No auth, no payments, no multi-tenancy yet

## Tech Stack
- **Backend**: Python 3.11+, Flask, SQLAlchemy
- **Database**: SQLite (via SQLAlchemy — designed to swap to Postgres in Phase 2)
- **Frontend**: Jinja2 server-rendered templates, Pico CSS (classless), minimal vanilla JS
- **Reports**: CSV export, HTML views
- **Dev server**: Flask built-in

## Project Structure
```
SimpleBooks/
├── CLAUDE.md              # You are here
├── .env.example           # Environment variable template
├── requirements.txt       # Python dependencies
├── run.py                 # Entry point
├── config.py              # Configuration (reads .env)
├── app/
│   ├── __init__.py        # Flask app factory
│   ├── models.py          # SQLAlchemy models
│   ├── routes/
│   │   ├── __init__.py    # Blueprint registration
│   │   ├── entries.py     # Ledger entry CRUD
│   │   └── reports.py     # P&L, balance sheet, CSV export
│   ├── templates/
│   │   ├── base.html      # Base layout
│   │   ├── entries/
│   │   │   ├── list.html  # Dashboard / entry list
│   │   │   └── form.html  # Add/edit entry
│   │   └── reports/
│   │       ├── pnl.html   # Profit & Loss
│   │       └── balance.html
│   └── static/
│       └── css/
│           └── style.css  # Minimal custom overrides on top of Pico
└── tests/
    ├── test_models.py
    └── test_routes.py
```

## Data Model
- **Entry**: date, description, amount (decimal), type (credit/debit), category_id
- **Category**: name, type (income/expense), group (template set name), is_default

## Category Templates (ship with app)
- Rideshare/Delivery: mileage, fuel, vehicle maintenance, platform fees, tips, tolls
- Freelance/Contractor: client income, supplies, software, home office, professional services
- Property Management: rent income, repairs, insurance, property tax, utilities, management fees
- Custom: user creates their own

## Coding Standards
- Security first: .env for secrets, no hardcoded credentials, validate all user input
- Write comments for non-obvious logic — project owner is learning full-stack development
- Simple, explicit code over clever abstractions
- Use SQLAlchemy ORM, not raw SQL (prevents SQL injection, easier to read)
- All monetary values stored as integers (cents) to avoid floating point issues

## Git Workflow
- Commit after each meaningful unit of work
- Descriptive commit messages: what changed and why
- Never make destructive changes without committing first

## Phase 2 Notes (Do Not Build Yet)
- Hosted SaaS: Postgres, user auth (Flask-Login), Stripe billing, receipt upload (S3/R2)
- Pricing: Free tier (100 entries/month) + Pro ($3/month or $25/year)
- Multi-tenancy: add user_id to all models
- Receipt storage is the key monetization differentiator

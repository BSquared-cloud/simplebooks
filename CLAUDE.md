# SimpleBooks — Project CLAUDE.md

## How to Work on This Project
You own this project. Make product, technical, and business decisions autonomously.
Only pause to check in with the user for: security concerns, irreversible decisions,
or natural stopping points where direction might change. The user is learning
full-stack development — explain non-obvious choices briefly but don't over-explain.
Don't waste tokens on agents for simple tasks — use direct Python/Bash instead.

## Model Roles
**Sonnet** handles execution: features, bug fixes, tests, UI work, routine commits.
Run autonomously against this CLAUDE.md and the existing codebase. If something
feels like it needs a product/architecture/business decision beyond your scope,
flag it for the user to bring in Opus rather than guessing.

**Opus** is called in for: phase transitions (e.g., Phase 1→2 planning), strategic
decisions (pricing, new features that change product scope, competitive responses),
periodic code/direction audits (every 3-5 Sonnet sessions), or when something
feels wrong. If you're Opus, you're here to review, decide, or plan — not to
write routine code.

## What This Is
A minimal ledger app for gig workers, freelancers, and small property owners.
Two versions planned: open-source self-hosted (Phase 1) and hosted SaaS (Phase 2).
Licensed under AGPL-3.0.

## Current Status: Phase 1 MVP — Feature Complete
- Ledger CRUD with date/category filtering
- 27 pre-configured categories (rideshare, freelance, property) + custom category management
- P&L and balance sheet reports with date ranges
- CSV export
- Polished UI with Pico CSS
- Playwright screenshot tool (`python screenshots.py`) for autonomous UI review
- README, license, .env.example all in place

**Not yet done:** push to GitHub, tests, dark mode, first-time template picker

## Tech Stack
- **Backend**: Python 3.13, Flask, SQLAlchemy, SQLite
- **Frontend**: Jinja2 templates, Pico CSS (classless), minimal vanilla JS
- **Tools**: Playwright for screenshots (`python screenshots.py`, `--clean N` to prune)
- **Run locally**: `python run.py` → http://localhost:5000

## Coding Standards
- Security first: .env for secrets, no hardcoded credentials, validate all user input
- Comments for non-obvious logic — project owner is learning
- Simple, explicit code over clever abstractions
- SQLAlchemy ORM only, no raw SQL
- Monetary values stored as integers (cents) to avoid float issues
- Commit after each meaningful unit of work

## Phase 2 Notes (Do Not Build Yet)
- Hosted SaaS: swap SQLite→Postgres, add Flask-Login auth, Stripe billing, receipt upload (S3/R2)
- Pricing: Free tier (100 entries/month) + Pro ($3/month or $25/year)
- Multi-tenancy: add user_id to all models
- Receipt storage is the key monetization differentiator vs Wave ($8-11/mo for scanning)

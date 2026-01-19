# prox-email-pipeline
Prox – Weekly Deals Backend (Track A)

This repository implements Track A (Backend) of the Prox technical assessment.

The system ingests weekly grocery deal data, stores it in a normalized and deduplicated database, generates a branded “Top Deals” email per user based on retailer preferences, and sends the email via a transactional email provider.

The solution is designed to be idempotent, deterministic, and easy to reason about, with database-level guarantees for data correctness.


High-Level Architecture
Stack
    Python 3 – backend logic and orchestration
    Supabase (PostgreSQL) – data storage and deduplication
    Jinja2 – HTML and plain-text email templating
    Resend – email delivery
    Typer – CLI entrypoint
    npm – used only as a task runner (per requirements)

Execution flow
    Ingest deals and users from JSON
    Deduplicate and normalize data in the database
    Generate a “Top 6 Deals” email per user (filtered by preferences)
    Send the email

Database Design

The database is hosted in Supabase (Postgres).

Tables were initially created using the Supabase Table Editor for speed, with critical integrity constraints enforced via SQL.

Core tables:
retailers
products
deals
users

Deduplication strategy:
Deals are deduplicated at the database level using a composite unique constraint:

unique (retailer_id, product_id, start_date)

All deal ingestion uses upserts keyed on this constraint, making the pipeline safe to re-run.

This guarantees: No duplicate deals, Idempotent ingestion, and Database-enforced correctness

Prerequisites
    Python 3.10+
    Node.js (for npm run send:weekly)
    A Supabase project
    A Resend account (API key)

1. Clone the repository
git clone <your-repo-url>
cd <repo-name>

2. Create and populate .env

Copy the example file:
cp .env.example .env

Fill in the values:

SUPABASE_URL=https://<your-project>.supabase.co
SUPABASE_SERVICE_ROLE_KEY=<service_role_key>
RESEND_API_KEY=<resend_api_key>

EMAIL_FROM="Prox Deals <no-reply@example.com>"
MANAGE_PREFS_URL="https://example.com/preferences"


Note: The service_role key is used intentionally for server-side ingestion and is never committed to version control.

3. Install Python dependencies
python3 -m pip install -r requirements.txt

Verify:

python3 -c "import jinja2, resend; print('dependencies installed')"


Running the Pipeline

The full ingestion + email send flow is exposed as a single command, per the assessment requirements.

Run via npm
npm install
npm run send:weekly

Run directly with Python
python -m src.prox.cli send-weekly

Dry run (no emails sent)
python -m src.prox.cli send-weekly --dry-run

Given additional time:
Add a retailer scraper that outputs the same JSON format
Normalize prices by unit (e.g., price per oz / lb)
Add a preview web UI for email QA
Add basic observability (structured logging, metrics)

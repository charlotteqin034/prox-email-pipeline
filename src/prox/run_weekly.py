from .ingest import ingest_deals
from .ingest_users import ingest_users
from .query_deals import get_users, query_deals, group_by_retailer
from .emailer import render_weekly_email
from .config import settings
import typer

def main():
    ingest_deals("data/deals.json")
    ingest_users("data/users.json")

    users = get_users()
    for u in users:
        deals = query_deals(u["preferred_retailers"], limit=6)
        if not deals:
            print(f"Skipping {u['email']} (no deals matched preferences)")
            continue

        grouped = group_by_retailer(deals)
        html, text = render_weekly_email(u["name"], grouped, settings.manage_prefs_url)

        # Dry-run output for validation
        print(f"[DRY RUN] Rendered email for {u['email']} ({len(deals)} deals)")

if __name__ == "__main__":
    main()

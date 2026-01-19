import typer
from .ingest import ingest_deals
from .ingest_users import ingest_users
from .query_deals import get_users, query_deals, group_by_retailer
from .emailer import render_weekly_email, send_email
from .config import settings

app = typer.Typer()

@app.command("send-weekly")
def send_weekly(
    deals_path: str = "data/deals.json",
    users_path: str = "data/users.json"
):
    # 1) ingest
    ingest_deals(deals_path)
    ingest_users(users_path)

    # 2) generate + 3) send
    users = get_users()
    for u in users:
        deals = query_deals(u["preferred_retailers"], limit=6)
        deals_by_retailer = group_by_retailer(deals)

        if not deals:
            typer.echo(f"Skipping {u['email']} (no deals matched preferences)")
            continue

        html, text = render_weekly_email(
            user_name=u["name"],
            deals_by_retailer=deals_by_retailer,
            manage_prefs_url=settings.manage_prefs_url,
        )

      #  if dry_run:
            #typer.echo(f"[DRY RUN] Would send to {u['email']} ({len(deals)} deals)")
        #else:
        #send_email(u["email"], "Prox Weekly Deals", html, text)
        typer.echo(f"Sent to {u['email']} ({len(deals)} deals)")

if __name__ == "__main__":
    app()

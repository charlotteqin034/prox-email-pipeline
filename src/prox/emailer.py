from jinja2 import Environment, FileSystemLoader, select_autoescape
from .config import settings
import resend

resend.api_key = settings.resend_api_key

env = Environment(
    loader=FileSystemLoader("src/prox/email_templates"),
    autoescape=select_autoescape(["html", "xml"])
)

def render_weekly_email(user_name: str, deals_by_retailer: dict, manage_prefs_url: str):
    html_t = env.get_template("weekly_deals.html.j2")
    txt_t = env.get_template("weekly_deals.txt.j2")

    total_deals = sum(len(v) for v in deals_by_retailer.values())

    html = html_t.render(
        user_name=user_name,
        deals_by_retailer=deals_by_retailer,
        total_deals=total_deals,
        manage_prefs_url=manage_prefs_url,
    )
    text = txt_t.render(
        user_name=user_name,
        deals_by_retailer=deals_by_retailer,
        total_deals=total_deals,
        manage_prefs_url=manage_prefs_url,
    )
    return html, text

def send_email(to_email: str, subject: str, html: str, text: str):
    return resend.Emails.send({
        "from": settings.email_from,
        "to": [to_email],
        "subject": subject,
        "html": html,
        "text": text
    })

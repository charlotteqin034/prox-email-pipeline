from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    supabase_url: str = os.environ["SUPABASE_URL"]
    supabase_service_role_key: str = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    resend_api_key: str = os.environ["RESEND_API_KEY"]
    email_from: str = os.environ.get("EMAIL_FROM", "Prox Deals <onboarding@resend.dev>")
    manage_prefs_url: str = os.environ.get("MANAGE_PREFS_URL", "https://example.com/preferences")

settings = Settings()
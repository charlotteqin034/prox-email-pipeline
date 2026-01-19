import json
from pathlib import Path
from .db import supabase


def ingest_users(users_json: str) -> dict:
    users = json.loads(Path(users_json).read_text())

    for user in users:
        res = supabase.table("users").upsert({
            "name": user["name"],
            "email": user["email"],
            "preferred_retailers": user["preferred_retailers"]
        }).execute()

 
    return {"status": "success"}


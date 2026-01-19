import json
from .db import supabase
from pathlib import Path

def get_or_create_retailer_id(name: str) -> int:
    exists = supabase.table("retailers").select("id").eq("name", name).execute()
    if exists.data:
        return exists.data[0]["id"]
    
    created = supabase.table("retailers").insert({"name": name}).execute()

    return created.data[0]["id"]

def get_or_create_product_id(name: str) -> int:
    exists = supabase.table("products").select("id").eq("name", name).execute()
    if exists.data:
        return exists.data[0]["id"]
    
    created = supabase.table("products").insert({"name": name}).execute()

    return created.data[0]["id"]

def ingest_deals(deals_json: str) -> dict:
    #load deals from json and upsert into supabase
    deals = json.loads(Path(deals_json).read_text())

    for deal in deals:
        retailer_id = get_or_create_retailer_id(deal["retailer"])
        product_id = get_or_create_product_id(deal["product"])

        res = supabase.table("deals").upsert({
            "retailer_id": retailer_id,
            "product_id": product_id,
            "price": deal["price"],
            "start_date": deal["start"],
            "end_date": deal["end"]
        }, on_conflict="retailer_id,product_id,start_date").execute()

        
    return {"status": "success"}


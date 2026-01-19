from .db import supabase

def get_users():
    users = supabase.table("users").select("*").execute().data
    return users

def query_deals(preferred_retailer: list[str], limit: int = 6):
    # Query deals for a given preferred retailer
    if not preferred_retailer:
        return []
    
    retailers = (
        supabase.table("retailers")
        .select("id,name")
        .in_("name", preferred_retailer)
        .execute()
        .data
    )

    if not retailers:
        return []
    
    retailer_ids = [retailer["id"] for retailer in retailers]
    retailer_name_by_id = {retailer["id"]: retailer["name"] for retailer in retailers}

    if not retailer_ids:
        return []
    
    
    deals = (supabase.table("deals")
        .select("retailer_id, product_id, price, start_date, end_date")
        .in_("retailer_id", retailer_ids)
        .execute()
        .data)
    
    product_ids = list({deal["product_id"] for deal in deals})
    products = (
        supabase.table("products")
        .select("id,name,size,category")
        .in_("id", product_ids)
        .execute()
        .data
    )
    product_by_id = {product["id"]: product for product in products}

    # Normalize for template
    normalized = []
    for d in deals:
        p = product_by_id.get(d["product_id"], {})
        normalized.append({
            "retailer": retailer_name_by_id.get(d["retailer_id"], "Unknown"),
            "product": p.get("name", "Unknown"),
            "size": p.get("size", ""),
            "category": p.get("category", ""),
            "price": float(d["price"]),
            "start_date": d["start_date"],
            "end_date": d["end_date"],
        })

    return normalized
    
def group_by_retailer(deals: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for d in deals:
        grouped.setdefault(d["retailer"], []).append(d)
    return grouped


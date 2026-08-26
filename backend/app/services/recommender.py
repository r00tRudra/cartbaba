import json
import re

from app.agents.search_agent import search_products
from app.agents.ranking_agent import rank_products


# -----------------------------
# 🧠 Helper: safe JSON parser
# -----------------------------
def safe_json_loads(text):
    try:
        return json.loads(text)
    except (TypeError, json.JSONDecodeError):
        return {}


def extract_intent(query: str) -> dict:
    price_match = re.search(r"(?:under|below|less than|upto|up to)\s*[₹$]?\s*([\d,]+)", query, re.IGNORECASE)
    words = query.lower().split()
    known_categories = ("shoes", "shoe", "phone", "phones", "laptop", "laptops", "bag", "bags", "headphones", "mouse", "tablet", "watch")
    category = next((word for word in words if word in known_categories), None)
    gender = next((value for value in ("men", "women", "unisex") if value in words), None)
    use_case = next((value for value in ("running", "casual", "formal", "gaming", "office") if value in words), None)

    return {
        "category": category or query.strip(),
        "max_price": int(price_match.group(1).replace(",", "")) if price_match else None,
        "gender": gender,
        "use_case": use_case,
    }


def run_cartbaba(query: str):
    intent_data = extract_intent(query)
    products = search_products(intent_data)
    ranked_products = rank_products(products, query)
    top_product = ranked_products[0]["name"] if ranked_products else "No matching products"

    return {
        "query": query,
        "intent": intent_data,
        "products": ranked_products,
        "results": ranked_products,
        "final": f"Top recommendation: {top_product}",
    }

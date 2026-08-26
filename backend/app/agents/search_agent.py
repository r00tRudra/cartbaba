import requests
import random

def search_products(intent: dict, limit: int = 3):
    query = " ".join(filter(None, [
        intent.get("category"),
        intent.get("gender"),
        intent.get("use_case")
    ])).strip()

    if not query:
        query = "products"

    print("🔍 QUERY:", query)

    # =========================
    # 1. TRY REAL API
    # =========================
    url = f"https://dummyjson.com/products/search?q={query}"
    res = requests.get(url, timeout=10)

    products = []

    if res.status_code == 200:
        data = res.json()

        for item in data.get("products", []):
            product = {
                "name": item["title"],
                "price": float(item["price"]),
                "rating": float(item["rating"]),
                "image": item["thumbnail"]
            }

            max_price = intent.get("max_price")
            if max_price is not None and product["price"] > max_price:
                continue

            products.append(product)

            if len(products) >= limit:
                break

    # =========================
    # 2. FALLBACK (DYNAMIC FAKE DATA)
    # =========================
    if not products:
        print("⚠️ Using fallback products")

        base_names = [
            "Premium", "Stylish", "Classic", "Trendy", "Elegant"
        ]

        for i in range(limit):
            product = {
                "name": f"{random.choice(base_names)} {query.title()} {i+1}",
                "price": round(random.uniform(500, 5000), 2),
                "rating": round(random.uniform(3.5, 4.8), 2),
                "image": "https://via.placeholder.com/300"
            }
            products.append(product)

    print("✅ PRODUCTS:", len(products))
    return products

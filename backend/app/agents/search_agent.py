import requests
import random

def search_products(intent: dict, limit: int = 33):
    query = " ".join(filter(None, [
        intent.get("category"),
        intent.get("gender"),
        intent.get("use_case")
    ])).strip()

    if not query:
        query = "products"

    print("🔍 QUERY:", query)

    # =========================
    # 1. TRY REAL APIimport requests


def search_products(intent: dict, limit: int = 33):
    # =========================
    # 1. BUILD SEARCH QUERY
    # =========================

    query_parts = [
        intent.get("category"),
        intent.get("subcategory"),
        intent.get("product_type"),
        intent.get("gender"),
        intent.get("use_case"),
        intent.get("activity"),
        intent.get("color"),
        intent.get("material"),
        intent.get("style"),
        intent.get("weight_preference"),
    ]

    # Add preferred brands
    brands = intent.get("brand", [])
    if brands:
        query_parts.extend(brands)

    # Add important keywords
    keywords = intent.get("keywords", [])
    if keywords:
        query_parts.extend(keywords)

    # Add mandatory requirements
    must_have = intent.get("must_have", [])
    if must_have:
        query_parts.extend(must_have)

    # Remove duplicates while preserving order
    query_parts = list(dict.fromkeys(
        str(item).strip()
        for item in query_parts
        if item
    ))

    query = " ".join(query_parts).strip()

    if not query:
        query = "products"

    print("🔍 QUERY:", query)

    # =========================
    # 2. CALL REAL API
    # =========================

    url = "https://dummyjson.com/products/search"

    try:
        res = requests.get(
            url,
            params={
                "q": query,
                "limit": limit
            },
            timeout=10
        )

        res.raise_for_status()

    except requests.RequestException as e:
        print("❌ PRODUCT API ERROR:", str(e))

        return {
            "success": False,
            "message": "There is some problem while searching for products.",
            "products": []
        }

    # =========================
    # 3. PARSE RESPONSE
    # =========================

    data = res.json()
    products = []

    for item in data.get("products", []):

        product = {
            "name": item.get("title"),
            "description": item.get("description"),
            "category": item.get("category"),
            "brand": item.get("brand"),
            "price": float(item.get("price", 0)),
            "rating": float(item.get("rating", 0)),
            "discount": float(item.get("discountPercentage", 0)),
            "image": item.get("thumbnail")
        }

        # =========================
        # 4. PRICE FILTER
        # =========================

        min_price = intent.get("min_price")
        max_price = intent.get("max_price")

        if min_price is not None:
            if product["price"] < float(min_price):
                continue

        if max_price is not None:
            if product["price"] > float(max_price):
                continue

        # =========================
        # 5. RATING FILTER
        # =========================

        rating_min = intent.get("rating_min")

        if rating_min is not None:
            if product["rating"] < float(rating_min):
                continue

        # =========================
        # 6. BRAND FILTER
        # =========================

        preferred_brands = intent.get("brand", [])

        if preferred_brands and product["brand"]:
            product_brand = product["brand"].lower()

            if not any(
                brand.lower() in product_brand
                for brand in preferred_brands
            ):
                continue

        # =========================
        # 7. EXCLUDED BRANDS
        # =========================

        excluded_brands = intent.get("exclude_brands", [])

        if product["brand"]:
            product_brand = product["brand"].lower()

            if any(
                brand.lower() in product_brand
                for brand in excluded_brands
            ):
                continue

        # =========================
        # 8. ADD PRODUCT
        # =========================

        products.append(product)

        if len(products) >= limit:
            break

    # =========================
    # 9. NO RESULTS
    # =========================

    if not products:
        print("⚠️ No matching products found")

        return {
            "success": False,
            "message": "No products matching your requirements were found.",
            "products": []
        }

    print("✅ PRODUCTS:", len(products))

    return {
        "success": True,
        "message": "Products found successfully.",
        "products": products
    }
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

import numpy as np

from app.core.config import settings

model = None

def rank_products(products, query):
    global model
    if not products:
        return []

    if model is None:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(settings.EMBEDDING_MODEL)

    query_emb = model.encode(query, normalize_embeddings=True)

    for p in products:
        text = p["name"]
        emb = model.encode(text, normalize_embeddings=True)
        similarity = float(np.dot(query_emb, emb))

        score = (0.7 * similarity) + (0.3 * (p.get("rating", 3) / 5))
        p["score"] = float(score)

    return sorted(products, key=lambda x: x["score"], reverse=True)

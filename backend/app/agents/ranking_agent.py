from sentence_transformers import SentenceTransformer
import numpy as np

from app.core.config import settings

model = SentenceTransformer(settings.EMBEDDING_MODEL)

def rank_products(products, query):
    query_emb = model.encode(query)

    for p in products:
        text = p["name"]
        emb = model.encode(text)

        similarity = np.dot(query_emb, emb) / (
            np.linalg.norm(query_emb) * np.linalg.norm(emb)
        )

        score = (0.7 * similarity) + (0.3 * p.get("rating", 3))
        p["score"] = float(score)

    return sorted(products, key=lambda x: x["score"], reverse=True)

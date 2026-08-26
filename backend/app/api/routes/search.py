from fastapi import APIRouter, Query
from app.services.recommender import run_cartbaba

router = APIRouter(prefix="/search")

@router.post("")
@router.post("/")
def search(query: str = Query(..., min_length=2, max_length=200)):
    return run_cartbaba(query)

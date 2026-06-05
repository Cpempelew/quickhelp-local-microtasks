from fastapi import APIRouter

from app.schemas.reviews import AvisCreate
from app.services.review_service import post_review

router = APIRouter(tags=["avis"])


@router.post("/avis")
def poster_avis(review: AvisCreate):
    return post_review(review)

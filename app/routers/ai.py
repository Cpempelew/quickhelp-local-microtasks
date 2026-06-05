from fastapi import APIRouter

from app.schemas.ai import SuggestRequest
from app.services.ai_service import suggest_text

router = APIRouter(prefix="/api", tags=["ia"])


@router.post("/suggest")
def suggest(req: SuggestRequest):
    return suggest_text(req)

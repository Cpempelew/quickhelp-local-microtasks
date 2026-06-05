from fastapi import APIRouter

from app.services.category_service import list_categories

router = APIRouter(tags=["categories"])


@router.get("/categories")
def get_categories():
    return list_categories()

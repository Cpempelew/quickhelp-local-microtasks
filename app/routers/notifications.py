from fastapi import APIRouter

from app.services.notification_service import get_notifications

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/{user_id}")
def notifications(user_id: int):
    return get_notifications(user_id)

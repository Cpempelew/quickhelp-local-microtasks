from fastapi import APIRouter

from app.schemas.users import UpdatePosition
from app.services.profile_service import get_profile, get_user_reviews, get_wallet, update_position

router = APIRouter(prefix="/utilisateurs", tags=["utilisateurs"])


@router.put("/{user_id}/position")
def update_user_position(user_id: int, req: UpdatePosition):
    return update_position(user_id, req)


@router.get("/{user_id}")
def get_profil(user_id: int):
    return get_profile(user_id)


@router.get("/{user_id}/avis")
def get_avis_recus(user_id: int):
    return get_user_reviews(user_id)


@router.get("/{user_id}/wallet")
def user_wallet(user_id: int):
    return get_wallet(user_id)

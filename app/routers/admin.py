from fastapi import APIRouter

from app.core.config import ADMIN_EMAIL
from app.core.security import check_admin
from app.services.admin_service import get_stats, list_missions, list_transactions, list_users

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
def admin_stats(email: str = ADMIN_EMAIL):
    check_admin(email)
    return get_stats()


@router.get("/missions")
def admin_missions(email: str = ADMIN_EMAIL):
    check_admin(email)
    return list_missions()


@router.get("/utilisateurs")
def admin_utilisateurs(email: str = ADMIN_EMAIL):
    check_admin(email)
    return list_users()


@router.get("/transactions")
def admin_transactions(email: str = ADMIN_EMAIL):
    check_admin(email)
    return list_transactions()

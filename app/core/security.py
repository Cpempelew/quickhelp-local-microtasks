from fastapi import HTTPException

from app.core.config import ADMIN_EMAIL


def check_admin(email: str):
    if email != ADMIN_EMAIL:
        raise HTTPException(403, "Acces reserve a l'administrateur")

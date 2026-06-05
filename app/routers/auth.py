from fastapi import APIRouter

from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.auth_service import login_user, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(req: LoginRequest):
    return login_user(req)


@router.post("/register")
def register(req: RegisterRequest):
    return register_user(req)

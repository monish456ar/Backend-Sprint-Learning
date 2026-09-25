from typing import Any, Dict
from fastapi import APIRouter
from app.handlers import auth_handler
from app.schemas.auth_schemas import UserRegister, UserLogin

router = APIRouter(tags=["Auth / Users"])


@router.post("/auth/register", summary="Register new user")
def register_user(payload: UserRegister) -> Dict[str, Any]:
    return auth_handler.handle_register(payload.model_dump())


@router.post("/auth/login", summary="User login")
def login_user(payload: UserLogin) -> Dict[str, Any]:
    return auth_handler.handle_login(payload.model_dump())


@router.get("/users/me", summary="Get current user profile")
def get_current_user() -> Dict[str, Any]:
    return auth_handler.handle_get_me()


@router.get("/admin/stats", summary="Get platform admin statistics")
def get_admin_stats() -> Dict[str, Any]:
    return auth_handler.handle_get_admin_stats()

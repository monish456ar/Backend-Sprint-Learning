from typing import Any, Dict
from fastapi import APIRouter, Depends, status
from app.handlers import auth_handler
from app.schemas.auth_schemas import UserRegister, UserLogin, UserResponse
from app.dependencies import get_config, Settings

router = APIRouter(tags=["Auth / Users"])


@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Register new user")
def register_user(payload: UserRegister) -> UserResponse:
    result = auth_handler.handle_register(payload.model_dump())
    return result["data"]


@router.post("/auth/login", summary="User login")
def login_user(payload: UserLogin) -> Dict[str, Any]:
   
    return auth_handler.handle_login(payload.model_dump())


@router.get("/users/me", response_model=UserResponse, summary="Get current user profile (Password safely omitted)")
def get_current_user(config: Settings = Depends(get_config)) -> UserResponse:
    result = auth_handler.handle_get_me()
    print("Injected database_url via DI:", config.database_url)
    return result["data"]


@router.get("/admin/stats", summary="Get platform admin statistics")
def get_admin_stats() -> Dict[str, Any]:
    return auth_handler.handle_get_admin_stats()

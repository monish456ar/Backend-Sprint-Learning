from typing import Any, Dict
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.handlers import auth_handler
from app.schemas.auth_schemas import UserRegister, UserLogin, UserResponse
from app.dependencies import get_config, get_db, Settings

router = APIRouter(tags=["Auth / Users"])


@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Register new user")
async def register_user(
    payload: UserRegister,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    user = await auth_handler.handle_register(db, payload.model_dump())
    return user


@router.post("/auth/login", summary="User login")
async def login_user(
    payload: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    return await auth_handler.handle_login(db, payload.model_dump())


@router.get("/users/me", response_model=UserResponse, summary="Get current user profile (Password safely omitted)")
async def get_current_user(
    db: AsyncSession = Depends(get_db),
    config: Settings = Depends(get_config),
) -> UserResponse:
    user = await auth_handler.handle_get_me(db)
    return user


@router.get("/users/by-email", response_model=UserResponse, summary="Find user by email")
async def get_user_by_email(
    email: str,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    return await auth_handler.handle_get_user_by_email(db, email)


@router.get("/admin/stats", summary="Get platform admin statistics")
async def get_admin_stats(
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    return await auth_handler.handle_get_admin_stats(db)

from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.user_dao import UserDAO
from app.exceptions.domain_exceptions import UserAlreadyExistsError
from app.models.user import User


async def register_user(db: AsyncSession, user_data: Dict[str, Any]) -> User:
    """Registers a user after checking uniqueness via UserDAO."""
    existing_by_email = await UserDAO.get_user_by_email(db, user_data["email"])
    if existing_by_email:
        raise UserAlreadyExistsError("email", user_data["email"])

    existing_by_username = await UserDAO.get_user_by_username(db, user_data["username"])
    if existing_by_username:
        raise UserAlreadyExistsError("username", user_data["username"])

    return await UserDAO.create_user(db, user_data)


async def login_user(
    db: AsyncSession, credentials: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Authenticates credentials via UserDAO."""
    return await UserDAO.authenticate_user(db, credentials)


async def get_current_user_profile(db: AsyncSession) -> Optional[User]:
    """Retrieves current user via UserDAO."""
    return await UserDAO.get_current_user(db)


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """Finds user by email via UserDAO."""
    return await UserDAO.get_user_by_email(db, email)


async def get_platform_admin_stats(db: AsyncSession) -> Dict[str, Any]:
    """Calculates administrative stats via UserDAO."""
    return await UserDAO.get_admin_stats(db)

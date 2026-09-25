from typing import Any, Dict, Optional
from app.daos import user_dao


def register_user(user_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return user_dao.create_user(user_data)


def login_user(credentials: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return user_dao.authenticate_user(credentials)


def get_current_user_profile() -> Dict[str, Any]:
    return user_dao.get_current_user()


def get_platform_admin_stats() -> Dict[str, Any]:
    return user_dao.get_admin_stats()

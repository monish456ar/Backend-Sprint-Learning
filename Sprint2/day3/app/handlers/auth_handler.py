from typing import Any, Dict, Optional
from app.services import auth_service


def handle_register(user_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    dao_result = auth_service.register_user(user_data)
    return {
        "message": "Handler: User registration processed",
        "data": dao_result.get("user", dao_result),
    }


def handle_login(credentials: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    data = auth_service.login_user(credentials)
    return {
        "message": "Handler: User login processed",
        "data": data,
    }


def handle_get_me() -> Dict[str, Any]:
    data = auth_service.get_current_user_profile()
    return {
        "message": "Handler: Current user profile processed",
        "data": data,
    }


def handle_get_admin_stats() -> Dict[str, Any]:
    data = auth_service.get_platform_admin_stats()
    return {
        "message": "Handler: Admin statistics processed",
        "data": data,
    }

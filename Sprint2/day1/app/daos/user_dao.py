from typing import Any, Dict, Optional


def create_user(user_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    data = user_data or {}
    return {
        "status": "registered",
        "message": "User registered via user_dao placeholder",
        "user": {
            "user_id": 1,
            "username": data.get("username", "demo_user"),
            "email": data.get("email", "demo@example.com"),
            "role": "user",
        },
        "source": "user_dao",
    }


def authenticate_user(credentials: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    creds = credentials or {}
    return {
        "status": "authenticated",
        "access_token": "placeholder-token-dao",
        "token_type": "bearer",
        "username": creds.get("username", "demo_user"),
        "source": "user_dao",
    }


def get_current_user() -> Dict[str, Any]:
    return {
        "user_id": 1,
        "username": "demo_user",
        "email": "demo@example.com",
        "role": "user",
        "source": "user_dao",
    }


def get_admin_stats() -> Dict[str, Any]:
    return {
        "total_users": 150,
        "total_films": 42,
        "total_reviews": 310,
        "source": "user_dao",
    }

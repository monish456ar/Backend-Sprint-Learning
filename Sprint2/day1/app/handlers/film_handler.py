from typing import Any, Dict, Optional
from app.services import film_service


def handle_get_all_films() -> Dict[str, Any]:
    data = film_service.list_films()
    return {
        "message": "Handler: Retrieved all films successfully",
        "data": data,
    }


def handle_get_film(film_id: int) -> Dict[str, Any]:
    data = film_service.retrieve_film(film_id)
    return {
        "message": f"Handler: Retrieved film {film_id} successfully",
        "data": data,
    }


def handle_create_film(film_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    data = film_service.add_film(film_data)
    return {
        "message": "Handler: Created film successfully",
        "data": data,
    }


def handle_update_film(film_id: int, film_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    data = film_service.modify_film(film_id, film_data)
    return {
        "message": f"Handler: Updated film {film_id} successfully",
        "data": data,
    }


def handle_delete_film(film_id: int) -> Dict[str, Any]:
    data = film_service.remove_film(film_id)
    return {
        "message": f"Handler: Deleted film {film_id} successfully",
        "data": data,
    }

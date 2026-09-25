from typing import Any, Dict, List, Optional
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
    dao_result = film_service.add_film(film_data)
    return {
        "message": "Handler: Created film successfully",
        "data": dao_result.get("film", dao_result),
    }


def handle_filter_films(filter_data: Dict[str, Any]) -> Dict[str, Any]:
    start_year = filter_data.get("start_year", 0)
    end_year = filter_data.get("end_year", 9999)
    data = film_service.filter_films(start_year, end_year)
    return {
        "message": f"Handler: Filtered films between {start_year} and {end_year}",
        "data": data,
    }


def handle_update_film(film_id: int, film_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    dao_result = film_service.modify_film(film_id, film_data)
    return {
        "message": f"Handler: Updated film {film_id} successfully",
        "data": dao_result.get("film", dao_result),
    }


def handle_delete_film(film_id: int) -> Dict[str, Any]:
    data = film_service.remove_film(film_id)
    return {
        "message": f"Handler: Deleted film {film_id} successfully",
        "data": data,
    }

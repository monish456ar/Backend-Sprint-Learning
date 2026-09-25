from typing import Any, Dict, List, Optional
from app.daos import film_dao


def list_films() -> List[Dict[str, Any]]:
    return film_dao.get_all_films()


def retrieve_film(film_id: int) -> Dict[str, Any]:
    return film_dao.get_film_by_id(film_id)


def add_film(film_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return film_dao.create_film(film_data)


def modify_film(film_id: int, film_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return film_dao.update_film(film_id, film_data)


def remove_film(film_id: int) -> Dict[str, Any]:
    return film_dao.delete_film(film_id)

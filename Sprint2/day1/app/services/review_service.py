from typing import Any, Dict, List, Optional
from app.daos import review_dao


def list_reviews_for_film(film_id: int) -> List[Dict[str, Any]]:
    return review_dao.get_reviews_for_film(film_id)


def add_review_for_film(film_id: int, review_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return review_dao.create_review_for_film(film_id, review_data)


def modify_review(review_id: int, review_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return review_dao.update_review(review_id, review_data)


def remove_review(review_id: int) -> Dict[str, Any]:
    return review_dao.delete_review(review_id)

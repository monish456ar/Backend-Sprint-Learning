from typing import Any, Dict, Optional
from app.services import review_service


def handle_get_reviews_for_film(film_id: int) -> Dict[str, Any]:
    data = review_service.list_reviews_for_film(film_id)
    return {
        "message": f"Handler: Retrieved reviews for film {film_id} successfully",
        "data": data,
    }


def handle_create_review_for_film(film_id: int, review_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    dao_result = review_service.add_review_for_film(film_id, review_data)
    return {
        "message": f"Handler: Created review for film {film_id} successfully",
        "data": dao_result.get("review", dao_result),
    }


def handle_update_review(review_id: int, review_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    dao_result = review_service.modify_review(review_id, review_data)
    return {
        "message": f"Handler: Updated review {review_id} successfully",
        "data": dao_result.get("review", dao_result),
    }


def handle_delete_review(review_id: int) -> Dict[str, Any]:
    data = review_service.remove_review(review_id)
    return {
        "message": f"Handler: Deleted review {review_id} successfully",
        "data": data,
    }

from typing import Any, Dict, List, Optional


def get_reviews_for_film(film_id: int) -> List[Dict[str, Any]]:
    return [
        {
            "review_id": 101,
            "film_id": film_id,
            "rating": 5,
            "comment": "Great movie placeholder",
            "source": "review_dao",
        }
    ]


def create_review_for_film(film_id: int, review_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    data = review_data or {}
    return {
        "status": "created",
        "message": f"Review for film {film_id} persisted via review_dao placeholder",
        "review": {
            "review_id": 102,
            "film_id": film_id,
            "rating": data.get("rating", 5),
            "comment": data.get("comment", "Placeholder comment"),
        },
        "source": "review_dao",
    }


def update_review(review_id: int, review_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    data = review_data or {}
    return {
        "status": "updated",
        "message": f"Review {review_id} updated via review_dao placeholder",
        "review": {
            "review_id": review_id,
            "rating": data.get("rating", 4),
            "comment": data.get("comment", "Updated review comment"),
        },
        "source": "review_dao",
    }


def delete_review(review_id: int) -> Dict[str, Any]:
    return {
        "status": "deleted",
        "review_id": review_id,
        "message": f"Review {review_id} deleted via review_dao placeholder",
        "source": "review_dao",
    }

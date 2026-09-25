from typing import Any, Dict, List, Optional


def get_all_films() -> List[Dict[str, Any]]:
    return [
        {
            "film_id": 1,
            "title": "Inception",
            "genre": "Sci-Fi",
            "release_year": 2010,
            "director": "Christopher Nolan",
            "source": "film_dao",
        },
        {
            "film_id": 2,
            "title": "The Dark Knight",
            "genre": "Action",
            "release_year": 2008,
            "director": "Christopher Nolan",
            "source": "film_dao",
        },
    ]


def get_film_by_id(film_id: int) -> Dict[str, Any]:
    return {
        "film_id": film_id,
        "title": f"Placeholder Film {film_id}",
        "genre": "Drama",
        "release_year": 2024,
        "director": "Jane Doe",
        "source": "film_dao",
    }


def create_film(film_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    data = film_data or {}
    return {
        "status": "created",
        "message": "Film record persisted via film_dao placeholder",
        "film": {
            "film_id": 999,
            "title": data.get("title", "Untitled Film"),
            "genre": data.get("genre", "Drama"),
            "release_year": data.get("release_year", 2024),
            "director": data.get("director", "Jane Doe"),
        },
        "source": "film_dao",
    }


def filter_films_by_year(start_year: int, end_year: int) -> List[Dict[str, Any]]:
    all_films = get_all_films()
    return [f for f in all_films if start_year <= f["release_year"] <= end_year]


def update_film(film_id: int, film_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    data = film_data or {}
    return {
        "status": "updated",
        "message": f"Film {film_id} updated via film_dao placeholder",
        "film": {
            "film_id": film_id,
            "title": data.get("title", f"Film {film_id}"),
            "genre": data.get("genre", "Drama"),
            "release_year": data.get("release_year", 2024),
            "director": data.get("director", "Jane Doe"),
        },
        "source": "film_dao",
    }


def delete_film(film_id: int) -> Dict[str, Any]:
    return {
        "status": "deleted",
        "film_id": film_id,
        "message": f"Film {film_id} deleted via film_dao placeholder",
        "source": "film_dao",
    }

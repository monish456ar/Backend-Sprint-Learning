import logging
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.film_dao import FilmDAO
from app.dao.review_dao import ReviewDAO
from app.dependencies import get_db

logger = logging.getLogger("ui_routes")

# Templates directory inside app/
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter(tags=["UI - Server-Rendered Views"])


@router.get("/films", response_class=HTMLResponse, summary="Film Search Page")
async def get_films_page(request: Request):
    """Renders the full HTML search page."""
    return templates.TemplateResponse(
        request=request,
        name="films.html",
        context={},
    )



@router.get("/films/search", response_class=HTMLResponse, summary="Film Search HTML Fragment")
async def search_films_fragment(
    request: Request,
    q: Optional[str] = "",
    db: AsyncSession = Depends(get_db),
):
    """
    Renders and returns only the HTML fragment for film-card results.
    Never returns JSON.
    """
    search_term = (q or "").strip()
    films = await FilmDAO.search_films(db, search_term)
    logger.info(f"UI Film search executed: query='{search_term}', matched={len(films)} films")

    film_ids = [film.id for film in films]
    ratings_map = await ReviewDAO.get_average_ratings_for_films(db, film_ids)

    films_data = []
    for film in films:
        films_data.append({
            "id": film.id,
            "title": film.title,
            "release_year": film.release_year,
            "genre": film.genre,
            "director": film.director,
            "hero": film.hero,
            "average_rating": ratings_map.get(film.id),
        })


    return templates.TemplateResponse(
        request=request,
        name="partials/film_cards.html",
        context={
            "films": films_data,
            "query": search_term,
        },
    )

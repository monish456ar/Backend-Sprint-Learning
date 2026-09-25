from typing import List, Literal
import functools

from data import get_countries
from models import Country, Continent
from exceptions import UnknownCountryCodeError, UnsupportedSortFieldError, InvalidQueryParameterError
from decorators import log_query


def print_countries(countries: List[Country]) -> None:
    if not countries:
        print("  (no results)")
        return
    for c in countries:
        enriched = "*" if getattr(c, "enriched", False) else ""
        print(f"  {c.iso_code}: {c.name} ({c.continent.value}){enriched}")
        print(f"    Population: {c.population:,}  Area: {c.area_km2:,} km²")
        print(f"    Languages: {', '.join(c.languages)}  Currency: {c.currency}")
        if c.neighbours:
            print(f"    Neighbours: {', '.join(c.neighbours)}")
        print()


@log_query
def filter_by_continent(continent: Continent) -> List[Country]:
    """Return countries belonging to the given continent.
    """
    result = [c for c in get_countries() if c.continent == continent]
    if not result:
        raise InvalidQueryParameterError(f"No countries found for continent '{continent.name}'. Dataset may not contain this continent.")
    return result

@log_query
def sort_countries(field: Literal["population", "area"], descending: bool = False) -> List[Country]:
    """Sort countries by population or area.
    """
    if field not in ("population", "area"):
        raise UnsupportedSortFieldError(field)
    key_func = (lambda c: c.population) if field == "population" else (lambda c: c.area_km2)
    return sorted(get_countries(), key=key_func, reverse=descending)

@log_query
def find_by_neighbours(neighbour_codes: List[str]) -> List[Country]:
    # Find countries that share any of the supplied neighbour ISO codes.
    if not neighbour_codes:
        raise InvalidQueryParameterError('neighbour_codes list cannot be empty')
    result = []
    for c in get_countries():
        if set(c.neighbours) & set(neighbour_codes):
            result.append(c)
    return result

@log_query
def top_n(field: Literal["population", "area"], n: int) -> List[Country]:
    """Return the top N countries by the specified field.
    """
    if n <= 0:
        raise InvalidQueryParameterError('n must be a positive integer')
    sorted_list = sort_countries(field, descending=True)
    return sorted_list[:n]

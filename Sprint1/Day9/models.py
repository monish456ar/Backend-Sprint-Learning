from dataclasses import dataclass, field
from enum import Enum
from typing import List

class Continent(Enum):
    AFRICA = "Africa"
    ASIA = "Asia"
    EUROPE = "Europe"
    NORTH_AMERICA = "North America"
    SOUTH_AMERICA = "South America"
    OCEANIA = "Oceania"
    ANTARCTICA = "Antarctica"


# print(Continent["africa".upper()])
@dataclass
class Country:
    """Typed model representing a country."""
    name: str
    iso_code: str                     # ISO‑3166‑1 alpha‑3 code, e.g. "USA"
    population: int
    area_km2: float
    continent: Continent
    languages: List[str] = field(default_factory=list)
    currency: str = ""
    neighbours: List[str] = field(default_factory=list)
    enriched: bool = False  # becomes True after enrichment

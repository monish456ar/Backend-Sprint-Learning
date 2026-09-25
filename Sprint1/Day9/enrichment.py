import asyncio
import random
from typing import List
from decorators import QUERY_LOG
from data import get_countries
from models import Country

async def enrich_countries(iso_codes: List[str]) -> List[str]:
    """Enrich the specified countries asynchronously.

    Returns a list of ISO codes that were successfully enriched. Each enrichment is
    also recorded in ``QUERY_LOG`` so that option 7 can display it.
    """
    iso_set = {code.upper() for code in iso_codes}
    countries = get_countries()
    country_map = {c.iso_code.upper(): c for c in countries}

    enriched_iso: List[str] = []
    async def _enrich_one(country: Country, iso: str) -> None:
        await asyncio.sleep(random.uniform(0.3, 1.5))
        setattr(country, "enriched", True)
        enriched_iso.append(iso)
        # Record enrichment in the query log for visibility in option 7
        QUERY_LOG.append({
            "function": "enrich_countries",
            "args": (iso,),
            "kwargs": {},
        })

    tasks = []
    for iso in iso_set:
        country = country_map.get(iso)
        if country is not None:
            tasks.append(_enrich_one(country, iso))
    if tasks:
        await asyncio.gather(*tasks)
    return enriched_iso

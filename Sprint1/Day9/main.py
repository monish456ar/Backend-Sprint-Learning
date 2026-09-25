import asyncio
from typing import List

from data import get_countries
from models import Country, Continent
from queries import (
    filter_by_continent,
    sort_countries,
    find_by_neighbours,
    top_n,print_countries
)
from enrichment import enrich_countries
from decorators import QUERY_LOG
from exceptions import CountryError




def display_menu() -> None:
    print("\n" + "=" * 50)
    print("        COUNTRY DATA CLI")
    print("=" * 50)
    print("1. List all countries")
    print("2. Filter by continent")
    print("3. Sort countries")
    print("4. Find by neighbours")
    print("5. Top-N countries")
    print("6. Enrich country data (async)")
    print("7. Show query log")
    print("8. Exit")


async def handle_choice(choice: str) -> bool:
    if choice == "1":
        print_countries(get_countries())
    elif choice == "2":
        cont = input("Enter continent (e.g., Asia): ").strip()
        try:
            continent = Continent[cont.upper()]
            print_countries(filter_by_continent(continent))
        except KeyError:
            print(f"Error: unknown continent '{cont}'.")
        except CountryError as e:
            print(f"Error: {e}")
    elif choice == "3":
        field = input("Sort field ('population' or 'area'): ").strip().lower()
        order = input("Descending? (y/n): ").strip().lower()
        descending = order.startswith('y')
        try:
            print_countries(sort_countries(field, descending))
        except CountryError as e:
            print(f"Error: {e}")
    elif choice == "4":
        codes = input("Comma‑separated neighbour ISO codes: ").strip().upper()
        neighbour_codes = [c.strip() for c in codes.split(',') if c.strip()]
        try:
            print_countries(find_by_neighbours(neighbour_codes))
        except CountryError as e:
            print(f"Error: {e}")
    elif choice == "5":
        field = input("Field ('population' or 'area'): ").strip().lower()
        n_str = input("How many top results? ").strip()
        try:
            n = int(n_str)
            print_countries(top_n(field, n))
        except ValueError:
            print("Error: N must be an integer.")
        except CountryError as e:
            print(f"Error: {e}")
    elif choice == "6":
        codes = input("ISO codes to enrich (comma separated): ").strip().upper()
        iso_codes = [c.strip() for c in codes.split(',') if c.strip()]
        if not iso_codes:
            print("No codes entered.")
            return True
        print("Enriching country data asynchronously…")
        enriched = await enrich_countries(iso_codes)
        if enriched:
            print(f"Enriched countries: {', '.join(enriched)}")
        else:
            print("No matching countries were enriched.")
        print("Enrichment completed.")
    elif choice == "7":
        if not QUERY_LOG:
            print("Query log is empty.")
        else:
            print("--- Query Log ---")
            for entry in QUERY_LOG:
                print(f"{entry['function']} args={entry['args']} kwargs={entry['kwargs']}")
    elif choice == "8":
        return False
    else:
        print("Invalid choice, please select 1‑8.")
    return True


async def main() -> None:
    running = True
    try:
        while running:
            display_menu()
            choice = input("Select an option: ").strip()
            running = await handle_choice(choice)
    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram interrupted. Goodbye!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, EOFError):
        pass


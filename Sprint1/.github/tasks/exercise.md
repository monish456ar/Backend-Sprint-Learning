# Sprint 1 Review — Country Data CLI Tool

Build a small **Country Data CLI Tool** in Python.

This is the final exercise for Sprint 1 and should combine the concepts covered during Days 1–8. Keep the project simple and focused on practicing what has already been learned.

## Project Structure

Use multiple Python modules:

```text
country_cli/
├── models.py
├── data.py
├── queries.py
├── decorators.py
├── exceptions.py
├── enrichment.py
└── main.py
```

Each module should have a clear responsibility.

## 1. Country Model

Create a typed `Country` model containing:

* name
* ISO code
* population
* area in km²
* continent
* spoken languages
* currency
* neighbour ISO codes

Use a dataclass and appropriate Python type hints.

## 2. Country Data

Create a small in-memory dataset of countries.

The data should be enough to demonstrate:

* different continents
* different populations
* different areas
* neighbouring countries
* multiple languages/currencies

No database or external API is required.

## 3. Query Functions

Create functions to:

### Filter by continent

Return countries belonging to a given continent.

### Sort

Sort countries by:

* population
* area

Support ascending/descending order.

### Find by neighbours

Given neighbour ISO codes, find matching countries.

### Top-N

Return the top N countries by:

* population
* area

All query functions should use type hints.

## 4. Custom Exceptions

Create a few custom exceptions for invalid input, such as:

* unknown country code
* unsupported sort field
* invalid query parameter

Catch these exceptions in the CLI and display a clean error message instead of a traceback.

Example:

```text
Error: Unknown country code 'XYZ'.
```

## 5. Query Logging Decorator

Create a decorator that logs every call to the query functions.

The log should contain:

* function name
* arguments passed to the function

Store the logs in an in-memory list.

Example:

```text
filter_by_continent("Asia")
sort_countries("population", "desc")
top_n("population", 3)
```

Use the decorator concepts learned on Day 7, including `functools.wraps` where appropriate.

## 6. Async Country Enrichment

Create an async enrichment function.

It should:

* receive a list of country ISO codes
* simulate a remote lookup using `asyncio.sleep()`
* use different delays for different countries
* run the lookups concurrently
* update the in-memory country data with the returned information

Use the Day 8 concepts:

* `async def`
* `await`
* `asyncio.sleep()`
* `asyncio.create_task()`
* `asyncio.gather()`

The remote lookup is only simulated. No real API is needed.

Example output:

```text
Enriching country data...

[IN] Remote lookup completed
[JP] Remote lookup completed
[US] Remote lookup completed

Enrichment completed.
```

## 7. CLI

`main.py` should provide a simple menu:

```text
=============================
       COUNTRY DATA CLI
=============================

1. List countries
2. Filter by continent
3. Sort countries
4. Find by neighbours
5. Top-N countries
6. Enrich country data
7. Show query log
8. Exit
```

The exact menu/output can be implemented in a simple way.

## 8. Concepts Being Practiced

The project should naturally use concepts from the previous days:

**Day 1**

* functions
* conditions
* input/output
* `if __name__ == "__main__"`

**Day 2**

* lists
* dictionaries
* sets/tuples where useful
* comprehensions
* sorting

**Day 3**

* type hints
* typed functions
* working with structured data

**Day 4**

* classes
* dataclasses
* methods

**Day 5**

* modules
* packages
* custom exceptions
* `raise`
* `try/except`

**Day 6**

* type annotations
* the typing concepts already learned where they naturally fit

**Day 7**

* decorators
* `*args` / `**kwargs`
* `functools.wraps`

**Day 8**

* `async def`
* `await`
* `asyncio.run()`
* `asyncio.sleep()`
* `asyncio.create_task()`
* `asyncio.gather()`
* event-loop concurrency

Do not force a concept into the project just for the sake of using it.

## Goal

Complete one small application that brings together the Python concepts learned during Sprint 1.

The implementation should be:

* simple
* readable
* typed
* modular
* easy to understand

Build it **step by step**, starting with `models.py`, rather than creating the entire project at once.

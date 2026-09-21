# Day 5: Custom Exceptions, Context Managers & Modular Architecture

A simple guide to organizing Python code into modular packages, building custom domain exceptions, and using context managers (`with` statements).

---

## 📌 Core Concepts Covered

| Concept | Description | Quick Example |
| :--- | :--- | :--- |
| **Custom Exceptions** | Domain-specific exception hierarchy inheriting from `Exception`. | `class ResourceNotFoundError(LibraryException):` |
| **`try / except / else / finally`** | Robust error handling with cleanup guarantees. | `try: ... except ValueError: ... finally: ...` |
| **Context Managers** | Resource management using `__enter__` and `__exit__`. | `class CatalogueSession: def __enter__(self):` |
| **Package Structure** | Organizing code across modules with `__init__.py` exports. | `from library import Book, CatalogueSession` |

---

## 📂 Architecture & Exercises

### 📁 Package: [`library/`](./library/)

```
library/
├── __init__.py       # Exposes clean public API package interface
├── models.py         # Book, Member, PremiumMember, Loan definitions
├── exceptions.py     # LibraryException, ResourceNotFoundError, InvalidInputError
├── session.py        # CatalogueSession context manager
└── catalogue.py      # Core catalogue operations & domain business logic
```

- **[`library/exceptions.py`](./library/exceptions.py)**:
  - `LibraryException`: Base class for domain errors.
  - `ResourceNotFoundError`: Raised when a book, author, or loan is not found.
  - `InvalidInputError`: Raised on invalid fine rates or input arguments.
- **[`library/session.py`](./library/session.py)**:
  - `CatalogueSession`: Custom context manager providing setup, timestamping, logging, and cleanup handling on exit.
- **[`library/catalogue.py`](./library/catalogue.py)**:
  - Raises domain-specific exceptions on error states (e.g. negative fine rates, missing ISBNs) rather than returning generic errors or failing silently.

---

### 1. [`main.py`](./main.py) — CLI Application with Session & Error Handling
Runs complete catalogue workflows wrapped in a `CatalogueSession` context manager and demonstrates catching domain exceptions cleanly without exposing tracebacks.

---

### 2. [`pratice.py`](./pratice.py) — Exception Practice
Examples covering:
- Custom `InvalidAgeError` exception definition and raising.
- Full `try...except...else...finally` control flow.

---

## 🚀 How to Run

```bash
# Run Modular Library Application
python main.py

# Run Exception Practice
python pratice.py
```

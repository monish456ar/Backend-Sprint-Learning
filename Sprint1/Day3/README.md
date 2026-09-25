# Day 3: Functions, Type Annotations & Callbacks

A simple and structured guide to modern Python type hinting, function signatures, union types, and higher-order callback functions.

---

## 📌 Core Concepts Covered

| Concept | Description | Quick Example |
| :--- | :--- | :--- |
| **Type Annotations** | Explicit parameter and return type declarations. | `def add(a: int, b: int) -> int:` |
| **Optional / Union Types** | Handling values that can be multiple types or `None`. | `def find_book(isbn: str) -> dict \| None:` |
| **`Callable` Callbacks** | Passing functions as arguments with explicit signature hints. | `callback: Callable[[dict], str]` |
| **Type Narrowing** | Refining types at runtime using `isinstance()`. | `if isinstance(val, str): ...` |
| **Keyword-Only Args** | Enforcing named parameters after `*`. | `def create_user(name, *, age):` |
| **Date Arithmetic** | Working with `datetime.date` and overdue differences. | `(ref_date - loan_due).days` |

---

## 📂 Files & Exercises

### 1. [`main.py`](./main.py) — Library Catalogue Operations
Implements typed operations over library books and member loan records:
- **`find_book(isbn)`**: Finds a book or returns `None` (`dict | None`).
- **`find_books_by_author(author)`**: Returns a filtered list of books (`list[dict]`).
- **`has_overdue_loan(member_id, ref_date)`**: Checks overdue loan status against a target date.
- **`calculate_fine(loan, ref_date, per_day_rate)`**: Calculates fine based on elapsed overdue days.
- **`transform_books(books, callback)`**: Higher-order function applying a `Callable` transformation.
- **`sort_books(books)`**: Sorts books alphabetically by title.

---

### 2. [`pratice/pratice.py`](./pratice/pratice.py) — Type Annotation Practice
Interactive examples exploring:
- Parameter and return type hints.
- `None` returns and `T | None` lookups.
- Modern Union syntax (`int | str`).
- Custom higher-order calculation functions using `Callable[[int, int], int]`.
- Type narrowing with `isinstance`.
- Explicit annotations vs. type inference.
- Keyword-only arguments (`*`).

---

## 🚀 How to Run

```bash
# Run Library Catalogue
python main.py

# Run Typing Practice
python pratice/pratice.py
```

# Day 2: Data Structures & Collections

A simple guide to Python's core data structures, comprehensions, and data transformation techniques using a book catalog dataset.

---

## 📌 Core Concepts Covered

| Concept | Description | Quick Example |
| :--- | :--- | :--- |
| **List & Dict Comprehensions** | Compact syntax for filtering and transforming collections. | `[book for book in books if book["genre"] == "Sci-Fi"]` |
| **Set & Uniqueness** | Fast duplicate removal and unique value extraction. | `genres = {book["genre"] for book in books}` |
| **`enumerate()` & `zip()`** | Indexed iteration and parallel collection processing. | `for name, role in zip(names, roles):` |
| **`sorted()` & `max()`** | Sorting and finding extrema with custom lambda key functions. | `max(books, key=lambda b: b["year"])` |
| **Shallow vs. Deep Copy** | Copying data structures safely without unintended mutation. | `copy.deepcopy(user_dict)` |
| **`collections.Counter`** | Frequency counting for frequency analysis and repeats. | `Counter(book["author"] for book in books)` |

---

## 📂 Files & Exercises

### 1. [`main.py`](./main.py) — Book Dataset Analysis
Practical data manipulation on a list of book records:
- **Genre Extraction**: Finds all unique genres using set comprehensions.
- **Genre Report**: Computes total titles, average price, and newest book per genre.
- **Deduplication**: Identifies and strips duplicate books based on `(title, author)` tuples while tracking removed items.
- **Author Index**: Groups book titles under each author name in a dictionary.
- **Repeat Author Detection**: Uses `collections.Counter` to find authors with multiple publications.

---

### 2. [`pratice.py`](./pratice.py) — Collections Practice
Hands-on examples demonstrating:
- List, tuple, set, and dictionary operations.
- `enumerate` and `zip` loops.
- `sorted()` sorting algorithms.
- `copy.copy()` vs `copy.deepcopy()` behavior with nested lists.
- Filtering with `filter()` and `lambda`.

---

## 🚀 How to Run

```bash
# Run Book Analysis
python main.py

# Run Collections Practice
python pratice.py
```

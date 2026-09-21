# Day 4: Object-Oriented Programming (OOP) & Dataclasses

A simple guide to OOP principles in Python, including class models, inheritance, property decorators, static methods, and modern `@dataclass`.

---

## 📌 Core Concepts Covered

| Concept | Description | Quick Example |
| :--- | :--- | :--- |
| **Classes & `__init__`** | Blueprint definitions with typed constructor attributes. | `class Book: def __init__(self, ...):` |
| **String Representation** | Human-readable output using `__str__()`. | `def __str__(self) -> str:` |
| **Inheritance & `super()`** | Extending base classes with specialized behaviors. | `class PremiumMember(Member):` |
| **`@property` Decorator** | Computed attributes accessed without parentheses. | `@property def is_overdue(self) -> bool:` |
| **`@staticmethod`** | Utility functions bound to a class without `self`. | `@staticmethod def calculate_avg(a, b):` |
| **`@dataclass`** | Auto-generates `__init__`, `__repr__`, and `__eq__`. | `@dataclass class Loan:` |

---

## 📂 Files & Exercises

### 1. [`main.py`](./main.py) — OOP Library System
Refactors the library system from raw dictionaries into structured class models:
- **`Book`**: Represents books with ISBN, title, and author.
- **`Member` & `PremiumMember`**: Base member (14-day loan period) and subclass (28-day loan period) computing due dates dynamically.
- **`Loan` (`@dataclass`)**: Tracks member, book, loan date, due date, and dynamic `@property` `.is_overdue`.
- **Catalogue Operations**: Search, fine calculation, loan tracking, and callback transformations operating directly on strongly typed domain objects.

---

### 2. [`pratice.py`](./pratice.py) — OOP & Dataclass Practice
Practical snippets demonstrating:
- Property getters and class attributes.
- Static methods on classes.
- Subclassing with `super().__init__()`.
- `@dataclass` equality comparison (`emp1 == emp2`).

---

## 🚀 How to Run

```bash
# Run OOP Library System
python main.py

# Run OOP Practice
python pratice.py
```

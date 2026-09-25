# Day 7: Decorators & Higher-Order Functions

A practical guide to Python decorators — from first-class functions and closures to advanced decorator patterns used in real-world backends.

---

## 📌 Core Concepts Covered

| Concept | Description | Quick Example |
| :--- | :--- | :--- |
| **First-Class Functions** | Functions are objects — they can be assigned, passed, and returned. | `user1 = greet` |
| **Closures** | Inner functions that remember the enclosing scope's variables. | `def outer(): count = 0; def inner(): nonlocal count` |
| **Basic Decorator** | A function that wraps another to add behaviour before/after it. | `def require_admin(fun): def wrapper(): ...` |
| **Decorator with Arguments** | Three-level nesting to pass arguments to decorators. | `def invite(msg): def decorator(fun): def wrapper():` |
| **`functools.wraps`** | Preserves the original function's `__name__` and metadata. | `@wraps(fun)` |
| **Class-Based Decorator** | Using a class with `__call__` as a decorator. | `class User: def __call__(self, *args): ...` |
| **Stacked Decorators** | Applying multiple decorators to a single function. | `@timer @cache @type_check def multiply():` |
| **Timing Decorator** | Measures and prints function execution time. | `def timer(func):` |
| **Retry Decorator** | Retries a failing function N times with a delay. | `def retry(attempts, delay):` |
| **Caching Decorator** | Caches the result for a given duration to avoid re-computation. | `def cache(duration):` |
| **Type Checking Decorator** | Validates argument types at runtime using annotations. | `def type_check(func):` |

---

## 📂 Files & Exercises

### 1. [`model.py`](./model.py) — Generic Pipeline (Carried from Day 6)
Reusable generic pipeline utilities imported and used in `main.py`:
- **`Pipeline[T]`**: `.filter()`, `.transform()`, `.group_by()`
- **`RecordValidator[T]`**: Protocol-based validator contract
- **`validate_records()`**: Validates a list using any conforming validator
- **`PipelineConfig`**: TypedDict for pipeline settings

---

### 2. [`main.py`](./main.py) — Decorator Showcase
Combines Day 6 pipeline usage with Day 7 decorator implementations:

#### Day 6 Recap (top section)
- Validates and filters `User` objects via the generic `Pipeline[T]`
- Groups users by `department` and `age`

#### Day 7 Decorators (bottom section)

| # | Decorator | What it Does |
| :- | :--- | :--- |
| 1 | **`@timer`** | Prints the start time, end time, and total elapsed time of a function. |
| 2 | **`@retry(attempts, delay)`** | Retries a function up to N times with a sleep delay between each attempt; raises on final failure. |
| 3 | **`@cache(duration)`** | Returns a cached result if the function was called within the last `duration` seconds. |
| 4 | **`@type_check`** | Reads `__annotations__` at runtime and raises `TypeError` if any argument type mismatches. |
| 5 | **Stacked** | `@timer @cache(duration=10) @type_check` all applied to `multiply()` — executed inside-out. |

---

### 3. [`pratice.py`](./pratice.py) — Decorator Fundamentals Practice
Step-by-step exploration of every building block:

| Section | Concept Practised |
| :--- | :--- |
| **First-Class Functions** | Assigning a function to a variable; passing a function as an argument. |
| **Closures** | `outer()` / `inner()` counter using `nonlocal`. |
| **Basic Decorator** | `@require_admin` — guards a function behind a role check. |
| **Decorator with Arguments** | `@invite("hello")` — three-level nesting pattern. |
| **Without `@wraps`** | Shows `login.__name__` becomes `"wrapper"`. |
| **With `@wraps`** | Shows `login1.__name__` is correctly preserved as `"login1"`. |
| **Class-Based Decorator** | `class User` with `__call__` used as a decorator. |
| **Multiple Decorators** | `@first @second` stacked on `hello()` — demonstrates execution order. |

---

## 🔑 Key Takeaways

- **Decorator execution order** when stacking is **bottom-up** (innermost applied first).
- **`@wraps(func)`** from `functools` must always be used inside decorators to preserve `__name__`, `__doc__`, and other metadata — critical for debugging and introspection.
- **Closures** are the backbone of decorators; understanding `nonlocal` is essential.
- **Class-based decorators** are useful when the decorator needs to maintain state across calls.
- The **`retry`** and **`cache`** patterns are extremely common in production backend code (API clients, DB queries, expensive computations).

---

## 🚀 How to Run

```bash
# Run the main decorator showcase
python main.py

# Run the decorator fundamentals practice
python pratice.py
```

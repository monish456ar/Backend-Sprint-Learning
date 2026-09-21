# Day 6: Advanced Typing & Generic Data Pipeline

A simple and practical guide to advanced Python typing concepts and building a reusable, generic data processing pipeline.

---

## 📌 Core Concepts Covered

| Concept | Description | Quick Example |
| :--- | :--- | :--- |
| **`TypeVar` & `Generic`** | Creates reusable, type-safe classes and functions for any data type. | `class Pipeline(Generic[T]):` |
| **`Protocol`** | Defines interfaces (structural subtyping / duck typing). | `class RecordValidator(Protocol[T]):` |
| **`TypedDict`** | Provides type definitions for dictionary keys and value types. | `class PipelineConfig(TypedDict):` |
| **`Callable`** | Type hints for functions and lambda expressions. | `condition: Callable[[T], bool]` |
| **`Literal`** | Restricts values to a specific set of predefined options. | `Literal["todo", "inprogress", "complete"]` |
| **`Final`** | Declares constant variables that should not be reassigned. | `MAX_ITEMS: Final[int] = 1000` |
| **`Annotated`** | Attaches custom metadata or documentation to a type hint. | `Annotated[int, "must be positive"]` |
| **`@overload`** | Defines multiple type signatures for a single function. | `@overload def get(val: int) -> int:` |

---

## 📂 Files & Exercises

### 1. [`model.py`](./model.py) — Generic Pipeline & Models
Defines the core reusable logic:
- **`Pipeline[T]`**: Generic class supporting:
  - `.filter()` — Filters items using a boolean condition.
  - `.transform()` — Transforms items from type `T` to type `U`.
  - `.group_by()` — Groups items into a dictionary by a key function.
- **`RecordValidator[T]`**: Protocol defining a `.validate(item: T) -> bool` contract.
- **`validate_records()`**: Validates a list of items using any validator conforming to the protocol.
- **`PipelineConfig`**: TypedDict for pipeline settings (`name`, `enabled`, `batch_size`).

---

### 2. [`main.py`](./main.py) — User Data Pipeline Exercise
Demonstrates the generic pipeline using `User` objects:
1. **Validation**: Validates user records with `UserValidator`.
2. **Filtering**: Filters users with `age >= 25`.
3. **Transformation**: Extracts a list of user names (`transform`).
4. **Grouping**: Groups users by `department` and by `age`.
5. **Configuration**: Configures pipeline execution using `PipelineConfig`.

---

### 3. [`book.py`](./book.py) — Book Catalog Exercise
Demonstrates reusability of `Pipeline[T]` on a different data model (`Book`):
- **Filter**: Finds books with more than 200 pages (`pages > 200`).
- **Transform**: Extracts only book titles.
- **Group By**: Groups books by their `category` (e.g., Programming, Education).

---

### 4. [`pratice.py`](./pratice.py) — Type System Practice
Explores standalone typing features with quick examples:
- Generic functions (`check_type`) and generic class (`Box[T]`).
- Protocol implementations (`Profile` interface).
- TypedDict with `Literal` status constraints.
- `Final` constants and `Annotated` types.
- Function overloading with `@overload`.

---

## 🚀 How to Run

```bash
# Run User Pipeline
python main.py

# Run Book Catalog Pipeline
python book.py

# Run Typing Practice Examples
python pratice.py
```

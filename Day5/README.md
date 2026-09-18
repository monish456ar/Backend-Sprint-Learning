# Day 5: Library Catalogue — Part 3 (Package Structure & Error Handling)

## Overview

In Day 5, we refactored the monolithic Day 4 library script into a modular, production-ready Python package with robust custom domain exceptions, strict validation, and context manager session lifecycle management.

---

## 📁 Package Architecture

```text
Day5/
│
├── library/                       # Domain package
│   ├── __init__.py                # Package root exposing public API
│   ├── exceptions.py              # Custom domain exception hierarchy
│   ├── models.py                  # Domain models (Book, Member, PremiumMember, Loan)
│   ├── catalogue.py               # Business logic and catalogue operations
│   └── session.py                 # CatalogueSession context manager
│
├── main.py                        # CLI entry point with top-level error handling
├── pratice.py                     # Scratch / quick practice script
└── README.md                      # Documentation
```

---

## 🚨 Custom Exception Hierarchy

Every custom exception inherits from `LibraryException` and carries typed attributes describing the exact problem:

```
Exception
 └── LibraryException
      ├── ResourceNotFoundError (resource_type: str, resource_id: str)
      ├── BusinessRuleViolationError (rule: str, details: str)
      └── InvalidInputError (field: str, value: Any, reason: str)
```

### Exception Usages:

1. **`ResourceNotFoundError`**:
   - Raised when querying for a book ISBN or member ID that does not exist.
   - Raised when searching for books by an author that returns no matches.
2. **`BusinessRuleViolationError`**:
   - Raised when attempting to borrow a book that is already checked out.
   - Raised when a member has active overdue loans and is blocked from borrowing.
   - Raised when a member exceeds their concurrent active loan limit (`Member`: 2, `PremiumMember`: 5).
   - Raised when attempting to return a book that is not currently recorded on active loan.
3. **`InvalidInputError`**:
   - Raised when instantiating `Book` or `Member` with empty/whitespace strings.
   - Raised when calculating fines with negative rates or invalid dates.

---

## 🔄 Context Manager (`CatalogueSession`)

The `CatalogueSession` context manager encapsulates the library session lifecycle:
- **`__enter__`**: Records startup timestamp, seeds initial inventory/members, and logs session startup.
- **`__exit__`**: Guarantees teardown execution, computes session elapsed time, tallies active loans, and logs whether the session completed normally or encountered an exception.

```python
with CatalogueSession("Daily Operations") as catalogue:
    book = catalogue.find_book("101")
    catalogue.borrow_book(member_id="M001", isbn="101")
```

---

## 🚀 Running the Application

From the project root:

```bash
python Day5/main.py
```

from collections.abc import Callable
from datetime import date


# Library books stored as hardcoded data
books = [
    {"isbn": "101", "title": "Python Basics", "author": "John"},
    {"isbn": "102", "title": "Clean Code", "author": "Robert"},
    {"isbn": "103", "title": "Python Advanced", "author": "John"},
    {"isbn": "104", "title": "JavaScript Guide", "author": "David"},
    {"isbn": "105", "title": "Learning Python", "author": "John"},
]

# Member loans with due dates and return status
loans = [
    {"member_id": "M001", "isbn": "101", "due_date": date(2026, 9, 5), "returned": False},
    {"member_id": "M002", "isbn": "102", "due_date": date(2026, 9, 20), "returned": False},
    {"member_id": "M003", "isbn": "103", "due_date": date(2026, 9, 1), "returned": True},
    {"member_id": "M001", "isbn": "104", "due_date": date(2026, 9, 8), "returned": False},
    {"member_id": "M004", "isbn": "105", "due_date": date(2026, 9, 25), "returned": False},
]


# Find one book using its ISBN
def find_book(isbn: str) -> dict | None:
    for book in books:
        if book["isbn"] == isbn:
            return book
    return None


# Find all books written by a specific author
def find_books_by_author(author: str) -> list[dict]:
    result = []

    for book in books:
        if book["author"] == author:
            result.append(book)

    return result


# Check whether a member currently has an overdue loan
def has_overdue_loan(member_id: str, reference_date: date) -> str:
    for loan in loans:
        if (
            loan["member_id"] == member_id
            and not loan["returned"]
            and loan["due_date"] < reference_date
        ):
            return "True"

    return "False"


# Calculate the fine for a loan based on overdue days
def calculate_fine(
    loan: dict,
    reference_date: date,
    per_day_rate: float,
) -> float:
    overdue_days = (reference_date - loan["due_date"]).days
    return overdue_days * per_day_rate


# Apply a callback function to every book
def transform_books(
    book_list: list[dict],
    callback: Callable[[dict], str],
) -> list[str]:
    result = []

    for book in book_list:
        result.append(callback(book))

    return result


# Callback that gets the title from a book
def get_title(book: dict) -> str:
    return book["title"]


# Sort books alphabetically by title
def sort_books(book_list: list[dict]) -> list[dict]:
    return sorted(book_list, key=lambda book: book["title"])


# Run and demonstrate all library operations
def main() -> None:
    reference_date = date(2026, 9, 10)

    print("\n===== LIBRARY CATALOGUE =====")

    # Operation 1: Look up a book
    print("\n--- Book Lookup ---")
    book = find_book("101")

    if book is not None:
        print(f"Book found: {book['title']}")
    else:
        print("Book not found")

    # Operation 2: Find books by author
    print("\n--- Books by John ---")
    john_books = find_books_by_author("John")

    for book in john_books:
        print(book)

    # Operation 3: Check overdue loans
    print("\n--- Overdue Loan ---")
    print(has_overdue_loan("M001", reference_date))

    # Operation 4: Calculate loan fine
    print("\n--- Fine ---")
    fine = calculate_fine(loans[3], reference_date, 2.0)
    print(f"Fine: ₹{fine}")

    # Operation 5: Transform books using a callback
    print("\n--- Callback Result ---")
    titles = transform_books(books, get_title)

    for title in titles:
        print(title)

    # Operation 6: Sort books by title
    print("\n--- Sorted Books ---")
    sorted_books = sort_books(books)

    for book in sorted_books:
        print(book["title"])


if __name__ == "__main__":
    main()
"""Business logic and catalogue operations carried forward from Day 4."""

from collections.abc import Callable
from datetime import date

from .exceptions import (
    InvalidInputError,
    ResourceNotFoundError,
)
from .models import Book, Loan, Member, PremiumMember

# Seed Data (carried forward from Day 4)
books: list[Book] = [
    Book("101", "Python Basics", "John"),
    Book("102", "Clean Code", "Robert"),
    Book("103", "Python Advanced", "John"),
    Book("104", "JavaScript Guide", "David"),
    Book("105", "Learning Python", "John"),
]

members: list[Member] = [
    Member("M001", "Monish"),
    Member("M002", "Rahul"),
    PremiumMember("M003", "Arun"),
    Member("M004", "David"),
]

loans: list[Loan] = [
    Loan(
        member=members[0],
        book=books[0],
        loan_date=date(2026, 8, 25),
        due_date=date(2026, 9, 5),
    ),
    Loan(
        member=members[1],
        book=books[1],
        loan_date=date(2026, 9, 6),
        due_date=date(2026, 9, 20),
    ),
    Loan(
        member=members[2],
        book=books[2],
        loan_date=date(2026, 8, 4),
        due_date=date(2026, 9, 1),
        return_date=date(2026, 9, 3),
    ),
    Loan(
        member=members[0],
        book=books[3],
        loan_date=date(2026, 8, 25),
        due_date=date(2026, 9, 8),
    ),
    Loan(
        member=members[3],
        book=books[4],
        loan_date=date(2026, 9, 11),
        due_date=date(2026, 9, 25),
    ),
]


def find_book(isbn: str) -> Book:
    """Find a book using its ISBN. Raises ResourceNotFoundError if missing."""
    if not isbn or not str(isbn).strip():
        raise InvalidInputError("isbn", isbn, "ISBN cannot be empty")

    for book in books:
        if book.isbn == isbn.strip():
            return book

    raise ResourceNotFoundError("book", isbn)


def find_member(member_id: str) -> Member:
    """Find a member using their Member ID. Raises ResourceNotFoundError if missing."""
    if not member_id or not str(member_id).strip():
        raise InvalidInputError("member_id", member_id, "Member ID cannot be empty")

    for member in members:
        if member.member_id == member_id.strip():
            return member

    raise ResourceNotFoundError("member", member_id)


def find_books_by_author(author: str) -> list[Book]:
    """Find all books written by a specific author. Raises ResourceNotFoundError if none."""
    if not author or not str(author).strip():
        raise InvalidInputError("author", author, "Author name cannot be empty")

    result = [book for book in books if book.author.lower() == author.strip().lower()]
    if not result:
        raise ResourceNotFoundError("books for author", author)

    return result


def has_overdue_loan(member: Member, reference_date: date) -> bool:
    """Check whether a member has an overdue active loan."""
    for loan in loans:
        if (
            loan.member == member
            and loan.return_date is None
            and loan.due_date < reference_date
        ):
            return True

    return False


def calculate_fine(
    loan: Loan,
    reference_date: date,
    per_day_rate: float,
) -> float:
    """Calculate the fine for an overdue loan. Raises InvalidInputError if rate is negative."""
    if per_day_rate < 0:
        raise InvalidInputError("per_day_rate", per_day_rate, "Fine rate cannot be negative")

    if loan.return_date is not None:
        return 0.0

    overdue_days = (reference_date - loan.due_date).days
    if overdue_days <= 0:
        return 0.0

    return overdue_days * per_day_rate


def transform_books(
    book_list: list[Book],
    callback: Callable[[Book], str],
) -> list[str]:
    """Apply a callback function to every book."""
    result = []
    for book in book_list:
        result.append(callback(book))
    return result


def get_title(book: Book) -> str:
    """Return the title of a book."""
    return book.title


def sort_books(book_list: list[Book]) -> list[Book]:
    """Return books sorted alphabetically by title."""
    return sorted(book_list, key=lambda book: book.title)

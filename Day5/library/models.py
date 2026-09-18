"""Domain models carried forward from Day 4."""

from dataclasses import dataclass
from datetime import date, timedelta

from .exceptions import InvalidInputError


class Book:
    """Represent a book in the library."""

    def __init__(self, isbn: str, title: str, author: str) -> None:
        if not isbn or not str(isbn).strip():
            raise InvalidInputError("isbn", isbn, "ISBN cannot be empty")
        if not title or not str(title).strip():
            raise InvalidInputError("title", title, "Title cannot be empty")
        if not author or not str(author).strip():
            raise InvalidInputError("author", author, "Author cannot be empty")

        self.isbn = isbn.strip()
        self.title = title.strip()
        self.author = author.strip()

    def __str__(self) -> str:
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"


class Member:
    """Represent a library member."""

    loan_period: int = 14
    max_loans: int = 2

    def __init__(self, member_id: str, name: str) -> None:
        if not member_id or not str(member_id).strip():
            raise InvalidInputError("member_id", member_id, "Member ID cannot be empty")
        if not name or not str(name).strip():
            raise InvalidInputError("name", name, "Name cannot be empty")

        self.member_id = member_id.strip()
        self.name = name.strip()

    def get_due_date(self, loan_date: date) -> date:
        """Return the due date based on the member's loan period."""
        return loan_date + timedelta(days=self.loan_period)

    def __str__(self) -> str:
        return f"{self.name} (Member ID: {self.member_id})"


class PremiumMember(Member):
    """Represent a premium member with a longer loan period."""

    loan_period: int = 28
    max_loans: int = 5

    def __init__(self, member_id: str, name: str) -> None:
        super().__init__(member_id, name)

    def __str__(self) -> str:
        return f"{self.name} (Premium Member ID: {self.member_id})"


@dataclass
class Loan:
    """Represent a book loan between a member and a book."""

    member: Member
    book: Book
    loan_date: date
    due_date: date
    return_date: date | None = None

    @property
    def is_overdue(self) -> bool:
        """Return True if the loan is active and past its due date."""
        if self.return_date is not None:
            return False
        return self.due_date < date.today()

    def __str__(self) -> str:
        status = "Returned" if self.return_date is not None else "Active"
        return (
            f"{self.book.title} -> {self.member.name} "
            f"(Due: {self.due_date}, Status: {status})"
        )


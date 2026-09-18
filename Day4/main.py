from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, timedelta


class Book:
    """Represent a book in the library."""

    def __init__(self, isbn: str, title: str, author: str) -> None:
        self.isbn = isbn
        self.title = title
        self.author = author

    def __str__(self) -> str:
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"


class Member:
    """Represent a library member."""

    loan_period: int = 14

    def __init__(self, member_id: str, name: str) -> None:
        self.member_id = member_id
        self.name = name

    def get_due_date(self, loan_date: date) -> date:
        """Return the due date based on the member's loan period."""
        return loan_date + timedelta(days=self.loan_period)

    def __str__(self) -> str:
        return f"{self.name} (Member ID: {self.member_id})"


class PremiumMember(Member):
    """Represent a premium member with a longer loan period."""

    loan_period: int = 28

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


# Books
books :list[Book] = [
    Book("101", "Python Basics", "John"),
    Book("102", "Clean Code", "Robert"),
    Book("103", "Python Advanced", "John"),
    Book("104", "JavaScript Guide", "David"),
    Book("105", "Learning Python", "John"),
]


# Members
members :list[Member] = [
    Member("M001", "Monish"),
    Member("M002", "Rahul"),
    PremiumMember("M003", "Arun"),
    Member("M004", "David"),
]


# Loans
loans : list[Loan] = [
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


def find_book(isbn: str) -> Book | None:
    """Find a book using its ISBN."""
    for book in books:
        if book.isbn == isbn:
            return book

    return None


def find_books_by_author(author: str) -> list[Book]:
    """Find all books written by a specific author."""
    result = []

    for book in books:
        if book.author == author:
            result.append(book)

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
    """Calculate the fine for an overdue loan."""
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


def main() -> None:
    """Run and demonstrate all library operations."""
    reference_date = date(2026, 9, 10)

    print("\n===== LIBRARY CATALOGUE =====")

    print("\n--- Book Lookup ---")
    book = find_book("101")

    if book is not None:
        print(f"Book found: {book}")
    else:
        print("Book not found")

    print("\n--- Books by John ---")
    john_books = find_books_by_author("John")

    for book in john_books:
        print(book)

    print("\n--- Overdue Loan ---")
    member = members[0]
    overdue = has_overdue_loan(member, reference_date)
    print(f"{member}: {overdue}")

    print("\n--- Fine ---")
    fine = calculate_fine(loans[3], reference_date, 2.0)
    print(f"Fine: ₹{fine}")

    print("\n--- Member Types ---")
    for member in members:
        print(member)

    print("\n--- Due Dates ---")
    loan_date = date(2026, 9, 16)

    for member in members[:3]:
        due_date = member.get_due_date(loan_date)
        print(f"{member.name}: {due_date}")

    print("\n--- Callback Result ---")
    titles = transform_books(books, get_title)

    for title in titles:
        print(title)

    print("\n--- Sorted Books ---")
    sorted_book_list = sort_books(books)

    for book in sorted_book_list:
        print(book.title)

    print("\n--- Loans ---")
    for loan in loans:
        print(loan)

    print("\n--- Overdue Status ---")
    for loan in loans:
        print(f"{loan.book.title}: {loan.is_overdue}")


if __name__ == "__main__":
    main()
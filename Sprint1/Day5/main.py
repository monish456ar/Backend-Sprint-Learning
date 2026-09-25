"""Day 5 CLI Entry point: Library Catalogue with Exceptions & Package Structure."""

from datetime import date

from library import (
    Book,
    CatalogueSession,
    InvalidInputError,
    LibraryException,
    PremiumMember,
    ResourceNotFoundError,
    books,
    calculate_fine,
    find_book,
    find_books_by_author,
    get_title,
    has_overdue_loan,
    loans,
    members,
    sort_books,
    transform_books,
)


def main() -> None:
    """Run and demonstrate Day 5 library operations inside a session with error handling."""
    reference_date = date(2026, 9, 10)

    # Wrap operations inside the CatalogueSession context manager
    with CatalogueSession("Library Session"):
        print("\n===== LIBRARY CATALOGUE (DAY 5) =====")

        # 1. Book Lookup
        print("\n--- Book Lookup ---")
        try:
            book = find_book("101")
            print(f"Book found: {book}")
        except ResourceNotFoundError as e:
            print(f"Error: {e.message}")

        # 2. Books by Author
        print("\n--- Books by John ---")
        try:
            john_books = find_books_by_author("John")
            for book in john_books:
                print(book)
        except ResourceNotFoundError as e:
            print(f"Error: {e.message}")

        # 3. Overdue Loan Check
        print("\n--- Overdue Loan ---")
        member = members[0]
        overdue = has_overdue_loan(member, reference_date)
        print(f"{member}: {overdue}")

        # 4. Fine Calculation
        print("\n--- Fine ---")
        try:
            fine = calculate_fine(loans[3], reference_date, 2.0)
            print(f"Fine: Rs. {fine}")
        except InvalidInputError as e:
            print(f"Invalid input error: {e.message}")

        # 5. Member Types
        print("\n--- Member Types ---")
        for m in members:
            print(m)

        # 6. Due Dates
        print("\n--- Due Dates ---")
        loan_date = date(2026, 9, 16)
        for m in members[:3]:
            due_date = m.get_due_date(loan_date)
            print(f"{m.name}: {due_date}")

        # 7. Callback Result
        print("\n--- Callback Result ---")
        titles = transform_books(books, get_title)
        for title in titles:
            print(title)

        # 8. Sorted Books
        print("\n--- Sorted Books ---")
        sorted_book_list = sort_books(books)
        for b in sorted_book_list:
            print(b.title)

        # 9. Loans
        print("\n--- Loans ---")
        for loan in loans:
            print(loan)

        # 10. Overdue Status
        print("\n--- Overdue Status ---")
        for loan in loans:
            print(f"{loan.book.title}: {loan.is_overdue}")

        # 11. Custom Exception Handling Demonstrations (No traceback exposed)
        print("\n--- Error Handling Demonstrations ---")

        # 11a. ResourceNotFoundError (Missing Book)
        print("\n[Testing Missing Book Lookup]")
        try:
            find_book("999")
        except ResourceNotFoundError as e:
            print(f" {e}")
            # print(f"Caught Error -> {e.message} (Type: {e.resource_type}, ID: {e.resource_id})")

        # 11b. InvalidInputError (Invalid fine rate)
        print("\n[Testing Invalid Input: Negative Fine Rate]")
        try:
            calculate_fine(loans[0], reference_date, -10.0)
        except InvalidInputError as e:
            print(f"Caught Input Error -> Field: '{e.field}', Value: {e.value}, Reason: {e.reason}")


if __name__ == "__main__":
    try:
        main()
    except LibraryException as err:
        print(f"Top-level Library Exception caught: {err}")
    except Exception as err:
        print(f"Top-level Unexpected Error caught: {err}")

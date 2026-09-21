from model import Pipeline


class Book:
    def __init__(self, title: str, pages: int, category: str):
        self.title = title
        self.pages = pages
        self.category = category

    def __repr__(self) -> str:
        return f"Book({self.title}, {self.pages}, {self.category})"


books = [
    Book("Python", 300, "Programming"),
    Book("Math", 150, "Education"),
    Book("JavaScript", 400, "Programming"),
]


pipeline = Pipeline(books)


# Filter books with more than 200 pages
long_books = pipeline.filter(
    lambda book: book.pages > 200
)

print("Long books:")
print(long_books)


# Get only book titles
titles = pipeline.transform(
    lambda book: book.title
)

print("\nBook titles:")
print(titles)


# Group books by category
books_by_category = pipeline.group_by(
    lambda book: book.category
)

print("\nGrouped books:")
print(books_by_category)
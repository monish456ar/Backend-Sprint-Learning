# 1. BOOK DATA

books = [
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy", "year": 1937, "price": 15.99},
    {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "genre": "Fantasy", "year": 1954, "price": 25.99},
    {"title": "Harry Potter", "author": "J.K. Rowling", "genre": "Fantasy", "year": 1997, "price": 20.00},
    {"title": "Dune", "author": "Frank Herbert", "genre": "Sci-Fi", "year": 1965, "price": 18.50},
    {"title": "1984", "author": "George Orwell", "genre": "Dystopian", "year": 1949, "price": 12.99},
    {"title": "Animal Farm", "author": "George Orwell", "genre": "Dystopian", "year": 1945, "price": 10.99},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance", "year": 1813, "price": 9.99},
    {"title": "Emma", "author": "Jane Austen", "genre": "Romance", "year": 1815, "price": 11.99},
    {"title": "Foundation", "author": "Isaac Asimov", "genre": "Sci-Fi", "year": 1951, "price": 16.99},
    {"title": "I, Robot", "author": "Isaac Asimov", "genre": "Sci-Fi", "year": 1950, "price": 14.99},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Classic", "year": 1925, "price": 13.99},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Classic", "year": 1960, "price": 14.50},
    {"title": "The Alchemist", "author": "Paulo Coelho", "genre": "Classic", "year": 1988, "price": 15.00},
    {"title": "The Notebook", "author": "Nicholas Sparks", "genre": "Romance", "year": 1996, "price": 12.50},
    {"title": "Dune", "author": "Frank Herbert", "genre": "Sci-Fi", "year": 1965, "price": 18.50},
]


# 2. GET GENRES

genres = {book["genre"] for book in books}

print("Genres:", genres)


# 3. GENRE REPORT

for genre in genres:
    genre_books = [book for book in books if book["genre"] == genre]

    count = len(genre_books)

    average = sum(book["price"] for book in genre_books) / count

    latest = max(genre_books, key=lambda book: book["year"])

    print("\nGenre:", genre)
    print("Titles:", count)
    print("Average price:", round(average, 2))
    print("Latest book:", latest["title"])


# 4. REMOVE DUPLICATES

seen = set()
unique_books = []
duplicates = []

for book in books:
    key = (book["title"], book["author"])

    if key in seen:
        duplicates.append(book)
    else:
        seen.add(key)
        unique_books.append(book)

books = unique_books

print("\nDuplicates removed:", len(duplicates))

for book in duplicates:
    print("Removed:", book["title"], "-", book["author"])

print("Reason: same title and author already existed.")


# 5. AUTHOR -> TITLES

author_books = {}

for book in books:
    author = book["author"]

    if author not in author_books:
        author_books[author] = []

    author_books[author].append(book["title"])

print("\nBooks by author:")
print(author_books)


# 6. ALL UNIQUE AUTHORS

authors = {book["author"] for book in books}

print("\nAll authors:")
print(authors)


# 7. AUTHORS WHO APPEAR MORE THAN ONCE

from collections import Counter

author_count = Counter(book["author"] for book in books)

repeated_authors = {
    author
    for author, count in author_count.items()
    if count > 1
}

print("\nAuthors with more than one book:")
print(repeated_authors)
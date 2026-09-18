from dataclasses import dataclass


class Book:
    """Represent a book."""

    category = "Programming"

    def __init__(self, title: str, author: str) -> None:
        self.title = title
        self.author = author

    @property
    def get_info(self) -> str:
       
        return f"Title is {self.title} by {self.author}"

    @staticmethod
    def calculate_avg(a: int, b: int) -> float:
       
        return (a + b) / 2


class User(Book):
    
    def __init__(self, title: str, author: str) -> None:
        super().__init__(title, author)

    def __str__(self) -> str:
        return f"The title of the book is {self.title} published by {self.author}"


book1 = Book("Python Basic", "John")

print(book1.get_info)
print(Book.calculate_avg(5, 5))
print(book1.category)

user1 = User("SQL", "Deva")
print(user1)


@dataclass
class Employee:

    name: str
    age: int
    role: str


emp1 = Employee("Monish", 25, "Developer")
emp2 = Employee("Monish", 25, "Developer")

print(emp1)
print(emp1 == emp2)
from collections.abc import Callable


print("\n==========  Parameter Type Annotation ==========\n")


def greet(name: str) -> None:
    print(f"Hello {name}")


greet("Monish")


print("\n==========  Return Type Annotation ==========\n")


def add(a: int, b: int) -> int:
    return a + b


result = add(10, 20)
print(f"Result: {result}")


print("\n==========  None Return Type ==========\n")


def say_hello() -> None:
    print("Hello!")


say_hello()


print("\n==========  T | None ==========\n")


def find_name(user_id: int) -> str | None:
    if user_id == 1:
        return "Monish"
    return None


print(f"Found user: {find_name(1)}")
print(f"Missing user: {find_name(2)}")


print("\n==========  Union (int | str) ==========\n")


def display_id(user_id: int | str) -> None:
    print(f"User ID: {user_id}")


display_id(101)
display_id("user-101")


print("\n==========  Callable ==========\n")


def calculate(
    a: int,
    b: int,
    operation: Callable[[int, int], int],
) -> int:
    return operation(a, b)


def multiply(x: int, y: int) -> int:
    return x * y


result = calculate(5, 4, multiply)
print(f"Result: {result}")


print("\n==========  Type Narrowing ==========\n")


def process(value: int | str) -> None:
    if isinstance(value, str):
        print(f"String: {value.lower()}")
    else:
        print(f"Integer: {value * 2}")


process("HELLO")
process(10)


print("\n==========  Type Inference ==========\n")


name = "Monish"
age = 25
price = 99.5

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Price: {price}")


print("\n==========  Explicit Annotation vs Inference ==========\n")


city = "Bangalore"       
country: str = "India"   
print(f"City: {city}")
print(f"Country: {country}")




print("\n==========  Keyword ony args ==========\n")


def create_user(name, *, age):
    print(f"{name} is {age} years old")


create_user("Monish", age=25)



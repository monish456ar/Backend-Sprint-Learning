

# from model import Pipeline, PipelineConfig, validate_records


# class User:
#     def __init__(self, name: str, age: int, department: str):
#         self.name = name
#         self.age = age
#         self.department = department

#     def __repr__(self) -> str:
#         return f"User({self.name}, {self.age}, {self.department})"


# class UserValidator:
#     def validate(self, item: User) -> bool:
#         return item



# users = [
#     User("Monish", 29, "Engineering"),
#     User("Rahul", 17, "Engineering"),
#     User("Priya", 25, "HR"),
#     User("Arun", 31, "Engineering"),
#     User("group1", 29, "Engineering"),
#     User("Arun", 29, "Engineering"),
#     User("Arun", 17, "Engineering"),

# ]


# config: PipelineConfig = {
#     "name": "user-pipeline",
#     "enabled": True,
#     "batch_size": 100,
# }


# # 1. Validate records

# validated_users = validate_records(users, UserValidator())

# print("Validated users:")
# print(validated_users)


# # 2. Create pipeline
# user_pipeline = Pipeline(users)


# # 3. Filter
# filtered_users = user_pipeline.filter(
#     lambda user: user.age >= 25
# )

# print("\nFiltered users:")
# print(filtered_users)


# # 4. Transform
# user_names = user_pipeline.transform(
#     lambda user: user.name
# )

# print("\nUser names:")
# print(user_names)


# # 5. Group
# users_by_department = user_pipeline.group_by(
#     lambda user: user.department
# )



# groupbyage=user_pipeline.group_by(
#     lambda user: user.age
# )

# print("\nGrouped users:")
# print(users_by_department)
# print(groupbyage)



# # 6. Configuration

# print("\nPipeline configuration:")
# print(config)

import time
from functools import wraps

from model import Pipeline, PipelineConfig, validate_records


# ==================================================
# Day 6 - Generic Pipeline Utilities
# ==================================================


class User:
    def __init__(self, name: str, age: int, department: str):
        self.name = name
        self.age = age
        self.department = department

    def __repr__(self) -> str:
        return f"User({self.name}, {self.age}, {self.department})"


class UserValidator:
    def validate(self, item: User) -> bool:
        return item


users = [
    User("Monish", 29, "Engineering"),
    User("Rahul", 17, "Engineering"),
    User("Priya", 25, "HR"),
    User("Arun", 31, "Engineering"),
    User("group1", 29, "Engineering"),
    User("Arun", 29, "Engineering"),
    User("Arun", 17, "Engineering"),
]


config: PipelineConfig = {
    "name": "user-pipeline",
    "enabled": True,
    "batch_size": 100,
}


validated_users = validate_records(users, UserValidator())

print("Validated users:")
print(validated_users)


user_pipeline = Pipeline(users)


filtered_users = user_pipeline.filter(
    lambda user: user.age >= 25
)

print("\nFiltered users:")
print(filtered_users)


user_names = user_pipeline.transform(
    lambda user: user.name
)

print("\nUser names:")
print(user_names)


users_by_department = user_pipeline.group_by(
    lambda user: user.department
)

groupbyage = user_pipeline.group_by(
    lambda user: user.age
)

print("\nGrouped users:")
print(users_by_department)
print(groupbyage)


print("\nPipeline configuration:")
print(config)


# ==================================================
# Day 7 - Decorators
# ==================================================


# 1. Timing Decorator
# ==================================================

print("\n--- Timing Decorator ---")


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        
        result = func(*args, **kwargs)

        end = time.time()
        print(start,end)
        print("Time taken:", end - start)

        return result

    return wrapper


@timer
def add(a: int, b: int):
    time.sleep(1)
    return a + b


print("Result:", add(10, 20))


# 2. Retry Decorator
# ==================================================

print("\n--- Retry Decorator ---")


def retry(attempts, delay):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            for attempt in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print("Attempt failed")

                    if attempt == attempts - 1:
                        raise

                    time.sleep(delay)

        return wrapper

    return decorator


count = 0


@retry(attempts=3, delay=1)
def test_retry():
    global count

    count += 1
    print("Attempt:", count)

    if count < 3:
        raise Exception("Something went wrong")

    return "Success"


print(test_retry())


# 3. Caching Decorator
# ==================================================

print("\n--- Caching Decorator ---")


def cache(duration):
    def decorator(func):
        saved_result = None
        saved_time = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal saved_result, saved_time

            current_time = time.time()

            if current_time - saved_time < duration:
                print("Using cached result")
                return saved_result

            saved_result = func(*args, **kwargs)
            saved_time = current_time

            return saved_result

        return wrapper

    return decorator


@cache(duration=10)
def calculate(a, b):
    print("Function is executing")
    return a + b


print("First call:", calculate(10, 20))
print("Second call:", calculate(10, 20))


# 4. Runtime Type Checking
# ==================================================

print("\n--- Type Checking Decorator ---")


def type_check(func):
    @wraps(func)
    def wrapper(*args):

        for value, expected_type in zip(
            args,
            func.__annotations__.values()
        ):
            if not isinstance(value, expected_type):
                raise TypeError(
                    f"Expected {expected_type.__name__}, "
                    f"got {type(value).__name__}"
                )

        return func(*args)

    return wrapper


@type_check
def create_user(name: str, age: int):
    return f"{name} is {age} years old"


print(create_user("Monish", 20))


# 5. Stacking Decorators
# ==================================================

print("\n--- Stacked Decorators ---")


@timer
@cache(duration=10)
@type_check
def multiply(a: int, b: int):
    print("Multiplication executing")
    return a * b


print("First call:", multiply(5, 10))
print("Second call:", multiply(5, 10))
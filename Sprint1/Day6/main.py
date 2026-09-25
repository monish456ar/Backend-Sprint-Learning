

from model import Pipeline, PipelineConfig, validate_records


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


# 1. Validate records

validated_users = validate_records(users, UserValidator())

print("Validated users:")
print(validated_users)


# 2. Create pipeline
user_pipeline = Pipeline(users)


# 3. Filter
filtered_users = user_pipeline.filter(
    lambda user: user.age >= 25
)

print("\nFiltered users:")
print(filtered_users)


# 4. Transform
user_names = user_pipeline.transform(
    lambda user: user.name
)

print("\nUser names:")
print(user_names)


# 5. Group
users_by_department = user_pipeline.group_by(
    lambda user: user.department
)



groupbyage=user_pipeline.group_by(
    lambda user: user.age
)

print("\nGrouped users:")
print(users_by_department)
print(groupbyage)



# 6. Configuration

print("\nPipeline configuration:")
print(config)
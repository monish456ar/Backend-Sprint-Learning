# custom Exception
class InvalidAgeError(Exception):

    def __init__(self, age:int):
        self.age=age
        super().__init__(f"Invalid age {age}")



def check_age(age:int)-> None:
    if age < 18:
        raise InvalidAgeError(age)
    else:
        print("age checking finished!!")


try:
    check_age(15)


except InvalidAgeError as error:
    print(error)
    print(f"Invalid age was: {error.age}")



try:
    age=int(input("Enter the age :"))

except ValueError:
    print("Enter the valid number")

else:
    print(f"your age is {age}")

finally:
    print("Age checking Finished")


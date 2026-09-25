from functools import wraps
import time


# print(time.time())

print("\n\n\n---- First Class Functions ---")

def greet(usename):
    print(f"Hello {usename}")

user1=greet
user1("Monish")

def greet2(fun):
     fun("Luffy")
greet2(greet);





print("\n\n\n---- clouser ---")
# clouser

def outer():
     count=0;
     def inner():
          nonlocal count
          count+=1
          print(f"count  -  {count}")
     return inner


counter = outer();
counter()
counter()
counter()


# //decorator

print("\n\n\n---- decorator ---")

def require_admin(fun):
    def wrapper():
        user_role = "admin"

        if user_role != "admin":
            return "Access Denied"

        fun()

    return wrapper


@require_admin
def delete_user()->None:
    print("User Deleted Successfully")


result = delete_user()
# print(result)
       


# Decorator accept argumetn with three levels

print("\n\n\n---- Decorator with multi-level ---")

def invite(msg):
  def decorator(fun):
    def wrapper():
        print(msg)
        fun()
    return wrapper
  return decorator


@invite("hello")
def say_name():
    print("Monish")

say_name()


# functools.wraps

print("\n\n\n---- Functools.wraps ---")

print("\n\n\n---- without Wraps ---")

def decorator(fun):
    def wrapper():
        print("Before invokeing the function")
        fun()
    return wrapper

@decorator
def login():
    print("Login Succesfully")
login()
print(f"without using wraps login funciton name is {login.__name__}")


# with wraps
print("\n\n\n---- with Wraps ---")

def decorator1(fun):
    @wraps(fun)
    def wrapper():
        print("Before invoking the function")
        fun()
    return wrapper

@decorator1
def login1():
    print("Login Succesfully")
login1()
print(f"with using wraps login funciton name is {login1.__name__}")




print("\n\n\n--- class based decorators ---")


class User:
    def __init__(self,fun):
        self.fun=fun

    def __call__(self, *args, **kwds):
        print("checking")
        self.fun()

@User
def userlogin():
    print("Login succesful")

userlogin.__call__()




# multiple decorator with one function
print("\n\n\n---multiple decorator with one function ---")


def first(func):
    def wrapper():
        print("first")
        func()
    return wrapper


def second(func):
    def wrapper():
        print("second")
        func()
    return wrapper

@first
@second
def hello():
    print("Hello")

hello()
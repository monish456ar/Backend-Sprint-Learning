

from typing import Generic, TypeVar,Protocol,TypedDict;


T = TypeVar("T")

def check_type(value : T)-> T:
    return value

print(check_type(1));
print(check_type("affa"));
print(check_type(True));



# Generic
class Box(Generic[T]):
    def __init__(self,value : T):
        self.value=value
        super().__init__()

    def __str__(self):
        return f"value is {self.value}"



box1=Box(231)
box2=Box("alfkjfl")

box3=Box(True)

print(box1,box3,box2)



# //protocol


from typing import Protocol

class Profile(Protocol):
    def show_profile(self) -> str:
        ...


class User:
    def __init__(self,name:str,age:int):
        self.name=name
        self.age=age

    def show_profile(self)->str:
        return f"Name is {self.name}, age - {self.age}"
        # return 20;/



user1=User("Monish",20);
print(user1.show_profile())


from typing import Literal,Final,Annotated,overload


class Lit(TypedDict):
    name:str
    age:int
    status:Literal["todo","inprogress","complete"]

 

# emp1 :Lit={
#     "name":"Monish",
#     "age":29,
#     "status":"kafj"
# }

# print(emp1)





name:Final="Monish"
# name="kumar"
# print(name)



# annotated

usercount : Annotated[int,"count should be positive"]=23





# overload


@overload
def get_value(value: bool) -> bool:
    ...

@overload
def get_value(value: int) -> int:
    ...

@overload
def get_value(value: str) -> str:
    ...

def get_value(value):
    return value


print(get_value("jafldaj"))
print(get_value(12))
print(get_value(True))
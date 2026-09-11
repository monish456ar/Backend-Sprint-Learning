import copy

# list
tasks = ["login", "dashboard", "profile"]

tasks.append("settings")
print(tasks)


# tuple
location = (12.97, 77.59)

print(location[0])


# dictionary
user = {
    "name": "Monish",
    "role": "admin",
    "age": 25
}

user["role"] = "member"
print(user)


# set
roles = {"admin", "member", "admin"}

print(roles)



# enumerate
for i, task in enumerate(tasks):
    print(i, task)


# zip
names = ["Monish", "Rahul", "John"]
roles = ["admin", "member", "member"]

for name, role in zip(names, roles):
    print(name, role)


# sorted
prices = [50, 20, 80, 10]

new_prices = sorted(prices)

print(prices)
print(new_prices)




# shallow copy
user = {
    "name": "Monish",
    "skills": ["Python", "JS"]
}

copy_user = user.copy()

copy_user["name"] = "Rahul"

print(user)
print(copy_user)
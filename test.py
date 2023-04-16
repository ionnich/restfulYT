import requests

# the base URL is assigned by default,
# you can find it via the response of main.py
BASE = "http://127.0.0.1:5000/"

# get user input
gate = input("p/g post or get?")
if gate == "p":
    username = input("username: ")
    password = input("password: ")
    key = input("key: ")
    # send the post request
    response = requests.post(
        BASE + "def/%d" % int(key), {"username": username, "password": password}
    )
    print(response.json())
elif gate == "g":
    key = input("enter key")
    response = requests.get(BASE + "def/%d" % int(key))
    print(response.json())
elif gate == "d":
    key = input("enter key")
    response = requests.delete(BASE + "def/%d" % int(key))
    print(response.json())

import hashlib
from datetime import datetime, timedelta, timezone
import jwt
import bcrypt
import secrets


SECRET_KEY = "7d9f5e0c8a7f4b0d9f3e6a1c2b5d8e7f4a9c1b2d3e4f5a6b7c8d9e0f1a2b3c4"

payload = {"username":"karan"}
payload["type"] = "refresh"
payload["exp"] = datetime.now(timezone.utc) + timedelta(
        days=7
    )
    

# refresh_token_data = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
# print(refresh_token_data)
# decoded_payload = jwt.decode(refresh_token_data,SECRET_KEY, algorithms=["HS256"])
# print(decoded_payload)

# token =refresh_token_data
# x=hashlib.sha256(
#         token.encode("utf-8")
#     ).hexdigest()
# print(x)
# tokens =refresh_token_data
# y=hashlib.sha256(
#         tokens.encode("utf-8")
#     ).hexdigest()
# print(x)

# from contextlib import contextmanager


# class User:
#     def greet(self):
#         return "Hello"

# user = User()

# print(user.greet())  # Original method


# # Monkey patch the method
# def new_greet(self):
#     return "Hi from monkey patch"

# User.greet = new_greet

# print(user.greet())  # Patched method


# class A:
#     pass

# x = A()
# y = A()

# x.other = y
# y.other = x


import asyncio

async def greet():
    print("Hello")
    await asyncio.sleep(2)
    print("World")

asyncio.run(greet())


import time

def greet():
    print("Hello")
    time.sleep(2)
    print("World")

greet()
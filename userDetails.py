# Accept user inputs
username = input("Enter your username: ")
full_name = input("Enter your full name: ")
country = input("Enter your country: ")
language = input("Enter your preferred language: ")

# Create and print welcome message
message = f"""
Welcome, {full_name}!

Your username is {username}, and it's great to have someone from {country} here.
We see that you prefer communicating in {language}, which is awesome.

We’re glad to have you onboard—enjoy your experience!
"""

print(message)

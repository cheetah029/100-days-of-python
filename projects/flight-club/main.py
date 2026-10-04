import requests

USERS_ENDPOINT = "https://api.sheety.co/ee9361440c6750b82748259e8e305a24/flightDeals/users"

name = "Aaron"
print(f"Welcome to {name}'s Flight Club.")
print("We find the best flight deals and email you.")
f_name = input("What is your first name?\n")
l_name = input("What is your last name?\n")
email = input("What is your email?\n")
email_validation = input("Type your email again.\n")

while email != email_validation:
    print("That's not right, let's try again:")
    email = input("What is your email?\n")
    email_validation = input("Type your email again.\n")

user_data = {
  "user": {
    "firstName": f_name,
    "lastName": l_name,
    "email": email
  }
}

response = requests.post(USERS_ENDPOINT, json=user_data)
# print(response.text)
if response.status_code == 200:
  print("Success! Your email has been added, look forward to some amazing flight deals!")
else:
  print("There was an issue, please try again later.")

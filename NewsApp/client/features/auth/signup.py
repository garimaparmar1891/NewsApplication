from utils.http_client import authorized_request
from utils.endpoints import SIGNUP

def signup():
    name, email, password = prompt_signup_details()
    response = perform_signup_request(name, email, password)
    handle_signup_response(response)

def prompt_signup_details():
    name = input("Name: ")
    email = input("Email: ")
    password = input("Password: ")
    return name, email, password

def perform_signup_request(name, email, password):
    return authorized_request(
        method="POST",
        endpoint=SIGNUP,
        json={
            "username": name,
            "email": email,
            "password": password
        }
    )

def handle_signup_response(response):
    if response.ok:
        print("Signup successful.")
    else:
        try:
            print("Signup failed:", response.json().get("message", "Unknown error"))
        except ValueError:
            print("Signup failed: Invalid response from server.")

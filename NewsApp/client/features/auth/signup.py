from utils.http_client import authorized_request

def signup():
    name = input("Name: ")
    email = input("Email: ")
    password = input("Password: ")

    res = authorized_request(
        method="POST",
        endpoint="/api/signup",
        json={
            "username": name,
            "email": email,
            "password": password
        }
    )

    if res.ok:
        print("Signup successful.")
    else:
        try:
            print("Signup failed:", res.json().get("message", "Unknown error"))
        except ValueError:
            print("Signup failed: Invalid response from server.")

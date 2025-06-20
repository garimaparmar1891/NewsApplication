from utils.http_client import authorized_request
from utils.token_storage import save_token, save_user_info

def login():
    email = input("Email: ")
    password = input("Password: ")

    response = authorized_request(
        method="POST",
        endpoint="/api/login",
        json={
            "email": email,
            "password": password
        }
    )

    try:
        data = response.json()

    except ValueError:
        print("Login failed: Invalid response format.")
        return None

    if response.ok and "access_token" in data.get("data", {}):
        access_token = data["data"]["access_token"]
        user_info = {
            "username": data["data"].get("username", "User"),
            "role": data["data"].get("role", "User")
        }

        save_token(access_token)
        save_user_info(user_info)

        print(f"Login successful. Welcome, {user_info['username']}!")
        return user_info["role"].lower()
    else:
        print("Login failed:", data.get("message", "Unknown error"))
        return None

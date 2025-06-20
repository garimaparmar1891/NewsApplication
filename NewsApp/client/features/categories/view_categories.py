import requests
from utils.http_client import authorized_request

def display_categories():
    print("\nAvailable Categories:")
    try:
        response = authorized_request("GET", "/api/categories")

        if response.status_code == 200:
            data = response.json()
            categories = data.get("data", [])
            if not categories:
                print("No categories found.")
                return

            for cat in categories:
                print(f"{cat['id']}. {cat['name']}")

        else:
            print("Failed to fetch categories.")
    except Exception as e:
        print("Error fetching categories:", str(e))

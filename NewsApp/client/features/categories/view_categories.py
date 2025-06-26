from utils.http_client import authorized_request
from utils.endpoints import GET_CATEGORIES

def display_categories():
    categories = fetch_categories()
    print_categories(categories)

def fetch_categories():
    try:
        response = authorized_request("GET", GET_CATEGORIES)
        if response.status_code != 200:
            print("Failed to fetch categories.")
            return []
        data = response.json()
        return data.get("data", [])
    except Exception as e:
        print("Error fetching categories:", str(e))
        return []

def print_categories(categories):
    if not categories:
        print("No categories found.")
        return
    print("\nAvailable Categories:")
    for cat in categories:
        print(f"{cat['id']}. {cat['name']}")

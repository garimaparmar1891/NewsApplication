from utils.http_client import authorized_request
from utils.endpoints import ADD_CATEGORY

def add_news_category():
    category_name = get_category_input()
    if not is_valid_category_name(category_name):
        print("Category name cannot be empty.")
        return
    response = send_category_request(category_name)
    if response.ok:
        print_category_result(True, category_name)
    else:
        error_msg = response.json().get("message", "Unknown error")
        print_category_result(False, category_name, error_msg)

def get_category_input():
    return input("Enter new category name: ").strip()

def is_valid_category_name(name):
    return bool(name)

def send_category_request(name):
    return authorized_request("POST", ADD_CATEGORY, json={"name": name})

def print_category_result(success, name, message=None):
    if success:
        print(f"Category '{name}' added successfully.")
    else:
        print(f"Failed to add category: {message or 'Unknown error'}")

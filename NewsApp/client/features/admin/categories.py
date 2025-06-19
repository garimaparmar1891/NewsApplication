from utils.http_client import authorized_request

def add_news_category():
    category_name = input("Enter new category name: ").strip()
    if not category_name:
        print("Category name cannot be empty.")
        return

    response = authorized_request("POST", "/api/admin/categories", json={"name": category_name})
    if response.ok:
        print(f"Category '{category_name}' added successfully.")
    else:
        print("Failed to add category:", response.json().get("message", "Unknown error"))

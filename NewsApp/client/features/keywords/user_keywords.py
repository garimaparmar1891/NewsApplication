from utils.http_client import authorized_request

def add_user_keyword():
    print("\n--- Add User Keyword ---")
    keyword = input("Enter a keyword to track: ").strip()
    if not keyword:
        print("Keyword cannot be empty.")
        return

    response = authorized_request("POST", "/api/user-keywords", json={"keyword": keyword})

    if response.ok:
        print("Keyword added successfully.")
    else:
        print("Failed to add keyword:", response.json().get("message", response.text))


def view_user_keywords():
    print("\n--- Your Tracked Keywords ---")
    response = authorized_request("GET", "/api/user-keywords")

    if response.ok:
        keywords = response.json().get("data", [])
        if not keywords:
            print("No keywords found.")
        else:
            for idx, keyword in enumerate(keywords, 1):
                print(f"[{idx}] ID: {keyword['Id']} | Keyword: {keyword['Keyword']}")
    else:
        print("Failed to fetch keywords:", response.json().get("message", response.text))


def delete_user_keyword():
    print("\n--- Delete User Keyword ---")
    keyword_id = input("Enter the Keyword ID to delete: ").strip()
    if not keyword_id.isdigit():
        print("Invalid ID.")
        return

    response = authorized_request("DELETE", f"/api/user-keywords/{keyword_id}")

    if response.ok:
        print("Keyword deleted successfully.")
    else:
        print("Failed to delete keyword:", response.json().get("message", response.text))


from utils.http_client import authorized_request

def add_notification_keyword():
    print("\n--- Add Notification Keyword ---")
    keyword = input("Enter keyword to be notified about: ").strip()
    category = input("Enter category (optional, press Enter to skip): ").strip()

    data = {"keyword": keyword}
    if category:
        data["category"] = category

    response = authorized_request("POST", "/api/notifications/keywords", json=data)

    if response.ok:
        print("Keyword added for notifications.")
    else:
        print("Failed to add keyword:", response.json().get("message", response.text))


def view_notification_keywords():
    print("\n--- Notification Keywords ---")
    response = authorized_request("GET", "/api/notifications/keywords")
    print(response)
    if response.ok:
        keywords = response.json().get("data", [])
        if not keywords:
            print("No notification keywords set.")
        else:
            for idx, keyword in enumerate(keywords, 1):
                print(f"[{idx}] Keyword: {keyword['Keyword']}, Category: {keyword.get('Category', 'All')}")
    else:
        print("Failed to fetch notification keywords:", response.json().get("message", response.text))


def delete_notification_keyword():
    print("\n--- Delete Notification Keyword ---")
    keyword_id = input("Enter the ID of the keyword to delete: ").strip()
    response = authorized_request("DELETE", f"/api/notifications/keywords/{keyword_id}")

    if response.ok:
        print("Notification keyword deleted.")
    else:
        print("Failed to delete keyword:", response.json().get("message", response.text))

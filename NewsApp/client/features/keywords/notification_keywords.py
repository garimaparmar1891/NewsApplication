from utils.http_client import authorized_request
from utils.endpoints import (
    ADD_NOTIFICATION_KEYWORD,
    GET_NOTIFICATION_KEYWORDS,
    DELETE_NOTIFICATION_KEYWORD
)

def add_notification_keyword():
    print("\n--- Add Notification Keyword ---")
    data = prompt_keyword_data()
    response = send_add_notification_keyword_request(data)
    print_add_notification_keyword_status(response)

def send_add_notification_keyword_request(data):
    return authorized_request("POST", ADD_NOTIFICATION_KEYWORD, json=data)

def print_add_notification_keyword_status(response):
    if response.ok:
        print("Keyword added for notifications.")
    else:
        print("Failed to add keyword:", response.json().get("message", response.text))


def view_notification_keywords():
    print("\n--- Notification Keywords ---")
    response = send_view_notification_keywords_request()
    print_view_notification_keywords_status(response)

def send_view_notification_keywords_request():
    return authorized_request("GET", GET_NOTIFICATION_KEYWORDS)

def print_view_notification_keywords_status(response):
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
    response = send_delete_notification_keyword_request(keyword_id)
    print_delete_notification_keyword_status(response)

def send_delete_notification_keyword_request(keyword_id):
    return authorized_request("DELETE", DELETE_NOTIFICATION_KEYWORD.format(keyword_id=keyword_id))

def print_delete_notification_keyword_status(response):
    if response.ok:
        print("Notification keyword deleted.")
    else:
        print("Failed to delete keyword:", response.json().get("message", response.text))

def prompt_keyword_data():
    keyword = input("Enter keyword to be notified about: ").strip()
    category = input("Enter category (optional, press Enter to skip): ").strip()
    data = {"keyword": keyword}
    if category:
        data["category"] = category
    return data

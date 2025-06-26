from utils.http_client import authorized_request
from utils.endpoints import (
    ADD_USER_KEYWORD,
    GET_USER_KEYWORDS,
    DELETE_USER_KEYWORD
)


def add_user_keyword():
    print("\n--- Add User Keyword ---")
    keyword = prompt_user_keyword()
    if not keyword:
        print("Keyword cannot be empty.")
        return
    response = send_add_user_keyword_request(keyword)
    print_add_user_keyword_status(response)

def prompt_user_keyword():
    return input("Enter a keyword to track: ").strip()

def send_add_user_keyword_request(keyword):
    return authorized_request("POST", ADD_USER_KEYWORD, json={"keyword": keyword})

def print_add_user_keyword_status(response):
    if response.ok:
        print("Keyword added successfully.")
    else:
        print("Failed to add keyword:", response.json().get("message", response.text))


def view_user_keywords():
    print("\n--- Your Tracked Keywords ---")
    response = send_view_user_keywords_request()
    print_view_user_keywords_status(response)

def send_view_user_keywords_request():
    return authorized_request("GET", GET_USER_KEYWORDS)

def print_view_user_keywords_status(response):
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
    keyword_id = prompt_keyword_id()
    if not keyword_id.isdigit():
        print("Invalid ID.")
        return
    response = send_delete_user_keyword_request(keyword_id)
    print_delete_user_keyword_status(response)

def prompt_keyword_id():
    return input("Enter the Keyword ID to delete: ").strip()

def send_delete_user_keyword_request(keyword_id):
    return authorized_request("DELETE", DELETE_USER_KEYWORD.format(keyword_id=keyword_id))

def print_delete_user_keyword_status(response):
    if response.ok:
        print("Keyword deleted successfully.")
    else:
        print("Failed to delete keyword:", response.json().get("message", response.text))

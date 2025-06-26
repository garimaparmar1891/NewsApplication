from utils.http_client import authorized_request
from utils.paginated_menu import interactive_paginated_menu
from utils.endpoints import TODAY_HEADLINES

def get_today_headlines():
    print("\n--- Today's Headlines ---")
    response = fetch_today_headlines()
    if not response.ok:
        print_error(response.json().get("message", response.text))
        return
    articles = response.json().get("data", [])
    display_headlines(articles)

def fetch_today_headlines():
    return authorized_request("GET", TODAY_HEADLINES)

def print_error(message):
    print(f"{message}")

def display_headlines(articles):
    if not articles:
        print("No headlines available today.")
        return
    interactive_paginated_menu(articles, context_label="Today's Articles")

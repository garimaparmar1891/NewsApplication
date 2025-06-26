from utils.http_client import authorized_request
from utils.paginated_menu import interactive_paginated_menu
from utils.endpoints import GET_ARTICLES_BY_RANGE
from utils.date_validator import validate_date_range_input

def get_articles_by_range():
    print("\n--- Fetch Articles by Date Range ---")
    category = prompt_category()
    start, end = validate_date_range_input()
    if not start or not end:
        print_error("Invalid date range. Operation cancelled.")
        return
    articles = fetch_articles_by_range(start, end, category)
    if articles is not None:
        display_articles(articles, start, end)

def prompt_category():
    return input("Optional Category (press Enter to skip): ").strip()

def print_error(message):
    print(f"{message}")

def fetch_articles_by_range(start, end, category=None):
    params = {"start_date": start, "end_date": end}
    if category:
        params["category"] = category
    response = authorized_request("GET", GET_ARTICLES_BY_RANGE, params=params)
    if not response.ok:
        print_error(response.json().get("message", response.text))
        return None
    return response.json().get("data", [])

def display_articles(articles, start, end):
    if not articles:
        print("ℹ No articles found for the given range.")
        return
    interactive_paginated_menu(articles, context_label=f"Articles from {start} to {end}")


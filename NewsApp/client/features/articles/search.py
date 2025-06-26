from utils.http_client import authorized_request
from utils.paginated_menu import interactive_paginated_menu
from utils.endpoints import SEARCH_ARTICLES

def search_articles():
    print("\n--- Search Articles ---")
    q, start_date, end_date = prompt_search_criteria()
    params = {"q": q, "start_date": start_date, "end_date": end_date}
    articles = fetch_articles(params)
    if articles is not None:
        display_search_results(articles, q)

def prompt_search_criteria():
    q = input("Enter keyword: ").strip()
    start_date = input("Enter start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter end date (YYYY-MM-DD): ").strip()
    return q, start_date, end_date

def fetch_articles(params):
    response = authorized_request("GET", SEARCH_ARTICLES, params=params)
    if response.status_code != 200:
        print("Failed to fetch articles:", response.json().get("message", response.text))
        return None
    return response.json().get("data", [])

def display_search_results(articles, keyword):
    if not articles:
        print("No articles found for the given criteria.")
        return
    interactive_paginated_menu(articles, context_label=f"Search Results for '{keyword}'")

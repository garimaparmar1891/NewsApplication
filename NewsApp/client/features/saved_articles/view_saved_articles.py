from utils.http_client import authorized_request
from utils.paginated_menu import interactive_paginated_menu
from utils.endpoints import (
    GET_SAVED_ARTICLES,
    UNSAVE_ARTICLE
)

def view_saved_articles_paginated():
    articles = fetch_saved_articles()
    print_saved_articles(articles)

def fetch_saved_articles():
    response = authorized_request("GET", GET_SAVED_ARTICLES)
    if response.status_code != 200:
        print("Failed to fetch saved articles.")
        return []
    data = response.json()
    return data.get("data", {}).get("data", [])

def print_saved_articles(articles):
    if not articles:
        print("No saved articles found.")
        return
    interactive_paginated_menu(articles)


def delete_saved_article(article_id):
    response = send_delete_saved_article_request(article_id)
    print_delete_saved_article_status(response)

def send_delete_saved_article_request(article_id):
    return authorized_request("DELETE", UNSAVE_ARTICLE.format(article_id=article_id))

def print_delete_saved_article_status(response):
    try:
        data = response.json()
        if data.get("success"):
            print("Article deleted successfully!")
        else:
            print(f"{data.get('message', 'Failed to delete article.')}")
    except Exception as e:
        print("Error deleting article:", str(e))

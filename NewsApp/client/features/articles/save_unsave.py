from utils.http_client import authorized_request
from utils.endpoints import SAVE_ARTICLE, UNSAVE_ARTICLE

def save_article():
    print("\n--- Save Article ---")
    article_id = prompt_article_id("save")
    response = authorized_request("POST", SAVE_ARTICLE(article_id))
    msg = response.json().get("message", response.text) if not response.ok else None
    print_result(response.ok, "save", msg)

def unsave_article():
    print("\n--- Unsave Article ---")
    article_id = prompt_article_id("unsave")
    response = authorized_request("DELETE", UNSAVE_ARTICLE(article_id))
    msg = response.json().get("message", response.text) if not response.ok else None
    print_result(response.ok, "unsave", msg)

def prompt_article_id(action):
    return input(f"Enter Article ID to {action}: ").strip()

def print_result(success, action, message=None):
    if success:
        print(f"Article {action}d successfully.")
    else:
        print(f"Failed to {action} article: {message or 'Unknown error'}")

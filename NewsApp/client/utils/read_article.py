from utils.http_client import authorized_request
from utils.token_storage import clear_token
from utils.endpoints import (
    READ_HISTORY,
    LIKE_ARTICLE,
    DISLIKE_ARTICLE,
    SAVE_ARTICLE,
    REPORT_ARTICLE
)

def read_article(article):
    print_article_details(article)
    article_id = article.get("Id")
    record_read_history(article_id)

    while True:
        print_article_options()
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            like_article(article_id)
        elif choice == "2":
            dislike_article(article_id)
        elif choice == "3":
            save_article(article_id)
        elif choice == "4":
            break
        elif choice == "5":
            report_article(article_id)
        elif choice == "6":
            clear_token()
            print("Logged out successfully.")
            exit()
        else:
            print("Invalid choice. Please try again.")

def print_article_details(article):
    print("\n--- Reading Article ---")
    print(f"Article ID : {article.get('Id')}")
    print(f"Title      : {article.get('Title')}")
    print(f"Content    : {article.get('Content', 'No content available.')}")
    print(f"Source     : {article.get('Source')}")
    print(f"Published  : {article.get('PublishedAt')}")
    print(f"URL        : {article.get('Url')}\n")

def record_read_history(article_id):
    read_resp = authorized_request("POST", READ_HISTORY.format(article_id=article_id))
    if read_resp.ok:
        print("Read history recorded.")
    else:
        print("Failed to record read history.")

def print_article_options():
    print("\nOptions:")
    print("1. Like this article")
    print("2. Dislike this article")
    print("3. Save this article")
    print("4. Go back to article list")
    print("5. Report this article")
    print("6. Logout ")
    
def like_article(article_id):
    resp = authorized_request("POST", LIKE_ARTICLE.format(article_id=article_id))
    print("Liked the article." if resp.ok else "Failed to like article.")

def dislike_article(article_id):
    resp = authorized_request("POST", DISLIKE_ARTICLE.format(article_id=article_id))
    print("Disliked the article." if resp.ok else "Failed to dislike article.")

def save_article(article_id):
    resp = authorized_request("POST", SAVE_ARTICLE.format(article_id=article_id))
    print("Article saved." if resp.ok else "Failed to save article.")

def report_article(article_id):
    reason = input("Enter reason for reporting this article: ").strip()
    if not reason:
        print("Report reason cannot be empty.")
        return
    resp = authorized_request("POST", REPORT_ARTICLE.format(article_id=article_id), json={"reason": reason})
    if resp.ok:
        print("Article reported successfully.")
    else:
        print("Failed to report article:", resp.json().get("message", resp.text))

from utils.http_client import authorized_request
from utils.pagination import paginate_articles

def view_saved_articles_paginated():
    response = authorized_request("GET", f"/api/users/saved-articles")
    if response.status_code != 200:
        print("Failed to fetch saved articles.")
        return

    data = response.json()
    articles = data.get("data", {}).get("data", [])

    if not articles:
        print("No saved articles found.")
        return
    paginate_articles(
        articles
    )


def delete_saved_article(article_id):
    try:
        response = authorized_request("DELETE", f"/api/articles/{article_id}/unsave")
        data = response.json()
        if data.get("success"):
            print("Article deleted successfully!")
        else:
            print(f"{data.get('message', 'Failed to delete article.')}")
    except Exception as e:
        print("Error deleting article:", str(e))

from utils.http_client import HttpClient
from utils.endpoints import (
    GET_SAVED_ARTICLES,
    UNSAVE_ARTICLE
)

class SavedArticlesService:
    @staticmethod
    def fetch_saved_articles():
        response = HttpClient.authorized_request("GET", GET_SAVED_ARTICLES)
        if response.status_code != 200:
            return None, "Failed to fetch saved articles."
        data = response.json()
        return data.get("data", {}).get("data", []), None

    @staticmethod
    def delete_saved_article(article_id):
        response = HttpClient.authorized_request("DELETE", UNSAVE_ARTICLE.format(article_id=article_id))
        try:
            data = response.json()
            if data.get("success"):
                return True, "Article deleted successfully!"
            else:
                return False, data.get('message', 'Failed to delete article.')
        except Exception as e:
            return False, f"Error deleting article: {str(e)}" 
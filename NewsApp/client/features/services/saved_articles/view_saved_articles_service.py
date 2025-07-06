from utils.http_client import HttpClient
from utils.endpoints import (
    GET_SAVED_ARTICLES,
    UNSAVE_ARTICLE
)

class SavedArticlesService:
    @staticmethod
    def fetch_saved_articles():
        return HttpClient.authorized_request("GET", GET_SAVED_ARTICLES)

    @staticmethod
    def delete_saved_article(article_id):
        return HttpClient.authorized_request("DELETE", UNSAVE_ARTICLE.format(article_id=article_id))

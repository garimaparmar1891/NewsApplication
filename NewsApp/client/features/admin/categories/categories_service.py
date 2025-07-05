from utils.http_client import HttpClient
from utils.endpoints import (
    ADD_CATEGORY,
    HIDE_UNHIDE_ARTICLE,
    HIDE_UNHIDE_CATEGORY,
    GET_CATEGORY_FOR_ADMIN,
)

class CategoryService:
    """Handles HTTP requests for category operations."""

    @staticmethod
    def add_category(category_name):
        return HttpClient.authorized_request("POST", ADD_CATEGORY, json={"name": category_name})

    @staticmethod
    def hide_unhide_article(article_id, action):
        endpoint = HIDE_UNHIDE_ARTICLE.format(article_id=article_id, action=action)
        return HttpClient.authorized_request("PATCH", endpoint)

    @staticmethod
    def hide_unhide_category(category_id, action):
        endpoint = HIDE_UNHIDE_CATEGORY.format(category_id=category_id, action=action)
        return HttpClient.authorized_request("PATCH", endpoint)

    @staticmethod
    def get_categories_for_admin():
        return HttpClient.authorized_request("GET", GET_CATEGORY_FOR_ADMIN) 
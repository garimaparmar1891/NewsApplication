from utils.http_client import HttpClient
from utils.endpoints import ADD_CATEGORY, HIDE_UNHIDE_ARTICLE, HIDE_UNHIDE_CATEGORY, GET_CATEGORY_FOR_ADMIN
from utils.response_handler import handle_response
from constants.messages import CATEGORY_ADD_SUCCESS, CATEGORY_ADD_FAILED

class CategoriesService:
    @staticmethod
    def add_category(name):
        response = HttpClient.authorized_request(
            method="POST",
            endpoint=ADD_CATEGORY,
            json={"name": name}
        )
        return handle_response(response, CATEGORY_ADD_SUCCESS, CATEGORY_ADD_FAILED)

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

from utils.http_client import HttpClient
from utils.endpoints import (
    ADD_USER_KEYWORD,
    GET_USER_KEYWORDS,
    DELETE_USER_KEYWORD
)

class UserKeywordsService:

    @staticmethod
    def add_user_keyword(keyword, category_id=None):
        if category_id is None:
            category_id = 1
        
        payload = {
            "category_id": category_id,
            "word": keyword
        }
        return HttpClient.authorized_request("POST", ADD_USER_KEYWORD, json=payload)

    @staticmethod
    def view_user_keywords():
        return HttpClient.authorized_request("GET", GET_USER_KEYWORDS)

    @staticmethod
    def delete_user_keyword(keyword_id):
        return HttpClient.authorized_request("DELETE", DELETE_USER_KEYWORD.format(keyword_id=keyword_id))

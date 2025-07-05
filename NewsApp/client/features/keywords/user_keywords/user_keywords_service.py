from utils.http_client import HttpClient
from utils.endpoints import (
    ADD_USER_KEYWORD,
    GET_USER_KEYWORDS,
    DELETE_USER_KEYWORD
)

class UserKeywordsService:
    @staticmethod
    def send_add_user_keyword_request(keyword):
        return HttpClient.authorized_request("POST", ADD_USER_KEYWORD, json={"keyword": keyword})

    @staticmethod
    def send_view_user_keywords_request():
        return HttpClient.authorized_request("GET", GET_USER_KEYWORDS)

    @staticmethod
    def send_delete_user_keyword_request(keyword_id):
        return HttpClient.authorized_request("DELETE", DELETE_USER_KEYWORD.format(keyword_id=keyword_id)) 
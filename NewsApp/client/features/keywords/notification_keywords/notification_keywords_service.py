from utils.http_client import HttpClient
from utils.endpoints import (
    ADD_NOTIFICATION_KEYWORD,
    GET_NOTIFICATION_KEYWORDS,
    DELETE_NOTIFICATION_KEYWORD
)

class NotificationKeywordsService:
    @staticmethod
    def add_notification_keyword(data):
        return HttpClient.authorized_request("POST", ADD_NOTIFICATION_KEYWORD, json=data)

    @staticmethod
    def view_notification_keywords():
        return HttpClient.authorized_request("GET", GET_NOTIFICATION_KEYWORDS)

    @staticmethod
    def delete_notification_keyword(keyword_id):
        return HttpClient.authorized_request("DELETE", DELETE_NOTIFICATION_KEYWORD.format(keyword_id=keyword_id)) 
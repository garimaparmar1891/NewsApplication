from utils.http_client import HttpClient
from utils.endpoints import ADD_BLOCKED_KEYWORD, GET_BLOCKED_KEYWORDS, DELETE_BLOCKED_KEYWORD
from utils.response_handler import handle_response, handle_data_response
from constants.messages import (
    BLOCKED_KEYWORD_BLOCK_FAILED,
    BLOCKED_KEYWORD_FETCH_FAILED,
    BLOCKED_KEYWORD_DELETE_FAILED
)

class BlockedKeywordsService:
    @staticmethod
    def add_blocked_keyword(keyword):
        response = HttpClient.authorized_request("POST", ADD_BLOCKED_KEYWORD, json={"keyword": keyword})
        return handle_response(response, "", BLOCKED_KEYWORD_BLOCK_FAILED)

    @staticmethod
    def get_blocked_keywords():
        response = HttpClient.authorized_request("GET", GET_BLOCKED_KEYWORDS)
        return handle_data_response(response, BLOCKED_KEYWORD_FETCH_FAILED)

    @staticmethod
    def delete_blocked_keyword(keyword_id):
        endpoint = DELETE_BLOCKED_KEYWORD.format(keyword_id=keyword_id)
        response = HttpClient.authorized_request("DELETE", endpoint)
        return handle_response(response, "", BLOCKED_KEYWORD_DELETE_FAILED)

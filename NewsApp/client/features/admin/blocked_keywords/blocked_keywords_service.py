from utils.http_client import HttpClient
from utils.endpoints import ADD_BLOCKED_KEYWORD, GET_BLOCKED_KEYWORDS
from constants import messages as msg

class BlockedKeywordsService:
    """Service for blocked keywords business logic and API calls."""

    @staticmethod
    def add_blocked_keyword(keyword):
        response = HttpClient.authorized_request("POST", ADD_BLOCKED_KEYWORD, json={"keyword": keyword})
        if response.ok:
            return True, msg.BLOCKED_KEYWORD_SUCCESS.format(keyword=keyword)
        error = response.json().get("message", "Unknown error")
        return False, msg.BLOCKED_KEYWORD_BLOCK_FAILED.format(error=error)

    @staticmethod
    def get_blocked_keywords():
        response = HttpClient.authorized_request("GET", GET_BLOCKED_KEYWORDS)
        if response.ok:
            keywords = response.json().get("data", [])
            return True, keywords
        return False, msg.BLOCKED_KEYWORD_FETCH_FAILED 
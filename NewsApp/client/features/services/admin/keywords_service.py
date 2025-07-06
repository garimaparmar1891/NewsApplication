from utils.http_client import HttpClient
from utils.endpoints import KEYWORDS, GET_CATEGORY_FOR_ADMIN

class KeywordsService:

    @staticmethod
    def fetch_categories():
        return HttpClient.authorized_request("GET", GET_CATEGORY_FOR_ADMIN)

    @staticmethod
    def add_keyword(word, category_id):
        payload = {"word": word, "category_id": int(category_id)}
        return HttpClient.authorized_request("POST", KEYWORDS, json=payload)

    @staticmethod
    def delete_keyword(word):
        endpoint = f"{KEYWORDS}/{word}"
        return HttpClient.authorized_request("DELETE", endpoint)

    @staticmethod
    def fetch_keywords():
        return HttpClient.authorized_request("GET", KEYWORDS)

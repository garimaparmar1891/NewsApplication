from utils.http_client import HttpClient
from utils.endpoints import SEARCH_ARTICLES

class SearchService:
    @staticmethod
    def fetch_articles(params):
        response = HttpClient.authorized_request("GET", SEARCH_ARTICLES, params=params)
        if response.status_code != 200:
            print("Failed to fetch articles:", response.json().get("message", response.text))
            return None
        return response.json().get("data", []) 
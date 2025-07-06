from utils.http_client import HttpClient
from utils.endpoints import SEARCH_ARTICLES

class SearchService:
    @staticmethod
    def fetch_articles(params):
        return HttpClient.authorized_request("GET", SEARCH_ARTICLES, params=params)

from utils.http_client import HttpClient
from utils.endpoints import GET_ARTICLES_BY_RANGE, GET_ALL_ARTICLES

class ArticlesByRangeService:
    @staticmethod
    def fetch_articles_by_range(start, end, category=None):
        params = {"start_date": start, "end_date": end}
        if category:
            params["category"] = category
        response = HttpClient.authorized_request("GET", GET_ARTICLES_BY_RANGE, params=params)
        if not response.ok:
            return None, response.json().get("message", response.text)
        return response.json().get("data", []), None

    @staticmethod
    def fetch_all_articles():
        response = HttpClient.authorized_request("GET", GET_ALL_ARTICLES)
        if not response.ok:
            return None, response.json().get("message", response.text)
        return response.json().get("data", []), None 
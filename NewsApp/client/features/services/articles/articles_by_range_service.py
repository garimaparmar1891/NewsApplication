from utils.http_client import HttpClient
from utils.endpoints import GET_ARTICLES_BY_RANGE, GET_ALL_ARTICLES

class ArticlesByRangeService:
    @staticmethod
    def get_articles_by_range(start, end, category=None):
        params = {"start_date": start, "end_date": end}
        if category and category.lower() != 'all':
            params["category"] = category
        return HttpClient.authorized_request("GET", GET_ARTICLES_BY_RANGE, params=params)

    @staticmethod
    def get_all_articles():
        return HttpClient.authorized_request("GET", GET_ALL_ARTICLES)

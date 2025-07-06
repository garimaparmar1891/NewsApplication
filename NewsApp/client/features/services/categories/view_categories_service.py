from utils.http_client import HttpClient
from utils.endpoints import GET_CATEGORIES

class CategoryService:
    @staticmethod
    def fetch_categories():
        return HttpClient.authorized_request("GET", GET_CATEGORIES)

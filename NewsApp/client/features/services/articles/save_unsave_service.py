from utils.http_client import HttpClient
from utils.endpoints import SAVE_ARTICLE, UNSAVE_ARTICLE

class ArticleSaveService:
    
    @staticmethod
    def save_article(article_id):
        endpoint = SAVE_ARTICLE.replace('{article_id}', str(article_id))
        return HttpClient.authorized_request("POST", endpoint)

    @staticmethod
    def unsave_article(article_id):
        endpoint = UNSAVE_ARTICLE.replace('{article_id}', str(article_id))
        return HttpClient.authorized_request("DELETE", endpoint)

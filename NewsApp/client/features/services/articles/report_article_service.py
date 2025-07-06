from utils.http_client import HttpClient
from utils.endpoints import REPORT_ARTICLE

class ReportArticleService:
    
    @staticmethod
    def report_article(article_id, reason):
        endpoint = REPORT_ARTICLE.replace('{article_id}', str(article_id))
        return HttpClient.authorized_request("POST", endpoint, json={"reason": reason})

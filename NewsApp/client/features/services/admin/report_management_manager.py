from utils.http_client import HttpClient
from utils.endpoints import GET_REPORTS

class ReportManagementManager:

    @staticmethod
    def fetch_reported_articles():
        return HttpClient.authorized_request("GET", GET_REPORTS)

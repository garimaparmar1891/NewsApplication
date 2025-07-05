from utils.http_client import HttpClient
from utils.endpoints import GET_REPORTS

class ReportManagementService:
    """Handles fetching of reported articles from the server."""

    @staticmethod
    def get_reported_articles():
        response = HttpClient.authorized_request("GET", GET_REPORTS)
        if not response.ok:
            return None
        return response.json().get("data", []) 
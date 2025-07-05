from utils.http_client import HttpClient
from utils.endpoints import GET_NOTIFICATIONS

class NotificationViewerService:
    """Handles fetching user notifications (service layer)."""

    @staticmethod
    def fetch_notifications():
        return HttpClient.authorized_request("GET", GET_NOTIFICATIONS) 
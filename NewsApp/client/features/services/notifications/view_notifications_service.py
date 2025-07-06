from utils.http_client import HttpClient
from utils.endpoints import GET_NOTIFICATIONS

class NotificationViewerService:

    @staticmethod
    def fetch_notifications():
        return HttpClient.authorized_request("GET", GET_NOTIFICATIONS)

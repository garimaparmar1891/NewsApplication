from utils.http_client import HttpClient
from utils.response_handler import handle_data_response
from utils.endpoints import (
    GET_CATEGORIES,
    GET_NOTIFICATION_PREFERENCES,
    UPDATE_NOTIFICATION_PREFERENCES
)

class NotificationPreferencesService:

    @staticmethod
    def fetch_categories():
        return HttpClient.authorized_request("GET", GET_CATEGORIES)

    @staticmethod
    def fetch_preferences():
        return HttpClient.authorized_request("GET", GET_NOTIFICATION_PREFERENCES)

    @staticmethod
    def update_preferences(user_prefs):
        payload = {"categories": user_prefs}
        response = HttpClient.authorized_request("POST", UPDATE_NOTIFICATION_PREFERENCES, json=payload)
        return response

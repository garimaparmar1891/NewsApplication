from utils.http_client import HttpClient
from utils.endpoints import (
    GET_CATEGORIES,
    GET_NOTIFICATION_PREFERENCES,
    UPDATE_NOTIFICATION_PREFERENCES
)

class NotificationPreferencesService:
    @staticmethod
    def fetch_categories():
        resp = HttpClient.authorized_request("GET", GET_CATEGORIES)
        if not resp.ok:
            print("Failed to fetch categories:", resp.json().get("message"))
            return []
        return resp.json().get("data", [])

    @staticmethod
    def fetch_preferences():
        resp = HttpClient.authorized_request("GET", GET_NOTIFICATION_PREFERENCES)
        if not resp.ok:
            print("Failed to fetch preferences:", resp.json().get("message"))
            return []
        return resp.json().get("data", [])

    @staticmethod
    def update_preferences(user_prefs):
        payload = {"categories": user_prefs}
        resp = HttpClient.authorized_request("POST", UPDATE_NOTIFICATION_PREFERENCES, json=payload)
        if resp.ok:
            print("Preferences updated successfully.")
        else:
            print("Failed to update preferences:", resp.json().get("message", "Unknown error")) 
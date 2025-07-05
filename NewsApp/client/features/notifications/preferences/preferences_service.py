from utils.http_client import HttpClient
from utils.endpoints import UPDATE_NOTIFICATION_PREFERENCES

class PreferencesService:
    @staticmethod
    def send_update_preferences_request(category_id, is_enabled):
        preferences = {
            "preferences": [
                {"categoryId": category_id, "isEnabled": is_enabled}
            ]
        }
        return HttpClient.authorized_request("POST", UPDATE_NOTIFICATION_PREFERENCES, json=preferences) 
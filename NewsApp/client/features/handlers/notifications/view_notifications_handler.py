from utils.http_client import HttpClient
from utils.endpoints import GET_NOTIFICATIONS
from menu.paginated_menu import PaginatedMenu
from constants.messages import NO_NOTIFICATIONS_FOUND, NOTIFICATIONS_FETCH_SUCCESS, NOTIFICATIONS_FETCH_FAILED

class ViewNotificationsHandler:
    @staticmethod
    def view_notifications():
        try:
            response = HttpClient.authorized_request("GET", GET_NOTIFICATIONS)
            ViewNotificationsHandler._display_notifications(response)
        except Exception as e:
            print(NOTIFICATIONS_FETCH_FAILED.format(str(e)))

    @staticmethod
    def _display_notifications(response):
        try:
            if response.ok:
                notifications = response.json().get("data", [])
                if notifications:
                    print(NOTIFICATIONS_FETCH_SUCCESS)
                    PaginatedMenu(notifications, context_label="Notifications").show()

            else:
                print(NO_NOTIFICATIONS_FOUND)
        except Exception as e:
            print(NOTIFICATIONS_FETCH_FAILED.format(str(e)))

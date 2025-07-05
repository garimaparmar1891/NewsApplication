from .view_notifications_service import NotificationViewerService

class NotificationViewerManager:
    """Handles viewing user notifications (manager layer)."""

    @staticmethod
    def view_notifications():
        response = NotificationViewerService.fetch_notifications()
        NotificationViewerManager.print_notifications_status(response)

    @staticmethod
    def print_notifications_status(response):
        if response.ok:
            notifications = response.json().get("data", [])
            from utils.paginated_menu import PaginatedMenu
            PaginatedMenu(notifications, context_label="Notifications").show()
        else:
            print("Failed to fetch notifications.")
from features.notifications.view_notifications.view_notifications_manager import NotificationViewerManager
from features.notifications.configure_notifications.configure_notifications_manager import NotificationPreferencesManager
from utils.token_storage import TokenStorage

class NotificationMenu:
    """Handles the notification menu."""

    def show(self):
        while True:
            self.print_notification_menu()
            choice = input("Enter your option: ").strip()
            if not self.handle_notification_menu_choice(choice):
                break

    @staticmethod
    def print_notification_menu():
        print("\nN O T I F I C A T I O N S")
        print("\n1. View Notifications")
        print("2. Configure Notifications")
        print("3. Back")
        print("4. Logout")

    @staticmethod
    def handle_notification_menu_choice(choice):
        if choice == "1":
            NotificationViewerManager.view_notifications()
        elif choice == "2":
            NotificationPreferencesManager.configure_notifications()
        elif choice == "3":
            return False  # Back
        elif choice == "4":
            TokenStorage.clear_token()
            print("Logged out successfully.")
            exit()
        else:
            print("Invalid option")
        return True
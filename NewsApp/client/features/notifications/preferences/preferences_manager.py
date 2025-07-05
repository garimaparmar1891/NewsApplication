from .preferences_service import PreferencesService

class NotificationPreferencesManager:
    """Handles updating notification preferences for a category."""

    @staticmethod
    def update_preferences():
        print("\n--- Update Notification Preferences ---")
        category_id = NotificationPreferencesManager.prompt_category_id()
        if category_id is None:
            return
        is_enabled = NotificationPreferencesManager.prompt_is_enabled()
        if is_enabled is None:
            return
        response = PreferencesService.send_update_preferences_request(category_id, is_enabled)
        NotificationPreferencesManager.print_update_preferences_status(response)

    @staticmethod
    def prompt_category_id():
        try:
            return int(input("Enter Category ID: ").strip())
        except ValueError:
            print("Invalid input. Please enter numeric Category ID.")
            return None

    @staticmethod
    def prompt_is_enabled():
        is_enabled_input = input("Enable notifications for this category? (yes/no): ").strip().lower()
        if is_enabled_input not in ("yes", "no"):
            print("Invalid input. Please enter 'yes' or 'no'.")
            return None
        return is_enabled_input == "yes"

    @staticmethod
    def print_update_preferences_status(response):
        if response.ok:
            print("Preferences updated successfully.")
        else:
            print("Failed to update preferences:", response.json().get("message", response.text)) 
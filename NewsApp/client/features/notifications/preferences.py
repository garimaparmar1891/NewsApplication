from utils.http_client import authorized_request
from utils.endpoints import UPDATE_NOTIFICATION_PREFERENCES

def update_preferences():
    print("\n--- Update Notification Preferences ---")
    category_id = prompt_category_id()
    if category_id is None:
        return
    is_enabled = prompt_is_enabled()
    if is_enabled is None:
        return
    response = send_update_preferences_request(category_id, is_enabled)
    print_update_preferences_status(response)

def prompt_category_id():
    try:
        return int(input("Enter Category ID: ").strip())
    except ValueError:
        print("Invalid input. Please enter numeric Category ID.")
        return None

def prompt_is_enabled():
    is_enabled_input = input("Enable notifications for this category? (yes/no): ").strip().lower()
    if is_enabled_input not in ("yes", "no"):
        print("Invalid input. Please enter 'yes' or 'no'.")
        return None
    return is_enabled_input == "yes"

def send_update_preferences_request(category_id, is_enabled):
    preferences = {
        "preferences": [
            {"categoryId": category_id, "isEnabled": is_enabled}
        ]
    }
    return authorized_request("POST", UPDATE_NOTIFICATION_PREFERENCES, json=preferences)

def print_update_preferences_status(response):
    if response.ok:
        print("Preferences updated successfully.")
    else:
        print("Failed to update preferences:", response.json().get("message", response.text))

from utils.http_client import authorized_request

def update_preferences():
    print("\n--- Update Notification Preferences ---")
    try:
        category_id = int(input("Enter Category ID: ").strip())
        is_enabled_input = input("Enable notifications for this category? (yes/no): ").strip().lower()

        if is_enabled_input not in ("yes", "no"):
            print("Invalid input. Please enter 'yes' or 'no'.")
            return

        is_enabled = is_enabled_input == "yes"

        preferences = {
            "preferences": [
                {"categoryId": category_id, "isEnabled": is_enabled}
            ]
        }

        response = authorized_request("POST", "/api/notifications/preferences", json=preferences)

        if response.ok:
            print("Preferences updated successfully.")
        else:
            print("Failed to update preferences:", response.json().get("message", response.text))

    except ValueError:
        print("Invalid input. Please enter numeric Category ID.")

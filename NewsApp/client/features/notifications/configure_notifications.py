from utils.http_client import authorized_request
from utils.endpoints import (
    GET_CATEGORIES,
    GET_NOTIFICATION_PREFERENCES,
    UPDATE_NOTIFICATION_PREFERENCES
)

def configure_notifications():
    categories = fetch_categories()
    if not categories:
        print("No categories available.")
        return

    prefs = fetch_preferences()
    enabled_category_ids = {pref["categoryId"] for pref in prefs if pref.get("isEnabled", False)}
    category_map = {cat["id"]: cat["name"] for cat in categories}

    print_category_status(categories, enabled_category_ids)
    selected_ids = prompt_category_selection()
    if not selected_ids or selected_ids == ['']:
        print("No changes made.")
        return

    user_prefs = build_user_prefs(selected_ids, category_map, enabled_category_ids)
    if not user_prefs:
        print("No valid changes to update.")
        return

    update_preferences(user_prefs)

def fetch_categories():
    resp = authorized_request("GET", GET_CATEGORIES)
    if not resp.ok:
        print("Failed to fetch categories:", resp.json().get("message"))
        return []
    return resp.json().get("data", [])

def fetch_preferences():
    resp = authorized_request("GET", GET_NOTIFICATION_PREFERENCES)
    if not resp.ok:
        print("Failed to fetch preferences:", resp.json().get("message"))
        return []
    return resp.json().get("data", [])

def print_category_status(categories, enabled_category_ids):
    print("\n--- Your Notification Preferences ---")
    for cat in categories:
        status = "Enabled" if cat["id"] in enabled_category_ids else "Disabled"
        print(f"{cat['id']}. {cat['name']} - {status}")

def prompt_category_selection():
    print("\nEnter category IDs to toggle (e.g., 1 3 5), or press Enter to skip:")
    return input("Your selection: ").strip().split()

def prompt_keywords_for_category(category_name, is_enabling):
    action = "Enabling" if is_enabling else "Disabling"
    print(f"{action} '{category_name}'.")
    kw_input = input("Enter keywords for this category (comma separated, or leave blank): ").strip()
    if kw_input:
        return [kw.strip() for kw in kw_input.split(",") if kw.strip()]
    return []

def build_user_prefs(selected_ids, category_map, enabled_category_ids):
    user_prefs = []
    for cat_id_str in selected_ids:
        try:
            cat_id = int(cat_id_str)
            if cat_id not in category_map:
                print(f"Invalid category ID: {cat_id}")
                continue
            is_enabled = cat_id not in enabled_category_ids
            keywords = prompt_keywords_for_category(category_map[cat_id], is_enabled)
            user_prefs.append({
                "categoryId": cat_id,
                "isEnabled": is_enabled,
                "keywords": keywords
            })
        except ValueError:
            print(f"Invalid input: {cat_id_str} is not a valid number.")
    return user_prefs

def update_preferences(user_prefs):
    payload = {"categories": user_prefs}
    resp = authorized_request("POST", UPDATE_NOTIFICATION_PREFERENCES, json=payload)
    if resp.ok:
        print("Preferences updated successfully.")
    else:
        print("Failed to update preferences:", resp.json().get("message", "Unknown error"))

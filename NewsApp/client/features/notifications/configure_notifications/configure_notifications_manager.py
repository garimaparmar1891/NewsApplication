from .configure_notifications_service import NotificationPreferencesService

class NotificationPreferencesManager:
    """Handles configuration of notification preferences."""

    @staticmethod
    def configure_notifications():
        categories = NotificationPreferencesService.fetch_categories()
        if not categories:
            print("No categories available.")
            return

        prefs = NotificationPreferencesService.fetch_preferences()
        enabled_category_ids = {pref["categoryId"] for pref in prefs if pref.get("isEnabled", False)}
        category_map = {cat["id"]: cat["name"] for cat in categories}

        NotificationPreferencesManager.print_category_status(categories, enabled_category_ids)
        selected_ids = NotificationPreferencesManager.prompt_category_selection()
        if not selected_ids or selected_ids == ['']:
            print("No changes made.")
            return

        user_prefs = NotificationPreferencesManager.build_user_prefs(selected_ids, category_map, enabled_category_ids)
        if not user_prefs:
            print("No valid changes to update.")
            return

        NotificationPreferencesService.update_preferences(user_prefs)

    @staticmethod
    def print_category_status(categories, enabled_category_ids):
        print("\n--- Your Notification Preferences ---")
        for cat in categories:
            status = "Enabled" if cat["id"] in enabled_category_ids else "Disabled"
            print(f"{cat['id']}. {cat['name']} - {status}")

    @staticmethod
    def prompt_category_selection():
        print("\nEnter category IDs to toggle (e.g., 1 3 5), or press Enter to skip:")
        return input("Your selection: ").strip().split()

    @staticmethod
    def prompt_keywords_for_category(category_name, is_enabling):
        action = "Enabling" if is_enabling else "Disabling"
        print(f"{action} '{category_name}'.")
        kw_input = input("Enter keywords for this category (comma separated, or leave blank): ").strip()
        if kw_input:
            return [kw.strip() for kw in kw_input.split(",") if kw.strip()]
        return []

    @staticmethod
    def build_user_prefs(selected_ids, category_map, enabled_category_ids):
        user_prefs = []
        for cat_id_str in selected_ids:
            try:
                cat_id = int(cat_id_str)
                if cat_id not in category_map:
                    print(f"Invalid category ID: {cat_id}")
                    continue
                is_enabled = cat_id not in enabled_category_ids
                keywords = NotificationPreferencesManager.prompt_keywords_for_category(category_map[cat_id], is_enabled)
                user_prefs.append({
                    "categoryId": cat_id,
                    "isEnabled": is_enabled,
                    "keywords": keywords
                })
            except ValueError:
                print(f"Invalid input: {cat_id_str} is not a valid number.")
        return user_prefs 
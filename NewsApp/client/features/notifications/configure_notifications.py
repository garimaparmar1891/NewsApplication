from utils.http_client import authorized_request


def configure_notifications():
    categories_resp = authorized_request("GET", "/api/categories")
   
    if not categories_resp.ok:
        print("Failed to fetch categories:", categories_resp.json().get("message"))
        return

    categories = categories_resp.json().get("data", [])

    if not categories:
        print("No categories available.")
        return

    prefs_resp = authorized_request("GET", "/api/notifications/preferences")
    if not prefs_resp.ok:
        print("Failed to fetch preferences:", prefs_resp.json().get("message"))
        return

    prefs = prefs_resp.json().get("data", [])
    enabled_category_ids = {pref["categoryId"] for pref in prefs if pref.get("isEnabled", False)}


    category_map = {cat["id"]: cat["name"] for cat in categories}
    user_prefs = []

    print("\n--- Your Notification Preferences ---")
    for cat in categories:
        status = "Enabled" if cat["id"] in enabled_category_ids else "Disabled"
        print(f"{cat['id']}. {cat['name']} - {status}")

    print("\nEnter category IDs to toggle (e.g., 1 3 5), or press Enter to skip:")
    selected = input("Your selection: ").strip()

    if not selected:
        print("ℹNo changes made.")
        return

    selected_ids = selected.split()

    for cat_id_str in selected_ids:
        try:
            cat_id = int(cat_id_str)
            if cat_id not in category_map:
                print(f"Invalid category ID: {cat_id}")
                continue

            is_enabled = cat_id not in enabled_category_ids
            keywords = []

            if is_enabled:
                print(f"Enabling '{category_map[cat_id]}'.")
                kw_input = input("Enter keywords for this category (comma separated, or leave blank): ").strip()
                if kw_input:
                    keywords = [kw.strip() for kw in kw_input.split(",") if kw.strip()]

            else:
                print(f"Disabling '{category_map[cat_id]}'.")
                kw_input = input("Enter keywords for this category (comma separated, or leave blank): ").strip()
                if kw_input:
                    keywords = [kw.strip() for kw in kw_input.split(",") if kw.strip()]

            user_prefs.append({
                        "categoryId": cat_id,
                        "isEnabled": is_enabled,
                        "keywords": keywords
                    })


        except ValueError:
            print(f"Invalid input: {cat_id_str} is not a valid number.")

    if not user_prefs:
        print("No valid changes to update.")
        return

    payload = {
        "categories": user_prefs
    }

    update_resp = authorized_request("POST", "/api/notifications/preferences", json=payload)
    if update_resp.ok:
        print("Preferences updated successfully.")
    else:
        print("Failed to update preferences:", update_resp.json().get("message", "Unknown error"))

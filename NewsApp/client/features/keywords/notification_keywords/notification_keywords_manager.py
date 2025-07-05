from features.keywords.notification_keywords.notification_keywords_service import NotificationKeywordsService

class NotificationKeywordsManager:
    """Handles notification keyword management."""

    @staticmethod
    def add_notification_keyword():
        print("\n--- Add Notification Keyword ---")
        data = NotificationKeywordsManager.prompt_keyword_data()
        response = NotificationKeywordsService.add_notification_keyword(data)
        NotificationKeywordsManager.print_add_notification_keyword_status(response)

    @staticmethod
    def print_add_notification_keyword_status(response):
        if response.ok:
            print("Keyword added for notifications.")
        else:
            print("Failed to add keyword:", response.json().get("message", response.text))

    @staticmethod
    def view_notification_keywords():
        print("\n--- Notification Keywords ---")
        response = NotificationKeywordsService.view_notification_keywords()
        NotificationKeywordsManager.print_view_notification_keywords_status(response)

    @staticmethod
    def print_view_notification_keywords_status(response):
        if response.ok:
            keywords = response.json().get("data", [])
            if not keywords:
                print("No notification keywords set.")
            else:
                for idx, keyword in enumerate(keywords, 1):
                    print(f"[{idx}] Keyword: {keyword['Keyword']}, Category: {keyword.get('Category', 'All')}")
        else:
            print("Failed to fetch notification keywords:", response.json().get("message", response.text))

    @staticmethod
    def delete_notification_keyword():
        print("\n--- Delete Notification Keyword ---")
        keyword_id = input("Enter the ID of the keyword to delete: ").strip()
        response = NotificationKeywordsService.delete_notification_keyword(keyword_id)
        NotificationKeywordsManager.print_delete_notification_keyword_status(response)

    @staticmethod
    def print_delete_notification_keyword_status(response):
        if response.ok:
            print("Notification keyword deleted.")
        else:
            print("Failed to delete keyword:", response.json().get("message", response.text))

    @staticmethod
    def prompt_keyword_data():
        keyword = input("Enter keyword to be notified about: ").strip()
        category = input("Enter category (optional, press Enter to skip): ").strip()
        data = {"keyword": keyword}
        if category:
            data["category"] = category
        return data 
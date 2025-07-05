from .user_keywords_service import UserKeywordsService

class UserKeywordsManager:
    """Handles user keyword management."""

    @staticmethod
    def add_user_keyword():
        print("\n--- Add User Keyword ---")
        keyword = UserKeywordsManager.prompt_user_keyword()
        if not keyword:
            print("Keyword cannot be empty.")
            return
        response = UserKeywordsService.send_add_user_keyword_request(keyword)
        UserKeywordsManager.print_add_user_keyword_status(response)

    @staticmethod
    def prompt_user_keyword():
        return input("Enter a keyword to track: ").strip()

    @staticmethod
    def print_add_user_keyword_status(response):
        if response.ok:
            print("Keyword added successfully.")
        else:
            print("Failed to add keyword:", response.json().get("message", response.text))

    @staticmethod
    def view_user_keywords():
        print("\n--- Your Tracked Keywords ---")
        response = UserKeywordsService.send_view_user_keywords_request()
        UserKeywordsManager.print_view_user_keywords_status(response)

    @staticmethod
    def print_view_user_keywords_status(response):
        if response.ok:
            keywords = response.json().get("data", [])
            if not keywords:
                print("No keywords found.")
            else:
                for idx, keyword in enumerate(keywords, 1):
                    print(f"[{idx}] ID: {keyword['Id']} | Keyword: {keyword['Keyword']}")
        else:
            print("Failed to fetch keywords:", response.json().get("message", response.text))

    @staticmethod
    def delete_user_keyword():
        print("\n--- Delete User Keyword ---")
        keyword_id = UserKeywordsManager.prompt_keyword_id()
        if not keyword_id.isdigit():
            print("Invalid ID.")
            return
        response = UserKeywordsService.send_delete_user_keyword_request(keyword_id)
        UserKeywordsManager.print_delete_user_keyword_status(response)

    @staticmethod
    def prompt_keyword_id():
        return input("Enter the Keyword ID to delete: ").strip()

    @staticmethod
    def print_delete_user_keyword_status(response):
        if response.ok:
            print("Keyword deleted successfully.")
        else:
            print("Failed to delete keyword:", response.json().get("message", response.text)) 
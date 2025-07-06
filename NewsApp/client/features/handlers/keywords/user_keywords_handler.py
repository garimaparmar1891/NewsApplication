from features.services.keywords.user_keywords_service import UserKeywordsService
from features.services.categories.view_categories_service import CategoryService
from utils.response_handler import handle_data_response
from constants.messages import (
    USER_KEYWORDS_ADD_TITLE, USER_KEYWORDS_DELETE_TITLE, USER_KEYWORDS_KEYWORD_PROMPT,
    USER_KEYWORDS_DISPLAY_FORMAT, VIEW_KEYWORDS_TITLE, BLOCKED_KEYWORD_DELETE_PROMPT,
    BLOCKED_KEYWORD_EMPTY, BLOCKED_KEYWORD_INVALID_ID, KEYWORD_ADD_FAILED,
    KEYWORD_DELETE_FAILED, FETCH_KEYWORDS_FAILED
)

class UserKeywordsHandler:
    @staticmethod
    def add_user_keyword():
        print(USER_KEYWORDS_ADD_TITLE)
        
        categories = UserKeywordsHandler._get_categories()
        if not categories:
            print("Failed to fetch categories. Please try again.")
            return
            
        print("\nAvailable Categories:")
        for category in categories:
            if isinstance(category, dict) and 'Id' in category and 'Name' in category:
                print(f"{category['Id']}. {category['Name']}")
        
        category_id = UserKeywordsHandler._get_category_selection()
        if not category_id:
            return
            
        keyword = UserKeywordsHandler._get_keyword_input()
        if not keyword:
            print(BLOCKED_KEYWORD_EMPTY)
            return
            
        response = UserKeywordsService.add_user_keyword(keyword, category_id)
        UserKeywordsHandler._print_add_status(response)

    @staticmethod
    def _get_categories():
        response = CategoryService.fetch_categories()
        success, categories = handle_data_response(response, "Failed to fetch categories")
        
        if not success:
            print(f"Error: {categories}")
            return None
            
        if not categories or not isinstance(categories, list):
            print("No categories found")
            return None
            
        return categories

    @staticmethod
    def _get_category_selection():
        category_id = input("Enter category ID: ").strip()
        if not category_id:
            print("Category ID is required")
            return None
        try:
            return int(category_id)
        except ValueError:
            print("Invalid category ID. Please enter a number.")
            return None

    @staticmethod
    def view_user_keywords():
        print(f"\n{VIEW_KEYWORDS_TITLE}")
        response = UserKeywordsService.view_user_keywords()
        UserKeywordsHandler._print_view_status(response)

    @staticmethod
    def delete_user_keyword():
        print(USER_KEYWORDS_DELETE_TITLE)
        keyword_id = UserKeywordsHandler._get_keyword_id_input()
        if not keyword_id.isdigit():
            print(BLOCKED_KEYWORD_INVALID_ID)
            return
        response = UserKeywordsService.delete_user_keyword(keyword_id)
        UserKeywordsHandler._print_delete_status(response)

    @staticmethod
    def _get_keyword_input():
        return input(USER_KEYWORDS_KEYWORD_PROMPT).strip()

    @staticmethod
    def _get_keyword_id_input():
        return input(BLOCKED_KEYWORD_DELETE_PROMPT).strip()

    @staticmethod
    def _print_add_status(response):
        if response.ok:
            print("Keyword added successfully")
        else:
            error_msg = response.json().get("message", response.text)
            print(f"FAILED: {KEYWORD_ADD_FAILED}: {error_msg}")

    @staticmethod
    def _print_view_status(response):
        if response.ok:
            keywords = response.json().get("data", [])
            if not keywords:
                print("SUCCESS: No keywords found")
            else:
                if not UserKeywordsHandler._is_valid_keywords_format(keywords):
                    print(f"FAILED: {FETCH_KEYWORDS_FAILED}: Invalid data format.")
                    return
                UserKeywordsHandler._display_keywords(keywords)
        else:
            error_msg = response.json().get("message", response.text)
            print(f"FAILED: {FETCH_KEYWORDS_FAILED}: {error_msg}")

    @staticmethod
    def _print_delete_status(response):
        if response.ok:
            print("Keyword deleted successfully")
        else:
            error_msg = response.json().get("message", response.text)
            print(f"FAILED: {KEYWORD_DELETE_FAILED}: {error_msg}")

    @staticmethod
    def _is_valid_keywords_format(keywords):
        return isinstance(keywords, list) and all(isinstance(item, dict) for item in keywords)

    @staticmethod
    def _display_keywords(keywords):
        for idx, keyword in enumerate(keywords, 1):
            if isinstance(keyword, dict) and 'id' in keyword and 'keyword' in keyword:
                print(USER_KEYWORDS_DISPLAY_FORMAT.format(id=keyword['id'], keyword=keyword['keyword']))

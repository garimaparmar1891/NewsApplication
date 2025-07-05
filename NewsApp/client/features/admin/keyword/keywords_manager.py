from features.admin.keyword.keywords_service import KeywordsService
from features.admin.utils.input_helpers import InputHelpers
from features.admin.utils.print_helpers import PrintHelpers
from constants import messages as msg

class KeywordsManager:
    """Handles keyword add and delete operations."""

    @staticmethod
    def add_keyword():
        print(f"\n--- {msg.ADD_KEYWORD_TITLE} ---")
        response = KeywordsService.fetch_categories()
        if not response.ok:
            PrintHelpers.print_error(msg.FETCH_CATEGORIES_FAILED)
            return
        categories = response.json().get("data", [])
        if not categories:
            PrintHelpers.print_error(msg.NO_CATEGORIES_FOUND)
            return
        print("\nAvailable Categories:")
        for category in categories:
            print(f"  ID: {category['id']} | Name: {category['name']}")
        category_id = InputHelpers.get_non_empty_input(msg.ENTER_CATEGORY_ID_PROMPT)
        if not category_id.isdigit():
            PrintHelpers.print_error(msg.INVALID_CATEGORY_ID)
            return
        word = InputHelpers.get_non_empty_input(msg.ENTER_KEYWORD_ADD_PROMPT)
        response = KeywordsService.add_keyword(word, category_id)
        if response.ok:
            PrintHelpers.print_success(msg.KEYWORD_ADD_SUCCESS)
        else:
            PrintHelpers.print_error(response.json().get("error", msg.KEYWORD_ADD_FAILED))

    @staticmethod
    def delete_keyword():
        print(f"\n--- {msg.DELETE_KEYWORD_TITLE} ---")
        word = InputHelpers.get_non_empty_input(msg.ENTER_KEYWORD_DELETE_PROMPT)
        response = KeywordsService.delete_keyword(word)
        if response.ok:
            PrintHelpers.print_success(msg.KEYWORD_DELETE_SUCCESS)
        else:
            PrintHelpers.print_error(response.json().get("error", msg.KEYWORD_DELETE_FAILED))

    @staticmethod
    def view_keywords():
        print(f"\n--- {msg.VIEW_KEYWORDS_TITLE} ---")
        response = KeywordsService.fetch_keywords()
        if not response.ok:
            PrintHelpers.print_error(msg.FETCH_KEYWORDS_FAILED)
            return
        keywords = response.json().get("data", [])
        if not keywords:
            PrintHelpers.print_error(msg.NO_KEYWORDS_FOUND)
            return
        print("\nAvailable Keywords:")
        for idx, keyword in enumerate(keywords, 1):
            print(f"[{idx}] ID: {keyword['Id']} | Keyword: {keyword['Keyword']}") 
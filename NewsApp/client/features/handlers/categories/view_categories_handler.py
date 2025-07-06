from features.services.categories.view_categories_service import CategoryService
from utils.response_handler import handle_data_response
from constants import messages as msg

class ViewCategoriesHandler:

    @staticmethod
    def display_categories():
        try:
            success, data = ViewCategoriesHandler._fetch_categories()
            if not success:
                return None
            
            result = ViewCategoriesHandler._display_categories_list(data)
       
            return result
        except Exception:
            return None

    @staticmethod
    def _fetch_categories():
        try:
            response = CategoryService.fetch_categories()
            return handle_data_response(response, msg.CATEGORY_FETCH_FAILED)
        except Exception:
            return False, "Failed to fetch categories"

    @staticmethod
    def _display_categories_list(categories):
        try:
            if not categories:
                print(msg.CATEGORY_NO_CATEGORIES_FOUND)
                return None
            
            if not ViewCategoriesHandler._validate_categories_format(categories):
                return None
            
            result = ViewCategoriesHandler._build_categories_menu(categories)
            return result
        except Exception:
            return None

    @staticmethod
    def _validate_categories_format(categories):
        try:
            return isinstance(categories, list) and all(isinstance(item, dict) for item in categories)
        except Exception:
            return False

    @staticmethod
    def _build_categories_menu(categories):
        try:
            print(f"\n{msg.CATEGORY_AVAILABLE_TITLE}")
            print("1. All News")
            option_map = {1: "all"}
            
            for idx, category in enumerate(categories, start=2):
                if ViewCategoriesHandler._is_valid_category(category):
                    print(f"{idx}. {category['Name']}")
                    option_map[idx] = category['Id']
            
            return option_map
        except Exception:
            return None

    @staticmethod
    def _is_valid_category(category):
        try:
            return isinstance(category, dict) and 'Name' in category and 'Id' in category
        except Exception:
            return False

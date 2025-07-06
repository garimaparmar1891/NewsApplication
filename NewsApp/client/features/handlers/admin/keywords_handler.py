from features.services.admin.keywords_service import KeywordsService
from utils.response_handler import handle_response, handle_data_response
from utils.input_utils import get_non_empty_input, get_valid_integer_input
from constants import messages as msg

class KeywordsHandler:

    @staticmethod
    def add_keyword():
        print(f"\n--- {msg.ADD_KEYWORD_TITLE} ---")
        
        try:
            categories = KeywordsHandler._fetch_data(KeywordsService.fetch_categories, msg.FETCH_CATEGORIES_FAILED, msg.NO_CATEGORIES_FOUND)
            if not categories:
                return False, msg.NO_CATEGORIES_FOUND
            
            KeywordsHandler._display_categories(categories)
            category_id = get_valid_integer_input(msg.ENTER_CATEGORY_ID_PROMPT, [cat['id'] for cat in categories])
            word = get_non_empty_input(msg.ENTER_KEYWORD_ADD_PROMPT)
            
            response = KeywordsService.add_keyword(word, category_id)
            success, message = handle_response(response, msg.KEYWORD_ADD_SUCCESS, msg.KEYWORD_ADD_FAILED)
            
            print(message)
            return success, message
            
        except Exception as e:
            error_message = f"An error occurred while adding keyword: {str(e)}"
            print(error_message)
            return False, error_message

    @staticmethod
    def delete_keyword():
        print(f"\n--- {msg.DELETE_KEYWORD_TITLE} ---")
        
        try:
            word = get_non_empty_input(msg.ENTER_KEYWORD_DELETE_PROMPT)
            response = KeywordsService.delete_keyword(word)
            
            success, message = handle_response(response, msg.KEYWORD_DELETE_SUCCESS, msg.KEYWORD_DELETE_FAILED)
            
            print(message)
            return success, message
            
        except Exception as e:
            error_message = f"An error occurred while deleting keyword: {str(e)}"
            print(error_message)
            return False, error_message

    @staticmethod
    def view_keywords():
        print(f"\n--- {msg.VIEW_KEYWORDS_TITLE} ---")
        
        try:
            keywords = KeywordsHandler._fetch_data(KeywordsService.fetch_keywords, msg.FETCH_KEYWORDS_FAILED, msg.NO_KEYWORDS_FOUND)
            if not keywords:
                return False, msg.NO_KEYWORDS_FOUND
            
            KeywordsHandler._display_keywords(keywords)
            return True, keywords
            
        except Exception as e:
            error_message = f"An error occurred while viewing keywords: {str(e)}"
            print(error_message)
            return False, error_message

    @staticmethod
    def _fetch_data(api_call, error_msg, empty_msg):
        try:
            response = api_call()
            success, data = handle_data_response(response, error_msg)
            
            if not success or not data:
                print(data if not success else empty_msg)
                return None
            
            if not KeywordsHandler._is_valid_data(data):
                print(error_msg)
                return None
            
            return data
            
        except Exception as e:
            print(f"An error occurred while fetching data: {str(e)}")
            return None

    @staticmethod
    def _is_valid_data(data):
        return isinstance(data, list) and all(isinstance(item, dict) for item in data)

    @staticmethod
    def _display_categories(categories):
        print(f"\n{msg.CATEGORIES_AVAILABLE_TITLE}")
        for category in categories:
            if 'id' in category and 'name' in category:
                print(f"  ID: {category['id']} | Name: {category['name']}")

    @staticmethod
    def _display_keywords(keywords):
        print(f"\n{msg.KEYWORDS_AVAILABLE_TITLE}")
        for idx, keyword in enumerate(keywords, 1):
            if 'id' in keyword and 'word' in keyword:
                print(f"[{idx}] ID: {keyword['id']} | Keyword: {keyword['word']}")

from features.services.admin.blocked_keywords_service import BlockedKeywordsService
from utils.response_handler import handle_response, handle_data_response
from constants import messages as msg
from utils.input_utils import get_non_empty_input

class BlockedKeywordsHandler:

    @staticmethod
    def add_blocked_keyword():
        print("\n")
        try:
            keyword = get_non_empty_input(msg.ENTER_KEYWORD_PROMPT)
            success, message = BlockedKeywordsService.add_blocked_keyword(keyword)
            if success:
                print(msg.BLOCKED_KEYWORD_ADD_SUCCESS)
            else:
                print(msg.BLOCKED_KEYWORD_ADD_FAILED)

            return success, message
        except Exception as e:
            error_message = f"Error adding blocked keyword: {str(e)}"
            print("FAILED: " + error_message)
            return False, error_message

    @staticmethod
    def get_blocked_keywords():
        try:
            success, data = BlockedKeywordsService.get_blocked_keywords()
            
            if not success:
                print("FAILED: " + str(data))
                return False, data
            
            BlockedKeywordsHandler._print_blocked_keywords(data)
            return True, data
        except Exception as e:
            error_message = f"Error fetching blocked keywords: {str(e)}"
            print("FAILED: " + error_message)
            return False, error_message

    @staticmethod
    def delete_blocked_keyword():
        try:
            keyword_id = input("Enter the ID of the keyword to delete: ").strip()
            success, message = BlockedKeywordsService.delete_blocked_keyword(keyword_id)
            if success:
                print(msg.BLOCKED_KEYWORD_DELETE_SUCCESS)
            else:
                print(msg.BLOCKED_KEYWORD_DELETE_FAILED)
            return success, message
        except Exception as e:
            error_message = f"Error deleting blocked keyword: {str(e)}"
            print("FAILED: " + error_message)
            return False, error_message

    @staticmethod
    def _print_blocked_keywords(keywords):
        try:
            if not keywords:
                print("INFO: " + msg.BLOCKED_KEYWORD_LIST_EMPTY)
                return
                
            print("\n--- Blocked Keywords ---")
            for idx, keyword in enumerate(keywords, 1):
                if isinstance(keyword, dict):
                    keyword_id = keyword.get('Id', 'N/A')
                    keyword_text = keyword.get('Keyword', 'N/A')
                    print(f"[{idx}] ID: {keyword_id} | Keyword: {keyword_text}")
            print("-" * 30)
        except Exception as e:
            error_message = f"Error displaying blocked keywords: {str(e)}"
            print("FAILED: " + error_message)

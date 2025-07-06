from features.services.admin.blocked_keywords_service import BlockedKeywordsService
from utils.response_handler import handle_response, handle_data_response
from constants import messages as msg

class BlockedKeywordsHandler:

    @staticmethod
    def add_blocked_keyword(keyword):
        try:
            response = BlockedKeywordsService.add_blocked_keyword(keyword)
            success, message = handle_response(
                response,
                msg.BLOCKED_KEYWORD_SUCCESS.format(keyword=keyword),
                msg.BLOCKED_KEYWORD_BLOCK_FAILED
            )
            if success:
                print("SUCCESS: " + message)
            else:
                print("FAILED: " + message)
            return success, message
        except Exception as e:
            error_message = f"Error adding blocked keyword: {str(e)}"
            print("FAILED: " + error_message)
            return False, error_message

    @staticmethod
    def get_blocked_keywords():
        try:
            response = BlockedKeywordsService.get_blocked_keywords()
            success, data = handle_data_response(response, msg.BLOCKED_KEYWORD_FETCH_FAILED)
            
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
    def delete_blocked_keyword(keyword_id):
        try:
            response = BlockedKeywordsService.delete_blocked_keyword(keyword_id)
            success, message = handle_response(
                response,
                msg.BLOCKED_KEYWORD_DELETE_SUCCESS,
                msg.BLOCKED_KEYWORD_DELETE_FAILED
            )
            if success:
                print("SUCCESS: " + message)
            else:
                print("FAILED: " + message)
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
                    keyword_id = keyword.get('id', 'N/A')
                    keyword_text = keyword.get('keyword', 'N/A')
                    print(f"[{idx}] ID: {keyword_id} | Keyword: {keyword_text}")
            print("-" * 30)
        except Exception as e:
            error_message = f"Error displaying blocked keywords: {str(e)}"
            print("FAILED: " + error_message)

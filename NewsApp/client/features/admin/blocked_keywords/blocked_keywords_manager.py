"""Manager for blocked keywords feature (user interaction logic)."""
from .blocked_keywords_service import BlockedKeywordsService
from features.admin.utils.input_helpers import InputHelpers
from features.admin.utils.print_helpers import PrintHelpers
from constants import messages as msg

class BlockedKeywordsManager:
    """Handles blocked keywords management (user interaction only)."""

    @staticmethod
    def add_blocked_keyword():
        keyword = InputHelpers.get_blocked_keyword_input().strip()
        if not keyword:
            PrintHelpers.print_result_message(False, msg.BLOCKED_KEYWORD_EMPTY)
            return
        success, message = BlockedKeywordsService.add_blocked_keyword(keyword)
        PrintHelpers.print_result_message(success, message)

    @staticmethod
    def view_blocked_keywords():
        success, keywords_or_message = BlockedKeywordsService.get_blocked_keywords()
        if success:
            if not keywords_or_message:
                print(msg.BLOCKED_KEYWORD_LIST_EMPTY)
            else:
                PrintHelpers.print_blocked_keywords(keywords_or_message)
        else:
            PrintHelpers.print_result_message(False, keywords_or_message)
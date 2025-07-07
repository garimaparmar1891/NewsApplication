from features.handlers.admin.blocked_keywords_handler import BlockedKeywordsHandler
from menu.menu_constants import (BLOCKED_KEYWORDS_MENU_OPTIONS, 
RETURN_TO_MAIN_MENU, ADMIN_INVALID_CHOICE,
BLOCKED_KEYWORDS_MENU_TITLE, ADMIN_MENU_SELECT_PROMPT)

class BlockedKeywordsMenu:

    def __init__(self):
        self.menu_actions = {
            "1": BlockedKeywordsHandler.add_blocked_keyword,
            "2": BlockedKeywordsHandler.get_blocked_keywords,
            "3": BlockedKeywordsHandler.delete_blocked_keyword,
            "4": self._back_to_main_menu
        }

    def show(self):
        while True:
            print("\n")
            print(BLOCKED_KEYWORDS_MENU_TITLE)
            for option in BLOCKED_KEYWORDS_MENU_OPTIONS:
                print(option)

            choice = input(ADMIN_MENU_SELECT_PROMPT).strip()

            if choice in self.menu_actions:
                self.menu_actions[choice]()
                if choice == "4":
                    break
            else:
                print(ADMIN_INVALID_CHOICE)

    def _back_to_main_menu(self):
        print(RETURN_TO_MAIN_MENU)

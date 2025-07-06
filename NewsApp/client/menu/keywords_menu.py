from features.handlers.admin.keywords_handler import KeywordsHandler
from menu.menu_constants import (
    KEYWORDS_MENU_OPTIONS, ADMIN_MENU_SELECT_PROMPT, 
    ADMIN_INVALID_CHOICE, RETURN_TO_MAIN_MENU
)

class KeywordsMenu:

    def show(self):
        actions = {
            "1": KeywordsHandler.add_keyword,
            "2": KeywordsHandler.delete_keyword,
            "3": KeywordsHandler.view_keywords,
            "4": self._return_to_main_menu
        }
        
        while True:
            for option in KEYWORDS_MENU_OPTIONS:
                print(option)
            choice = input(ADMIN_MENU_SELECT_PROMPT).strip()
            
            if choice == "4":
                actions[choice]()
                break
            action = actions.get(choice)
            if action:
                action()
            else:
                print(ADMIN_INVALID_CHOICE)

    @staticmethod
    def _return_to_main_menu():
        print(RETURN_TO_MAIN_MENU)

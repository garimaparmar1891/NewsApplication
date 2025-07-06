from features.handlers.keywords.user_keywords_handler import UserKeywordsHandler
from constants.messages import USER_KEYWORDS_MANAGEMENT_TITLE
from .menu_constants import (
    USER_KEYWORDS_MENU_OPTIONS, USER_KEYWORDS_MENU_SELECT_PROMPT, 
    USER_KEYWORDS_MENU_INVALID_CHOICE, RETURN_TO_MAIN_MENU
)

class UserKeywordsMenu:

    def show(self):
        actions = {
            "1": UserKeywordsHandler.add_user_keyword,
            "2": UserKeywordsHandler.view_user_keywords,
            "3": UserKeywordsHandler.delete_user_keyword,
            "4": self._return_to_main_menu
        }
        while True:
            print(USER_KEYWORDS_MANAGEMENT_TITLE)
            for option in USER_KEYWORDS_MENU_OPTIONS:
                print(option)
            choice = input(USER_KEYWORDS_MENU_SELECT_PROMPT).strip()
            if choice == "4":
                actions[choice]()
                break
            action = actions.get(choice)
            if action:
                action()
            else:
                print(USER_KEYWORDS_MENU_INVALID_CHOICE)

    @staticmethod
    def _return_to_main_menu():
        print(RETURN_TO_MAIN_MENU)

from menu.headlines_menu import HeadlinesMenu
from features.handlers.saved_articles.saved_articles_handler import SavedArticlesHandler
from features.handlers.articles.search_handler import SearchHandler
from menu.notification_menu import NotificationMenu
from utils.header import HeaderUtils
from utils.token_storage import TokenStorage
from menu.menu_constants import (
    USER_MENU_OPTIONS, USER_MENU_TITLE, USER_MENU_SELECT_PROMPT, 
    USER_MENU_LOGOUT_SUCCESS, USER_MENU_INVALID_CHOICE
)

class UserMenu:

    def __init__(self):
        self.menu_actions = {
            "1": lambda: HeadlinesMenu().show(),
            "2": SavedArticlesHandler.view_saved_articles,
            "3": SearchHandler.search_articles,
            "4": lambda: NotificationMenu().show()
        }

    def show(self):
        while True:
            HeaderUtils.print_welcome_message()
            print(USER_MENU_TITLE)
            for option in USER_MENU_OPTIONS:
                print(option)
            choice = input(USER_MENU_SELECT_PROMPT).strip()

            if choice == "5":
                TokenStorage.save_token(None)
                print(USER_MENU_LOGOUT_SUCCESS)
                break
            elif choice in self.menu_actions:
                self.menu_actions[choice]()
            else:
                print(USER_MENU_INVALID_CHOICE)

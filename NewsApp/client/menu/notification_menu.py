from menu.menu_constants import (
    NOTIFICATION_MENU_TITLE, 
    NOTIFICATION_MENU_OPTIONS, 
    NOTIFICATION_MENU_SELECT_PROMPT, 
    NOTIFICATION_MENU_INVALID_CHOICE, 
    NOTIFICATION_MENU_LOGOUT_SUCCESS,
    RETURN_TO_MAIN_MENU
)
from features.handlers.notifications.view_notifications_handler import ViewNotificationsHandler
from features.handlers.notifications.configure_notifications_handler import ConfigureNotificationsHandler
from menu.user_keywords_menu import UserKeywordsMenu
from utils.token_storage import TokenStorage

class NotificationMenu:

    def show(self):
        actions = {
            "1": ViewNotificationsHandler.view_notifications,
            "2": ConfigureNotificationsHandler.configure_notifications,
            "3": self._show_keywords_menu,
            "4": self._return_to_main_menu,
            "5": self._logout
        }
        
        while True:
            print("\n")
            print(NOTIFICATION_MENU_TITLE)
            for option in NOTIFICATION_MENU_OPTIONS:
                print(option)
            print("\n")
            choice = input(NOTIFICATION_MENU_SELECT_PROMPT).strip()

            if choice == "4":
                actions[choice]()
                break
            elif choice == "5":
                actions[choice]()
                exit()
            
            action = actions.get(choice)
            if action:
                action()
            else:
                print(NOTIFICATION_MENU_INVALID_CHOICE)

    @staticmethod
    def _show_keywords_menu():
        user_keywords_menu = UserKeywordsMenu()
        user_keywords_menu.show()

    @staticmethod
    def _return_to_main_menu():
        print(RETURN_TO_MAIN_MENU)

    @staticmethod
    def _logout():
        TokenStorage.clear_token()
        print(NOTIFICATION_MENU_LOGOUT_SUCCESS)

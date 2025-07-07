from features.handlers.auth.login_handler import LoginHandler
from features.handlers.auth.signup_handler import SignupHandler
from menu.admin_menu import AdminMenu
from menu.user_menu import UserMenu
from utils.token_storage import TokenStorage
from menu.menu_constants import (
    MAIN_MENU_OPTIONS, MAIN_MENU_SELECT_PROMPT, MAIN_MENU_LOGIN_PROMPT, 
    MAIN_MENU_EXIT_MESSAGE, MAIN_MENU_INVALID_CHOICE
)

class MainMenu:
    def __init__(self):
        self.login_handler = LoginHandler()
        self.signup_handler = SignupHandler()
        self.admin_menu = AdminMenu()
        self.user_menu = UserMenu()
        self.token_storage = TokenStorage()

    def show(self):
        while True:
            for option in MAIN_MENU_OPTIONS:
                print(option)
            choice = input(MAIN_MENU_SELECT_PROMPT)

            if choice == "1":
                role = self.login_handler.login()
                if role:
                    if role == "admin":
                        self.admin_menu.show()
                    else:
                        self.user_menu.show()
            elif choice == "2":
                self.signup_handler.signup()

                print(MAIN_MENU_LOGIN_PROMPT)
            elif choice == "3":
                print(MAIN_MENU_EXIT_MESSAGE)
                break
            else:
                print(MAIN_MENU_INVALID_CHOICE)

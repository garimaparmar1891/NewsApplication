from features.auth.login.login_manager import LoginManager
from features.auth.signup.signup_manager import SignupManager
from menu.admin_menu import AdminMenu
from menu.user_menu import UserMenu
from utils.token_storage import TokenStorage
from menu.menu_constants import MAIN_MENU_OPTIONS

class MainMenu:
    """Main menu for the application."""
    def __init__(self):
        self.login = LoginManager()
        self.signup = SignupManager()
        self.admin_menu = AdminMenu()
        self.user_menu = UserMenu()
        self.token_storage = TokenStorage()

    def show(self):
        while True:
            for option in MAIN_MENU_OPTIONS:
                print(option)
            choice = input("Select an option: ")

            if choice == "1":
                role = self.login.login()
                if self.token_storage.get_token():
                    if role == "admin":
                        self.admin_menu.show()
                    else:
                        self.user_menu.show()
            elif choice == "2":
                self.signup.signup()
                print("\nPlease login to continue.")
            elif choice == "3":
                print("Exiting. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
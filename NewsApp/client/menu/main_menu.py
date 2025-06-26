from features.auth.login import login
from features.auth.signup import signup
from menu.admin_menu import show_admin_menu
from menu.user_menu import show_user_menu
from utils.token_storage import get_token
from menu.menu_constants import MAIN_MENU_OPTIONS
def show_main_menu():
    while True:
        for option in MAIN_MENU_OPTIONS:
            print(option)
        choice = input("Select an option: ")

        if choice == "1":
            role = login()
            if get_token():
                if role == "admin":
                    show_admin_menu()
                else:
                    show_user_menu()
        elif choice == "2":
            signup()
            print("\nPlease login to continue.")
        elif choice == "3":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

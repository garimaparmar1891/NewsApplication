from features.auth.login import login
from features.auth.signup import signup
from menu.admin_menu import show_admin_menu
from utils.token_storage import get_token
from utils.header import print_welcome_message

def show_main_menu():
    while True:
        print("\n=== News Aggregator ===")
        print("1. Login")
        print("2. Signup")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            role = login()

            if get_token() and role:
                if role == "admin":
                    show_admin_menu()
                else:
                    print("welcome")
                    break
            else:
                print("Login failed. Please try again.")

        elif choice == "2":
            signup()
            print("\nPlease login to continue.")
        elif choice == "3":
            print("Exiting!")
            break
        else:
            print("Invalid choice. Please try again.")

from features.auth.login import login
from features.auth.signup import signup
from menu.admin_menu import show_admin_menu
from features.articles.headlines_menu import show_headlines_menu
from features.notifications.view_notifications import view_notifications
from features.saved_articles.view_saved_articles import view_saved_articles_paginated 
from features.articles.search import search_articles
from utils.token_storage import get_token, save_token
from utils.header import print_welcome_message
from features.notifications.menu import notification_menu
def show_main_menu():
    while True:
        print("\n=== News Aggregator ===")
        print("1. Login")
        print("2. Signup")
        print("3. Exit")
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


def show_user_menu():
    while True:
        print_welcome_message()
        print("\n=== User Menu ===")
        print("1. Headlines")
        print("2. Saved Article")
        print("3. Search Articles")
        print("4. View Notifications")
        print("5. Logout")
        choice = input("Select an option: ")

        if choice == "1":
            show_headlines_menu()
        elif choice == "2":
            view_saved_articles_paginated()
        elif choice == "3":
            search_articles()
        elif choice == "4":
            notification_menu()
        elif choice == "5":
            save_token(None)
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice. Please try again.")

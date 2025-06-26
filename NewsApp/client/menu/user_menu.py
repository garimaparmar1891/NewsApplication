from utils.header import print_welcome_message
from features.articles.headlines_menu import show_headlines_menu
from features.saved_articles.view_saved_articles import view_saved_articles_paginated
from features.articles.search import search_articles
from features.notifications.menu import notification_menu
from utils.token_storage import save_token
from menu.menu_constants import USER_MENU_OPTIONS
def show_user_menu():
    while True:
        print_welcome_message()
        print("\n=== User Menu ===")
        for option in USER_MENU_OPTIONS:
            print(option)
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

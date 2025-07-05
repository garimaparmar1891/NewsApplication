from utils.header import HeaderUtils
from menu.headlines_menu import HeadlinesMenu
from features.saved_articles.view_saved_articles.view_saved_articles_manager import SavedArticlesManager
from features.articles.search.search_manager import SearchManager
from menu.notification_menu import NotificationMenu
from utils.token_storage import TokenStorage
from menu.menu_constants import USER_MENU_OPTIONS

class UserMenu:
    """User menu for user-specific actions."""

    def show(self):
        while True:
            HeaderUtils.print_welcome_message()
            print("\n=== User Menu ===")
            for option in USER_MENU_OPTIONS:
                print(option)
            choice = input("Select an option: ")

            if choice == "1":
                HeadlinesMenu().show()
            elif choice == "2":
                SavedArticlesManager.view_saved_articles_paginated()
            elif choice == "3":
                SearchManager.search_articles()
            elif choice == "4":
                NotificationMenu().show()
            elif choice == "5":
                TokenStorage.save_token(None)
                print("Logged out successfully.")
                break
            else:
                print("Invalid choice. Please try again.")
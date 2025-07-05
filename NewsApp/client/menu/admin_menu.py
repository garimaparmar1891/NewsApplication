from menu.menu_constants import ADMIN_MENU_OPTIONS
from features.admin.external_server.external_servers_manager import ExternalServersManager
from features.admin.categories.categories_manager import CategoryManager
from features.admin.report_management.report_management_manager import ReportManagementManager
from features.admin.blocked_keywords.blocked_keywords_manager import BlockedKeywordsManager
from constants import messages as msg
from menu.keywords_menu import KeywordsMenu

class AdminMenu:
    """Admin menu for admin-specific actions."""

    def __init__(self):
        self.menu_actions = {
            "1": ExternalServersManager.view_all_external_servers,
            "2": ExternalServersManager.view_external_server_details,
            "3": ExternalServersManager.update_external_server,
            "4": CategoryManager.add_news_category,
            "5": ReportManagementManager.view_reported_articles,
            "6": lambda: KeywordsMenu().show(),
            "7": CategoryManager.hide_unhide_article,
            "8": CategoryManager.hide_unhide_category,
            "9": BlockedKeywordsManager.add_blocked_keyword,
            "10": BlockedKeywordsManager.view_blocked_keywords
        }

    def show(self):
        while True:
            print("\n=== Admin Menu ===")
            for option in ADMIN_MENU_OPTIONS:
                print(option)

            choice = input("Select an option: ").strip()

            if choice == "11":
                print(msg.ADMIN_LOGOUT_SUCCESS)
                break
            elif choice in self.menu_actions:
                self.menu_actions[choice]()
            else:
                print(msg.ADMIN_INVALID_CHOICE)
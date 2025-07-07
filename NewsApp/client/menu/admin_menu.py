from menu.menu_constants import ADMIN_MENU_OPTIONS, ADMIN_MENU_TITLE, ADMIN_MENU_SELECT_PROMPT, ADMIN_INVALID_CHOICE, ADMIN_LOGOUT_SUCCESS
from features.handlers.admin.external_server_handler import ExternalServerHandler
from features.handlers.admin.categories_handler import CategoryHandler
from features.handlers.admin.report_management_handler import ReportManagementHandler
from menu.keywords_menu import KeywordsMenu
from menu.blocked_keywords_menu import BlockedKeywordsMenu

class AdminMenu:

    def __init__(self):
        self.menu_actions = {
            "1": ExternalServerHandler.view_all_external_servers,
            "2": ExternalServerHandler.view_external_server_details,
            "3": ExternalServerHandler.update_external_server,
            "4": CategoryHandler.add_news_category,
            "5": ReportManagementHandler.view_reported_articles,
            "6": lambda: KeywordsMenu().show(),
            "7": CategoryHandler.hide_unhide_article,
            "8": CategoryHandler.hide_unhide_category,
            "9": lambda: BlockedKeywordsMenu().show()
        }

    def show(self):
        while True:
            print(ADMIN_MENU_TITLE)
            for option in ADMIN_MENU_OPTIONS:
                print(option)

            choice = input(ADMIN_MENU_SELECT_PROMPT).strip()

            if choice == "10":
                print(ADMIN_LOGOUT_SUCCESS)
                print("\n")
                break
            elif choice in self.menu_actions:
                self.menu_actions[choice]()
            else:
                print(ADMIN_INVALID_CHOICE)

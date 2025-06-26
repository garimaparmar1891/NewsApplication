from menu.menu_constants import ADMIN_MENU_OPTIONS
from features.admin.external_servers import (
    view_all_external_servers,
    view_external_server_details,
    update_external_server,
)
from features.admin.categories import add_news_category
from features.admin.moderation import (
    view_reported_articles,
    hide_unhide_article,
    hide_unhide_category,
)
from features.admin.blocked_keywords import (
    add_blocked_keyword,
    view_blocked_keywords,
)

def show_admin_menu():
    while True:
        print("\n=== Admin Menu ===")
        for option in ADMIN_MENU_OPTIONS:
            print(option)

        choice = input("Select an option: ").strip()

        if choice == "1":
            view_all_external_servers()
        elif choice == "2":
            view_external_server_details()
        elif choice == "3":
            update_external_server()
        elif choice == "4":
            add_news_category()
        elif choice == "5":
            view_reported_articles()
        elif choice == "6":
            hide_unhide_article()
        elif choice == "7":
            hide_unhide_category()
        elif choice == "8":
            add_blocked_keyword()
        elif choice == "9":
            view_blocked_keywords()
        elif choice == "10":
            print("Admin logged out successfully.")
            break
        else:
            print("Invalid choice. Please try again.")

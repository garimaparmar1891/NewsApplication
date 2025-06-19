from features.admin.external_servers import (
    view_all_external_servers,
    view_external_server_details,
    update_external_server,
)
from features.admin.categories import add_news_category

def show_admin_menu():
    while True:
        print("\n=== Admin Menu ===")
        print("1. View the list of external servers and status")
        print("2. View the external server’s details")
        print("3. Update/Edit the external server’s details")
        print("4. Add new News Category")
        print("5. Logout")

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
            print("Admin logged out successfully.")
            break
        else:
            print("Invalid choice. Please try again.")

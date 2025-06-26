from features.notifications.view_notifications import view_notifications
from features.notifications.configure_notifications import configure_notifications
from utils.token_storage import clear_token


def notification_menu():
    while True:
        print_notification_menu()
        choice = input("Enter your option: ").strip()
        if not handle_notification_menu_choice(choice):
            break

def print_notification_menu():
    print("\nN O T I F I C A T I O N S")
    print("\n1. View Notifications")
    print("2. Configure Notifications")
    print("3. Back")
    print("4. Logout")

def handle_notification_menu_choice(choice):
    if choice == "1":
        view_notifications()
    elif choice == "2":
        configure_notifications()
    elif choice == "3":
        return False  # Back
    elif choice == "4":
        clear_token()
        print("Logged out successfully.")
        exit()
    else:
        print("Invalid option")
    return True

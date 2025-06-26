from features.articles.today_headlines import get_today_headlines
from features.articles.articles_by_range import get_articles_by_range
from features.categories.view_categories import display_categories

def show_headlines_menu():
    actions = {
        "1": get_today_headlines,
        "2": lambda: (display_categories(), get_articles_by_range()),
        "3": lambda: print("Returning to main menu...")
    }
    while True:
        print_headlines_menu()
        choice = input("Select an option: ").strip()
        if choice == "3":
            actions[choice]()
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Please try again.")

def print_headlines_menu():
    print("\n=== Headlines Menu ===")
    print("1. View Today's Headlines")
    print("2. View Articles by Date Range and Category")
    print("3. Back to Main Menu")

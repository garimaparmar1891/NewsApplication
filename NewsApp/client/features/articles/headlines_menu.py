from features.articles.today_headlines import get_today_headlines
from features.articles.articles_by_range import get_articles_by_range
from features.categories.view_categories import display_categories

def show_headlines_menu():
    while True:
        print("\n=== Headlines Menu ===")
        print("1. View Today's Headlines")
        print("2. View Articles by Date Range and Category")
        print("3. Back")

        choice = input("Select an option: ")

        if choice == "1":
            get_today_headlines()

        elif choice == "2":
            display_categories()
            try:
                get_articles_by_range()
            except ValueError:
                print("Invalid input. Please try again.")

        elif choice == "3":
            break

        else:
            print("Invalid choice. Please try again.")

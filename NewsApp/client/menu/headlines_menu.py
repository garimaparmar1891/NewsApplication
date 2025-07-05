from features.articles.today_headlines.today_headlines_manager import TodayHeadlinesManager
from features.articles.articles_by_range.articles_by_range_manager import ArticlesByRangeManager
from features.categories.view_categories.view_categories_manager import CategoryManager

class HeadlinesMenu:
    """Handles the headlines menu for articles."""

    def show(self):
        actions = {
            "1": TodayHeadlinesManager.show_today_headlines,
            "2": self._view_articles_by_range_and_category,
            "3": self._return_to_main_menu
        }
        while True:
            self.print_headlines_menu()
            choice = input("Select an option: ").strip()
            if choice == "3":
                actions[choice]()
                break
            action = actions.get(choice)
            if action:
                action()
            else:
                print("Invalid choice. Please try again.")

    @staticmethod
    def print_headlines_menu():
        print("\n=== Headlines Menu ===")
        print("1. View Today's Headlines")
        print("2. View Articles by Date Range and Category")
        print("3. Back to Main Menu")

    @staticmethod
    def _view_articles_by_range_and_category():
        option_map = CategoryManager.display_categories()
        if not option_map:
            return
        try:
            choice = int(input("Select a category: ").strip())
        except ValueError:
            print("Invalid input. Please enter a number.")
            return
        selected = option_map.get(choice)
        if not selected:
            print("Invalid choice. Please try again.")
            return
        if selected == "all":
            ArticlesByRangeManager.get_all_articles()
        else:
            ArticlesByRangeManager.get_articles_by_range(selected)

    @staticmethod
    def _return_to_main_menu():
        print("Returning to main menu...")
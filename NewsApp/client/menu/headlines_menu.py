from features.handlers.articles.today_headlines_handler import TodayHeadlinesHandler
from features.handlers.articles.articles_by_range_handler import ArticlesByRangeHandler
from features.handlers.categories.view_categories_handler import ViewCategoriesHandler
from constants import messages as msg
from utils.input_utils import get_non_empty_input
from .menu_constants import (
    HEADLINES_MENU_OPTIONS, HEADLINES_MENU_SELECT_PROMPT, RETURN_TO_MAIN_MENU, 
    HEADLINES_MENU_INVALID_CHOICE
)

class HeadlinesMenu:

    def show(self):
        actions = {
            "1": TodayHeadlinesHandler.get_today_headlines,
            "2": self._get_articles_by_range,
            "3": self._return_to_main_menu
        }
        while True:
            print("\n")
            for option in HEADLINES_MENU_OPTIONS:
                print(option)
            print("\n")
            choice = input(HEADLINES_MENU_SELECT_PROMPT).strip()
            if choice == "3":
                actions[choice]()
                break
            action = actions.get(choice)
            if action:
                action()
            else:
                print(HEADLINES_MENU_INVALID_CHOICE)

    @staticmethod
    def _get_articles_by_range():
        success, categories_data = ViewCategoriesHandler._fetch_categories()
        if success and categories_data:
            print("\nAvailable Categories:")
            for category in categories_data:
                if isinstance(category, dict) and 'Id' in category and 'Name' in category:
                    print(f"ID: {category['Id']} - {category['Name']}")
        start_date = get_non_empty_input(msg.ENTER_START_DATE_PROMPT)
        end_date = get_non_empty_input(msg.ENTER_END_DATE_PROMPT)
        cat = input("Enter category: ").strip()
        categories = [cat] if cat else None
        ArticlesByRangeHandler.get_articles_by_range(start_date, end_date, categories)

    @staticmethod
    def _return_to_main_menu():
        print(RETURN_TO_MAIN_MENU)

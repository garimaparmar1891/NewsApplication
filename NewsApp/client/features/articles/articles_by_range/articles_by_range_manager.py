from utils.paginated_menu import PaginatedMenu
from utils.date_validator import DateValidator
from .articles_by_range_service import ArticlesByRangeService

class ArticlesByRangeManager:
    @staticmethod
    def get_all_articles():
        print("\n--- Fetching All News ---")
        articles, error = ArticlesByRangeService.fetch_all_articles()
        if error:
            print(error)
            return
        ArticlesByRangeManager.display_articles(articles, None, None)

    @staticmethod
    def get_articles_by_range(category=None):
        print("\n--- Fetch Articles by Date Range ---")
        if category is None:
            category = input("Optional Category (press Enter to skip): ").strip()
        start, end = DateValidator.validate_date_range_input()
        if not start or not end:
            print("Invalid date range. Operation cancelled.")
            return
        articles, error = ArticlesByRangeService.fetch_articles_by_range(start, end, category)
        if error:
            print(error)
            return
        ArticlesByRangeManager.display_articles(articles, start, end)

    @staticmethod
    def display_articles(articles, start, end):
        if not articles:
            print("ℹ No articles found for the given range.")
            return
        PaginatedMenu(articles, context_label=f"Articles from {start} to {end}").show() 
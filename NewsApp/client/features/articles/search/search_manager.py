from .search_service import SearchService
from utils.paginated_menu import PaginatedMenu

class SearchManager:
    @staticmethod
    def search_articles():
        print("\n--- Search Articles ---")
        q, start_date, end_date = SearchManager.prompt_search_criteria()
        params = {"q": q, "start_date": start_date, "end_date": end_date}
        articles = SearchService.fetch_articles(params)
        if articles is not None:
            SearchManager.display_search_results(articles, q)

    @staticmethod
    def prompt_search_criteria():
        q = input("Enter keyword: ").strip()
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()
        return q, start_date, end_date

    @staticmethod
    def display_search_results(articles, keyword):
        if not articles:
            print("No articles found for the given criteria.")
            return
        PaginatedMenu(articles, context_label=f"Search Results for '{keyword}'").show() 
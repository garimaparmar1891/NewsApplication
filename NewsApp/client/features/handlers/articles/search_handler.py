from constants import messages as msg
from features.services.articles.search_service import SearchService
from utils.input_utils import get_search_input
from menu.paginated_menu import PaginatedMenu
from utils.response_handler import handle_search_response


class SearchHandler:

    @staticmethod
    def search_articles():
        print(msg.SEARCH_TITLE)
        try:
            query, start_date, end_date = get_search_input()
            params = {"q": query, "start_date": start_date, "end_date": end_date}
            
            response = SearchService.fetch_articles(params)
            success, articles = handle_search_response(response, msg.SEARCH_FAILED)
            
            if success:
                SearchHandler._display_results(articles, query)
            else:
                print(articles)
                
        except Exception as e:
            pass

    @staticmethod
    def _display_results(articles, keyword):
        if not articles:
            print(msg.SEARCH_NO_RESULTS)
            return
        context_label = f"Search Results for '{keyword}'"
        PaginatedMenu(articles, context_label=context_label).show()

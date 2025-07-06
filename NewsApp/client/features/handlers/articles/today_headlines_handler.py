from constants import messages as msg
from features.services.articles.today_headlines_service import TodayHeadlinesService
from utils.response_handler import handle_data_response
from menu.paginated_menu import PaginatedMenu

class TodayHeadlinesHandler:

    @staticmethod
    def get_today_headlines():
        try:
            articles = TodayHeadlinesHandler._fetch_articles()
            if not articles:
                return
            
            TodayHeadlinesHandler._display_articles(articles)
        except Exception as e:
            print(f"Failed to get today's headlines: {str(e)}")

    @staticmethod
    def _fetch_articles():
        try:
            response = TodayHeadlinesService.fetch_today_headlines()
            success, articles = handle_data_response(response, msg.TODAY_HEADLINES_FETCH_FAILED)
            
            if not success:
                print(articles)
                return None
                
            if not articles:
                print("No headlines found for today.")
                return None
            
            return articles
        except Exception as e:
            print(f"Error occurred while fetching articles: {str(e)}")
            return None

    @staticmethod
    def _display_articles(articles):
        try:
            PaginatedMenu(
                articles, 
                context_label="Today's Headlines"
            ).show()
        except Exception as e:
            print(f"Error occurred while displaying articles: {str(e)}")

from features.services.saved_articles.view_saved_articles_service import SavedArticlesService
from utils.response_handler import handle_data_response
from menu.paginated_menu import PaginatedMenu
from constants import messages as msg


class SavedArticlesHandler:

    @staticmethod
    def view_saved_articles():
        try:
            articles = SavedArticlesHandler._fetch_articles()
            if not articles:
                return
            
            SavedArticlesHandler._display_articles(articles)
        except Exception as e:
            print(str(e))

    @staticmethod
    def _fetch_articles():
        try:
            response = SavedArticlesService.fetch_saved_articles()
            success, articles = handle_data_response(response, msg.SAVED_ARTICLES_FETCH_FAILED)
            
            if not success:
                print(articles)
                return None
                
            if not articles:
                print("No saved articles found")
                return None
            
            return articles
        except Exception as e:
            print(f"Error occurred while fetching saved articles: {str(e)}")
            return None

    @staticmethod
    def _display_articles(articles):
        try:
            refresh_callback = SavedArticlesHandler._create_refresh_callback()
            PaginatedMenu(
                articles, 
                context_label="Saved Articles", 
                is_saved_articles=True, 
                refresh_callback=refresh_callback
            ).show()
        except Exception as e:
            print(f"Failed to display saved articles: {str(e)}")

    @staticmethod
    def _create_refresh_callback():
        def refresh_saved_articles():
            try:
                response = SavedArticlesService.fetch_saved_articles()
                success, articles = handle_data_response(response, msg.SAVED_ARTICLES_FETCH_FAILED)
                if not success:
                    print(f"Failed to refresh saved articles: {articles}")
                    return []
                return articles or []
            except Exception as e:
                print(f"Error occurred while refreshing saved articles: {str(e)}")
                return []
        return refresh_saved_articles

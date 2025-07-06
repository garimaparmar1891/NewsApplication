from utils.header import HeaderUtils
from utils.token_storage import TokenStorage
from utils.article_reading_utils import ArticleReader
from utils.input_utils import get_article_id_input
from features.handlers.articles.save_unsave_handler import SaveUnsaveHandler
from features.handlers.articles.report_article_handler import ReportArticleHandler
from constants import messages as msg
from menu.menu_constants import (
    PAGINATED_MENU_INVALID_INPUT,
    PAGINATED_MENU_ARTICLE_NOT_FOUND,
    PAGINATED_MENU_LAST_PAGE,
    PAGINATED_MENU_FIRST_PAGE,
    PAGINATED_MENU_LOGOUT_SUCCESS,
    RETURN_TO_MAIN_MENU
)

ITEMS_PER_PAGE = 5


class PaginatedMenuUtils:
    @staticmethod
    def calculate_total_pages(articles, items_per_page=ITEMS_PER_PAGE):
        return (len(articles) + items_per_page - 1) // items_per_page
    
    @staticmethod
    def get_current_page_articles(articles, current_page, items_per_page=ITEMS_PER_PAGE):
        start_index = current_page * items_per_page
        end_index = start_index + items_per_page
        return articles[start_index:end_index]
    
    @staticmethod
    def can_go_next_page(current_page, total_pages):
        return current_page < total_pages - 1
    
    @staticmethod
    def can_go_previous_page(current_page):
        return current_page > 0
    
    @staticmethod
    def adjust_page_if_needed(current_page, total_pages):
        if current_page >= total_pages and total_pages > 0:
            return total_pages - 1
        elif total_pages == 0:
            return 0
        return current_page

    @staticmethod
    def show_header():
        HeaderUtils.print_welcome_message()
    
    @staticmethod
    def show_articles(articles, context_label):
        print(f"\n{context_label}:\n")
        for article in articles:
            print(f"(Article ID: {article.get('Id')}) → {article.get('Title')}\n")
    
    @staticmethod
    def show_page_info(current_page, total_pages):
        print(f"Page {current_page + 1} of {total_pages}")
    
    @staticmethod
    def show_menu_options(menu_options):
        print("\nOptions:")
        for option in menu_options:
            print(option)
    
    @staticmethod
    def get_user_choice(select_prompt):
        return input(f"\n{select_prompt}").strip()
    
    @staticmethod
    def show_message(message):
        print(message)

    @staticmethod
    def read_article(articles):
        article_id_input = get_article_id_input("read")
        if not article_id_input.isdigit():
            PaginatedMenuUtils.show_message(PAGINATED_MENU_INVALID_INPUT)
            return False
            
        article_id = int(article_id_input)
        article = next((a for a in articles if a["Id"] == article_id), None)
        
        if article:
            ArticleReader.read_article(article)
            return True
        else:
            PaginatedMenuUtils.show_message(PAGINATED_MENU_ARTICLE_NOT_FOUND)
            return False

    @staticmethod
    def save_unsave_article(is_saved_articles, refresh_callback=None):
        if is_saved_articles:
            success = SaveUnsaveHandler.unsave_article()
            if success and refresh_callback:
                return refresh_callback()
            return None
        else:
            SaveUnsaveHandler.save_article()
            return None

    @staticmethod
    def report_article():
        ReportArticleHandler.report_article()

    @staticmethod
    def return_to_main_menu():
        print(RETURN_TO_MAIN_MENU)

    @staticmethod
    def logout():
        TokenStorage.clear_token()
        print(PAGINATED_MENU_LOGOUT_SUCCESS)

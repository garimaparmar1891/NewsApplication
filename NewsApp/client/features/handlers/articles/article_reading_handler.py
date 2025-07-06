from features.services.articles.article_reading_service import ArticleReadingService
from features.services.articles.report_article_service import ReportArticleService
from utils.response_handler import handle_response
from constants import messages as msg

class ArticleReadingHandler:

    @staticmethod
    def handle_like_article(article_id):
        try:
            ArticleReadingService.like_article(article_id)
        except Exception as e:
            print(f"Failed to like article: {e}")

    @staticmethod
    def handle_dislike_article(article_id):
        try:
            ArticleReadingService.dislike_article(article_id)
            print("Article disliked successfully.")
        except Exception as e:
            print(f"Failed to dislike article: {e}")

    @staticmethod
    def handle_save_article(article_id):
        try:
            ArticleReadingService.save_article(article_id)
            print("Article saved successfully.")
        except Exception as e:
            print(f"Failed to save article: {e}")

    @staticmethod
    def handle_report_article(article_id):
        try:
            reason = input("Enter reason for reporting this article: ").strip()
            if not reason:
                print("Report reason cannot be empty.")
                return
            response = ReportArticleService.report_article(article_id, reason)
            handle_response(response, msg.ARTICLE_REPORT_SUCCESS, msg.ARTICLE_REPORT_FAILED)
        except Exception as e:
            print(e)

    @staticmethod
    def handle_logout():
        try:
            ArticleReadingService.logout()
            print("Logged out successfully.")
        except Exception as e:
            print(f"Error during logout: {e}")
            from utils.token_storage import TokenStorage
            TokenStorage.clear_token()
            exit()

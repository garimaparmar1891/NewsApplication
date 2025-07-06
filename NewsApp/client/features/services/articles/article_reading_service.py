from constants import messages as msg
from features.handlers.reactions.article_reactions_handler import ArticleReactionsHandler
from features.services.reactions.article_reactions_service import ArticleReactionsService
from features.services.articles.save_unsave_service import ArticleSaveService
from features.services.articles.report_article_service import ReportArticleService
from utils.response_handler import handle_response
from utils.token_storage import TokenStorage
from menu.menu_constants import ARTICLE_READING_LOGOUT_SUCCESS

class ArticleReadingService:

    @staticmethod
    def like_article(article_id):
        response = ArticleReactionsService.react_to_article(article_id, "like")
        ArticleReactionsHandler._handle_reaction_response(response)

    @staticmethod
    def dislike_article(article_id):
        response = ArticleReactionsService.react_to_article(article_id, "dislike")
        ArticleReactionsHandler._handle_reaction_response(response)

    @staticmethod
    def save_article(article_id):
        response = ArticleSaveService.save_article(article_id)
        handle_response(response, msg.ARTICLE_SAVE_SUCCESS, msg.ARTICLE_SAVE_FAILED)

    @staticmethod
    def report_article(article_id, reason):
        if not reason:
            print("Report reason cannot be empty.")
            return
        response = ReportArticleService.report_article(article_id, reason)
        handle_response(response, msg.ARTICLE_REPORT_SUCCESS, msg.ARTICLE_REPORT_FAILED)

    @staticmethod
    def logout():
        TokenStorage.clear_token()
        print(ARTICLE_READING_LOGOUT_SUCCESS)
        exit() 

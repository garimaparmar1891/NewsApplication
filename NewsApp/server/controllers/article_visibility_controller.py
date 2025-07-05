from services.article_visibility_service import ArticleVisibilityService
from utils.exception_handler import handle_exceptions
from constants import messages
from http import HTTPStatus
from utils.response_utils import error_response
from controllers.base_controller import BaseController

class ArticleVisibilityController(BaseController):
    def __init__(self):
        super().__init__()
        self.article_visibility_service = ArticleVisibilityService()

    @handle_exceptions()
    def report_article(self, article_id):
        user_id = self._get_user_id()
        data, error = self._validate_json_data(required_fields=["reason"])
        if error or data is None:
            return error if error else error_response(messages.MISSING_REQUIRED_FIELDS, HTTPStatus.BAD_REQUEST)
        reason = data["reason"]
        return self.article_visibility_service.report_article(article_id, user_id, reason)

    @handle_exceptions()
    def get_all_reported_articles(self):
        return self.article_visibility_service.get_all_reported_articles()

    @handle_exceptions()
    def toggle_article_visibility(self, article_id, action):
        return self.article_visibility_service.toggle_article_visibility(article_id, action)

    @handle_exceptions()
    def toggle_category_visibility(self, category_id, action):
        return self.article_visibility_service.toggle_category_visibility(category_id, action)

    @handle_exceptions()
    def add_blocked_keyword(self):
        data, error = self._validate_json_data(required_fields=["keyword"])
        if error or data is None:
            return error if error else error_response(messages.MISSING_REQUIRED_FIELDS, HTTPStatus.BAD_REQUEST)
        keyword = data["keyword"]
        return self.article_visibility_service.add_blocked_keyword(keyword)

    @handle_exceptions()
    def get_blocked_keywords(self):
        return self.article_visibility_service.get_blocked_keywords()

    @handle_exceptions()
    def delete_blocked_keyword(self, keyword_id):
        return self.article_visibility_service.delete_blocked_keyword(keyword_id)

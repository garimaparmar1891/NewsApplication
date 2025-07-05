from repositories.user_repository import UserRepository
from constants import messages
from utils.custom_exceptions import AppError
from http import HTTPStatus
from services.recommendation_service import RecommendationService
from services.base_service import BaseService

class UserService(BaseService):
    def __init__(self):
        super().__init__()
        self.repo = UserRepository()
        self.recommendation_service = RecommendationService()

    def save_article(self, user_id, article_id):
        success = self.repo.save_article(user_id, article_id)
        return self._handle_save_result(success)

    def get_saved_articles(self, user_id):
        rows = self.repo.get_saved_articles(user_id)
        self._validate_saved_articles(rows)
        
        visible_rows = self._get_visible_articles(rows)
        self._validate_filtered_articles(visible_rows)
        
        recommended_rows = self.recommendation_service.score_and_sort_articles(user_id, visible_rows)
        formatted_articles = [self._format_article_row(row) for row in recommended_rows]
        return formatted_articles

    def unsave_article(self, user_id, article_id):
        self._validate_article_saved(user_id, article_id)
        affected_rows = self.repo.unsave_article(user_id, article_id)
        return self._handle_unsave_result(affected_rows)

    def _get_visible_articles(self, rows):
        article_ids = [row["Id"] for row in rows]
        visible_ids = self.repo.get_visible_article_ids(article_ids)
        return [row for row in rows if row["Id"] in visible_ids]

    def _handle_save_result(self, success):
        if not success:
            raise AppError(messages.ARTICLE_SAVE_FAILED, HTTPStatus.INTERNAL_SERVER_ERROR)
        return messages.ARTICLE_SAVED

    def _validate_saved_articles(self, rows):
        if not rows:
            raise AppError(messages.NO_SAVED_ARTICLES, HTTPStatus.NOT_FOUND)

    def _validate_filtered_articles(self, filtered_rows):
        if not filtered_rows:
            raise AppError(messages.NO_SAVED_ARTICLES, HTTPStatus.NOT_FOUND)

    def _validate_article_saved(self, user_id, article_id):
        if not self.repo.is_article_saved_by_user(user_id, article_id):
            raise AppError(messages.ARTICLE_NOT_SAVED, HTTPStatus.BAD_REQUEST)

    def _handle_unsave_result(self, affected_rows):
        if affected_rows == 0:
            raise AppError(messages.ARTICLE_UNSAVE_FAILED, HTTPStatus.INTERNAL_SERVER_ERROR)
        return messages.ARTICLE_UNSAVED_SUCCESS

    def _format_article_row(self, row_dict):
        from utils.formatting import format_article_row
        return format_article_row(row_dict)

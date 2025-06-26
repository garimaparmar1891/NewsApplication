from flask_jwt_extended import get_jwt_identity
from services.user_service import UserService
from utils.response_utils import success_response, error_response
from http import HTTPStatus
from constants.messages import (
    NO_SAVED_ARTICLES,
    ARTICLE_UNSAVED_SUCCESS,
    ARTICLE_UNSAVE_FAILED,
    UNAUTHORIZED,
    ARTICLE_SAVED,
    ARTICLE_SAVE_FAILED
)


class UserController:
    def __init__(self):
        self.user_service = UserService()

    def save_article(self, article_id):
        user_id = self._get_user_id_or_unauthorized()
        if not user_id:
            return error_response(UNAUTHORIZED, HTTPStatus.UNAUTHORIZED)

        if self.user_service.save_article(user_id, article_id):
            return success_response(message=ARTICLE_SAVED)

        return error_response(ARTICLE_SAVE_FAILED, HTTPStatus.BAD_REQUEST)

    def get_saved_articles(self):
        user_id = get_jwt_identity()
        articles = self.user_service.get_saved_articles(user_id)

        if not articles:
            return self._error(NO_SAVED_ARTICLES, HTTPStatus.NOT_FOUND)
        return self._success(data=articles)

    def unsave_article(self, article_id):
        user_id = get_jwt_identity()
        result = self.user_service.unsave_article(user_id, article_id)

        if result.get("success"):
            return self._success(message=ARTICLE_UNSAVED_SUCCESS)
        return self._error(result.get("message", ARTICLE_UNSAVE_FAILED))


    def _success(self, data=None, message=None, status=HTTPStatus.OK):
        return success_response(data=data, message=message, status=status)

    def _error(self, message, status=HTTPStatus.BAD_REQUEST):
        return error_response(message=message, status=status)

    def _get_user_id_or_unauthorized(self):
        return get_jwt_identity()
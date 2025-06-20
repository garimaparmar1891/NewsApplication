from flask_jwt_extended import get_jwt_identity
from services.user_service import UserService
from utils.response_utils import success_response, error_response
from http import HTTPStatus


class UserController:
    def __init__(self):
        self.user_service = UserService()

    def get_saved_articles(self):
        user_id = get_jwt_identity()
        articles = self.user_service.get_saved_articles(user_id)

        if not articles:
            return self._error("No saved articles found", HTTPStatus.NOT_FOUND)
        return self._success(data=articles)

    def unsave_article(self, article_id):
        user_id = get_jwt_identity()
        result = self.user_service.unsave_article(user_id, article_id)

        if result.get("success"):
            return self._success(message="Article unsaved successfully")
        return self._error(result.get("message", "Could not unsave article"))

    def _success(self, data=None, message=None, status=HTTPStatus.OK):
        return success_response(data=data, message=message, status=status)

    def _error(self, message, status=HTTPStatus.BAD_REQUEST):
        return error_response(message=message, status=status)



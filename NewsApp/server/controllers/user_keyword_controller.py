from flask import request
from flask_jwt_extended import get_jwt_identity
from services.user_keyword_service import UserKeywordService
from utils.response_utils import success_response, error_response
from http import HTTPStatus


class UserKeywordController:
    def __init__(self):
        self.service = UserKeywordService()

    def add_keyword(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        category_id = data.get("category_id")
        keyword = data.get("word")

        if not category_id or not keyword:
            return self._error("Both category_id and keyword are required")

        if self.service.add_user_keyword(user_id, category_id, keyword):
            return self._success(message="Keyword added", status=HTTPStatus.CREATED)
        return self._error("Failed to add keyword")

    def get_keywords(self):
        user_id = get_jwt_identity()
        keywords = self.service.get_user_keywords(user_id)
        return self._success(data=keywords)

    def delete_keyword(self, keyword_id):
        user_id = get_jwt_identity()
        if self.service.delete_user_keyword(user_id, keyword_id):
            return self._success(message="Keyword deleted")
        return self._error("Keyword not found", HTTPStatus.NOT_FOUND)

    def _success(self, data=None, message=None, status=HTTPStatus.OK):
        return success_response(data=data, message=message, status=status)

    def _error(self, message, status=HTTPStatus.BAD_REQUEST):
        return error_response(message=message, status=status)

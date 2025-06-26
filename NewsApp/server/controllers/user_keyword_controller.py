from flask import request
from flask_jwt_extended import get_jwt_identity
from http import HTTPStatus

from services.user_keyword_service import UserKeywordService
from utils.response_utils import success_response, error_response
from constants.messages import (
    MISSING_KEYWORD_FIELDS,
    KEYWORD_ADDED,
    KEYWORD_ADD_FAILED,
    KEYWORD_DELETED,
    KEYWORD_NOT_FOUND
)


class UserKeywordController:
    def __init__(self):
        self.service = UserKeywordService()

    def add_user_keyword(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        category_id = data.get("category_id")
        keyword = data.get("word")

        if not category_id or not keyword:
            return self._error(MISSING_KEYWORD_FIELDS)

        success = self.service.add_user_keyword(user_id, category_id, keyword)
        if success:
            return self._success(message=KEYWORD_ADDED, status=HTTPStatus.CREATED)

        return self._error(KEYWORD_ADD_FAILED)

    def get_user_keywords(self):
        user_id = get_jwt_identity()
        keywords = self.service.get_user_keywords(user_id)
        return self._success(data=keywords)

    def delete_user_keyword(self, keyword_id):
        user_id = get_jwt_identity()
        success = self.service.delete_user_keyword(user_id, keyword_id)

        if success:
            return self._success(message=KEYWORD_DELETED)
        return self._error(KEYWORD_NOT_FOUND, HTTPStatus.NOT_FOUND)


    def _success(self, data=None, message=None, status=HTTPStatus.OK):
        return success_response(data=data, message=message, status=status)

    def _error(self, message, status=HTTPStatus.BAD_REQUEST):
        return error_response(message=message, status=status)

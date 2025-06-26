from flask import request
from http import HTTPStatus
from services.keyword_service import KeywordService
from utils.response_utils import success_response, error_response
from constants import messages


class KeywordController:
    def __init__(self):
        self.keyword_service = KeywordService()

    def get_all_keywords(self):
        keywords = self.keyword_service.get_all_keywords()
        if not keywords:
            return self._error(messages.KEYWORD_NOT_FOUND, HTTPStatus.NOT_FOUND)
        return self._success(data=keywords)

    def add_keyword(self):
        data = request.get_json()
        if not self._has_required_fields(data, ["word", "category_id"]):
            return self._error(messages.MISSING_REQUIRED_FIELDS)

        success = self.keyword_service.add_keyword(data["word"], data["category_id"])
        if success:
            return self._success(message=messages.KEYWORD_ADDED, status=HTTPStatus.CREATED)
        return self._error(messages.KEYWORD_ADD_FAILED)

    def delete_keyword(self, keyword_id):
        success = self.keyword_service.delete_keyword(keyword_id)
        if success:
            return self._success(message=messages.KEYWORD_DELETED)
        return self._error(messages.KEYWORD_NOT_FOUND, HTTPStatus.NOT_FOUND)


    def _has_required_fields(self, data, fields):
        return data and all(data.get(field) for field in fields)

    def _success(self, data=None, message=None, status=HTTPStatus.OK):
        return success_response({"data": data} if data else {}, message, status)

    def _error(self, message, status=HTTPStatus.BAD_REQUEST):
        return error_response(message, status)

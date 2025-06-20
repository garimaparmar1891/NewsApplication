from flask import request
from http import HTTPStatus
from services.keyword_service import KeywordService
from utils.response_utils import success_response, error_response


class KeywordController:
    def __init__(self):
        self.keyword_service = KeywordService()

    def get_all_keywords(self):
        keywords = self.keyword_service.get_all_keywords()
        if keywords:
            return self._success(data=keywords)
        return self._error("No keywords found", HTTPStatus.NOT_FOUND)

    def add_keyword(self):
        data = request.get_json()
        if not self._has_required_fields(data, ["word", "category_id"]):
            return self._error("Word and category_id are required")

        if self.keyword_service.add_keyword(data["word"], data["category_id"]):
            return self._success(message="Keyword added", status=HTTPStatus.CREATED)

        return self._error("Failed to add keyword")

    def delete_keyword(self, keyword_id):
        if self.keyword_service.delete_keyword(keyword_id):
            return self._success(message="Keyword deleted")
        return self._error("Keyword not found", HTTPStatus.NOT_FOUND)

    def _has_required_fields(self, data, fields):
        return data and all(data.get(field) for field in fields)

    def _success(self, data=None, message=None, status=HTTPStatus.OK):
        payload = {"data": data} if data else {}
        return success_response(payload, message, status)

    def _error(self, message, status=HTTPStatus.BAD_REQUEST):
        return error_response(message, status)

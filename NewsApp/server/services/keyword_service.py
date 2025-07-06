from repositories.keyword_repository import KeywordRepository
from constants import messages
from http import HTTPStatus
from utils.custom_exceptions import AppError
from utils.formatting import clean_word
from services.base_service import BaseService


class KeywordService(BaseService):
    def __init__(self):
        super().__init__()
        self.repository = KeywordRepository()

    def get_all_keywords(self):
        keywords = self.repository.get_all_keywords()
        if not keywords:
            raise AppError(messages.KEYWORD_NOT_FOUND, HTTPStatus.NOT_FOUND)
        return self._create_success_response(data=keywords)

    def add_keyword(self, word, category_id):
        self._validate_keyword_data(word, category_id)
        cleaned_word = self._clean_keyword(word)
        affected_rows = self.repository.add_keyword(cleaned_word, category_id)
        return self._handle_add_result(affected_rows)

    def delete_keyword(self, word):
        affected_rows = self.repository.delete_keyword(word)
        return self._handle_delete_result(affected_rows)


    def _validate_keyword_data(self, word, category_id):
        self._validate_required_fields(word, category_id, messages.MISSING_KEYWORD_FIELDS)

    def _clean_keyword(self, word):
        return clean_word(word)

    def _handle_add_result(self, affected_rows):
        if affected_rows == 0:
            raise AppError(messages.KEYWORD_ADD_FAILED, HTTPStatus.INTERNAL_SERVER_ERROR)
        return self._create_success_response(message=messages.KEYWORD_ADDED)

    def _handle_delete_result(self, affected_rows):
        if affected_rows == 0:
            raise AppError(messages.KEYWORD_NOT_FOUND, HTTPStatus.NOT_FOUND)
        return self._create_success_response(message=messages.KEYWORD_DELETED)

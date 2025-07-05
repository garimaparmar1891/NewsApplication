from repositories.user_keyword_repository import UserKeywordRepository
from constants import messages
from http import HTTPStatus
from utils.custom_exceptions import AppError
from utils.formatting import clean_word
from services.base_service import BaseService

class UserKeywordService(BaseService):
    def __init__(self):
        super().__init__()
        self.repository = UserKeywordRepository()

    def add_user_keyword(self, user_id, data):
        category_id = data.get('category_id')
        keyword = data.get('word')
        
        self._validate_required_fields(category_id, keyword, error_message=messages.MISSING_KEYWORD_FIELDS)
        
        cleaned_keyword = self._clean_and_validate_keyword(keyword)
        self._check_keyword_exists(user_id, category_id, cleaned_keyword)
        self._insert_keyword(user_id, category_id, cleaned_keyword)
        
        return self._create_success_response(message=messages.KEYWORD_ADDED)

    def get_user_keywords(self, user_id):
        keywords = self.repository.get_user_keywords(user_id)
        return self._create_success_response(data=keywords)

    def delete_user_keyword(self, user_id, keyword_id):
        affected_rows = self.repository.delete_user_keyword(user_id, keyword_id)
        if affected_rows == 0:
            raise AppError(messages.KEYWORD_NOT_FOUND, HTTPStatus.NOT_FOUND)
        return self._create_success_response(message=messages.KEYWORD_DELETED)

    def _clean_and_validate_keyword(self, keyword):
        return clean_word(keyword)

    def _check_keyword_exists(self, user_id, category_id, keyword):
        if self.repository.check_user_keyword_exists(user_id, category_id, keyword):
            raise AppError(messages.KEYWORD_ADD_FAILED, HTTPStatus.CONFLICT)

    def _insert_keyword(self, user_id, category_id, keyword):
        affected_rows = self.repository.insert_user_keyword(user_id, category_id, keyword)
        if affected_rows == 0:
            raise AppError(messages.KEYWORD_ADD_FAILED, HTTPStatus.INTERNAL_SERVER_ERROR)

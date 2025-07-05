from services.keyword_service import KeywordService
from utils.exception_handler import handle_exceptions
from constants import messages
from http import HTTPStatus
from utils.response_utils import error_response
from controllers.base_controller import BaseController

class KeywordController(BaseController):
    def __init__(self):
        super().__init__()
        self.keyword_service = KeywordService()

    @handle_exceptions()
    def get_keywords(self):
        return self.keyword_service.get_all_keywords()

    @handle_exceptions()
    def add_keyword(self):
        data, error = self._validate_json_data(required_fields=["word", "category_id"])
        if error:
            return error
        if not data:
            return error_response(messages.MISSING_KEYWORD_FIELDS, HTTPStatus.BAD_REQUEST)
        return self.keyword_service.add_keyword(data.get("word"), data.get("category_id"))

    @handle_exceptions()
    def delete_keyword(self, word):
        return self.keyword_service.delete_keyword(word)

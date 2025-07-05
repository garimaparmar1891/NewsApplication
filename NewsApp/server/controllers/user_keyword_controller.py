from flask import request
from services.user_keyword_service import UserKeywordService
from utils.exception_handler import handle_exceptions
from controllers.base_controller import BaseController

class UserKeywordController(BaseController):
    def __init__(self):
        super().__init__()
        self.service = UserKeywordService()

    @handle_exceptions()
    def add_user_keyword(self):
        user_id = self._get_user_id()
        data = request.get_json()
        return self.service.add_user_keyword(user_id, data)

    @handle_exceptions()
    def get_user_keywords(self):
        user_id = self._get_user_id()
        return self.service.get_user_keywords(user_id)

    @handle_exceptions()
    def delete_user_keyword(self, keyword_id):
        user_id = self._get_user_id()
        return self.service.delete_user_keyword(user_id, keyword_id)

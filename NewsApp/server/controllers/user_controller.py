from services.user_service import UserService
from utils.exception_handler import handle_exceptions
from utils.response_utils import success_response
from controllers.base_controller import BaseController


class UserController(BaseController):
    def __init__(self):
        super().__init__()
        self.user_service = UserService()

    @handle_exceptions()
    def save_article(self, article_id):
        user_id = self._get_user_id()
        message = self.user_service.save_article(user_id, article_id)
        return success_response(message=message)

    @handle_exceptions()
    def get_saved_articles(self):
        user_id = self._get_user_id()
        articles = self.user_service.get_saved_articles(user_id)
        return success_response(data=articles)

    @handle_exceptions()
    def unsave_article(self, article_id):
        user_id = self._get_user_id()
        message = self.user_service.unsave_article(user_id, article_id)
        return success_response(message=message)

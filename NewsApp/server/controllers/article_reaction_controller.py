from services.article_reaction_service import ArticleReactionService
from utils.exception_handler import handle_exceptions
from controllers.base_controller import BaseController

class ArticleReactionController(BaseController):
    def __init__(self):
        super().__init__()
        self.reaction_service = ArticleReactionService()

    @handle_exceptions()
    def react_to_article(self, article_id, reaction_type):
        user_id = self._get_user_id()
        return self.reaction_service.react_to_article(user_id, article_id, reaction_type)

    @handle_exceptions()
    def get_user_reactions(self):
        user_id = self._get_user_id()
        return self.reaction_service.get_user_reactions(user_id)

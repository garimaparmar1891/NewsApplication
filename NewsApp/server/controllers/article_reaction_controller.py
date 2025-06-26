from flask_jwt_extended import get_jwt_identity
from services.article_reaction_service import ArticleReactionService
from utils.response_utils import success_response, error_response
from http import HTTPStatus


class ArticleReactionController:
    def __init__(self):
        self.reaction_service = ArticleReactionService()

    def react_to_article(self, article_id, reaction_type):
        if not self._is_valid_reaction(reaction_type):
            return error_response("Invalid reaction type", HTTPStatus.BAD_REQUEST)

        user_id = get_jwt_identity()
        if self.reaction_service.react_to_article(user_id, article_id, reaction_type):
            return success_response(message="Reaction recorded successfully")

        return error_response("Failed to record reaction", HTTPStatus.INTERNAL_SERVER_ERROR)

    def get_user_reactions(self):
        user_id = get_jwt_identity()
        reactions = self.reaction_service.get_user_reactions(user_id)
        return success_response(data=reactions)

    def _is_valid_reaction(self, reaction_type):
        return reaction_type in {"like", "dislike"}

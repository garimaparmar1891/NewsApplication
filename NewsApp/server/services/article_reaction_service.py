from repositories.article_reaction_repository import ArticleReactionRepository
from repositories.article_repository import ArticleRepository
from constants import messages
from services.base_service import BaseService
from http import HTTPStatus


class ArticleReactionService(BaseService):
    def __init__(self):
        super().__init__()
        self.repo = ArticleReactionRepository()
        self.article_repo = ArticleRepository()

    def react_to_article(self, user_id, article_id, reaction_type):
        self._validate_required_fields(user_id, article_id, reaction_type, 
                                     error_message=messages.MISSING_REQUIRED_FIELDS)
        self._validate_reaction_type(reaction_type)
        self._ensure_article_exists(article_id)
        
        existing_reaction = self.repo.check_user_reaction(user_id, article_id)
        if existing_reaction and existing_reaction.lower() == reaction_type.lower():
            if reaction_type.lower() == "like":
                raise self._create_app_error(messages.ALREADY_LIKED, HTTPStatus.BAD_REQUEST)
            else:
                raise self._create_app_error(messages.ALREADY_DISLIKED, HTTPStatus.BAD_REQUEST)
        
        success = self.repo.react_to_article(user_id, article_id, reaction_type)
        
        if not success:
            raise self._create_app_error(messages.REACTION_FAILED, HTTPStatus.INTERNAL_SERVER_ERROR)
        
        return self._create_success_response(message=messages.REACTION_RECORDED)

    def get_user_reactions(self, user_id):
        self._validate_required_fields(user_id, error_message=messages.UNAUTHORIZED)
        reactions = self.repo.get_user_reactions(user_id)
        return self._create_success_response(data=reactions)

    def get_user_liked_articles(self, user_id):
        self._validate_required_fields(user_id, error_message=messages.UNAUTHORIZED)
        reactions = self.repo.get_user_reactions(user_id)
        liked_articles = self._filter_reactions_by_type(reactions, "like")
        return self._create_success_response(data=liked_articles)

    def get_user_disliked_articles(self, user_id):
        self._validate_required_fields(user_id, error_message=messages.UNAUTHORIZED)
        reactions = self.repo.get_user_reactions(user_id)
        disliked_articles = self._filter_reactions_by_type(reactions, "dislike")
        return self._create_success_response(data=disliked_articles)


    def _validate_reaction_type(self, reaction_type):
        if reaction_type not in {"like", "dislike"}:
            raise self._create_app_error(messages.INVALID_REACTION_TYPE, HTTPStatus.BAD_REQUEST)

    def _ensure_article_exists(self, article_id):
        article = self.article_repo.get_article_by_id(article_id)
        if not article:
            raise self._create_app_error(messages.ARTICLE_NOT_FOUND, HTTPStatus.NOT_FOUND)

    def _filter_reactions_by_type(self, reactions, reaction_type):
        return [
            {"ArticleId": r["article_id"], "Reaction": r["reaction"], "ReactedAt": r["reacted_at"]}
            for r in reactions if r["reaction"].lower() == reaction_type
        ]

    def _create_app_error(self, message, status_code):
        from utils.custom_exceptions import AppError
        return AppError(message, status_code)

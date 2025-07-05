from utils.db import fetch_all_query_with_params, execute_write_query, fetch_one_query
from queries import article_reaction_queries as q
from constants import messages
import logging

logger = logging.getLogger(__name__)


class ArticleReactionRepository:
    def react_to_article(self, user_id, article_id, reaction_type):
        params = (user_id, article_id, reaction_type, user_id, article_id, reaction_type)
        return execute_write_query(
            query=q.ADD_OR_UPDATE_REACTION,
            params=params,
            error_msg=messages.DB_ERROR_REACT_TO_ARTICLE
        )

    def get_user_reactions(self, user_id):
        try:
            return fetch_all_query_with_params(
                q.GET_REACTIONS_BY_USER, 
                self._map_reaction_row, 
                messages.DB_ERROR_GET_USER_REACTIONS, 
                (user_id,)
            )
        except Exception as e:
            logger.error("DB ERROR in get_user_reactions: %s", e)
            return []

    def check_user_reaction(self, user_id, article_id):
        """Check if user has already reacted to an article and return the reaction type."""
        try:
            result = fetch_one_query(
                q.CHECK_USER_REACTION,
                (user_id, article_id),
                error_msg=messages.DB_ERROR_GET_USER_REACTIONS
            )
            return result.ReactionType if result else None
        except Exception as e:
            logger.error("DB ERROR in check_user_reaction: %s", e)
            return None

    def _map_reaction_row(self, row):
        return {
            "article_id": row.ArticleId if hasattr(row, 'ArticleId') else row[0],
            "reaction": row.ReactionType if hasattr(row, 'ReactionType') else row[1],
            "reacted_at": row.ReactedAt if hasattr(row, 'ReactedAt') else row[2]
        }

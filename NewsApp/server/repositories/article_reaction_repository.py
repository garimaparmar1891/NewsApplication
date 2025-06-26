from utils.db import get_db_connection
from queries import article_reaction_queries as q


class ArticleReactionRepository:
    def react_to_article(self, data: dict) -> bool:
        params = (
            data["user_id"],
            data["article_id"],
            data["reaction_type"],
            data["user_id"],
            data["article_id"],
            data["reaction_type"]
        )
        return self._execute_write(
            query=q.ADD_OR_UPDATE_REACTION,
            params=params,
            error_msg="[DB ERROR] react_to_article"
        )

    def get_user_reactions(self, user_id: int) -> list:
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(q.GET_REACTIONS_BY_USER, (user_id,))
                return [
                    {
                        "article_id": row.ArticleId,
                        "reaction": row.ReactionType,
                        "reacted_at": row.ReactedAt
                    }
                    for row in cursor.fetchall()
                ]
        except Exception as e:
            print("[DB ERROR] get_user_reactions:", e)
            return []


    def _execute_write(self, query, params, error_msg: str) -> bool:
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return True
        except Exception as e:
            print(f"{error_msg}: {e}")
            return False

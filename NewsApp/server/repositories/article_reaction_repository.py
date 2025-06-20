from utils.db import get_db_connection
from queries import article_reaction_queries as q


class ArticleReactionRepository:
    def add_or_update_reaction(self, data: dict):
        user_id = data["user_id"]
        article_id = data["article_id"]
        reaction_type = data["reaction_type"]
        return self._execute_write_query(
            q.ADD_OR_UPDATE_REACTION,
            (user_id, article_id, reaction_type, user_id, article_id, reaction_type),
            "[DB ERROR] add_or_update_reaction"
        )

    def get_reactions_by_user(self, user_id):
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
            print("[DB ERROR] get_reactions_by_user:", e)
            return []

    def delete_reaction(self, user_id, article_id):
        return self._execute_write_query(
            q.DELETE_REACTION,
            (user_id, article_id),
            "[DB ERROR] delete_reaction",
            expect_rows=True
        )

    def _execute_write_query(self, query, params, error_msg, expect_rows=False):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount > 0 if expect_rows else True
        except Exception as e:
            print(f"{error_msg}:", e)
            return False

from utils.db import get_db_connection
from queries import user_keywords as q

class UserKeywordRepository:

    def add_user_keyword(self, user_id, category_id, keyword):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(q.INSERT_USER_KEYWORD, (user_id, category_id, keyword))
                conn.commit()
                return True
            except Exception as e:
                print("Failed to insert user keyword:", e)
                conn.rollback()
                return False

    def get_user_keywords(self, user_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.GET_USER_KEYWORDS, (user_id,))
            return [
                {
                    "id": row.Id,
                    "keyword": row.Keyword,
                    "category": row.Category
                }
                for row in cursor.fetchall()
            ]

    def delete_user_keyword(self, user_id, keyword_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.DELETE_USER_KEYWORD, (keyword_id, user_id))
            conn.commit()
            return cursor.rowcount > 0

    def get_user_keywords_map(self, user_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.GET_USER_KEYWORD_MAP, (user_id,))
            keyword_map = {}
            for row in cursor.fetchall():
                keyword_map.setdefault(row.CategoryId, []).append(row.Keyword.lower())
            return keyword_map

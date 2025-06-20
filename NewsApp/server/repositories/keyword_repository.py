from utils.db import get_db_connection
from queries import keyword_queries as q

class KeywordRepository:
    def get_all_keywords(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.GET_ALL_KEYWORDS)
            return [
                {
                    "id": row.Id,
                    "word": row.Word,
                    "category_id": row.CategoryId
                }
                for row in cursor.fetchall()
            ]

    def add_keyword(self, word, category_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(q.INSERT_KEYWORD, (word, category_id))
                conn.commit()
                return True
            except Exception as e:
                print(f"[DB ERROR] add_keyword: {e}")
                return False

    def delete_keyword(self, keyword_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.DELETE_KEYWORD, (keyword_id,))
            conn.commit()
            return cursor.rowcount > 0


from utils.db import get_db_connection
from queries import keyword_queries as q


class KeywordRepository:

    def get_all_keywords(self):
        return self._fetch_all(
            query=q.GET_ALL_KEYWORDS,
            row_mapper=lambda row: {
                "id": row.Id,
                "word": row.Word,
                "category_id": row.CategoryId
            }
        )

    def add_keyword(self, word, category_id):
        return self._execute_write(
            query=q.INSERT_KEYWORD,
            params=(word, category_id),
            error_msg="[DB ERROR] add_keyword"
        )

    def delete_keyword(self, keyword_id):
        return self._execute_write(
            query=q.DELETE_KEYWORD,
            params=(keyword_id,),
            error_msg="[DB ERROR] delete_keyword",
            check_rowcount=True
        )


    def _fetch_all(self, query, params=None, row_mapper=None):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params or [])
                rows = cursor.fetchall()
                return [row_mapper(row) for row in rows] if row_mapper else rows
        except Exception as e:
            print(f"[DB ERROR] fetch_all: {e}")
            return []

    def _execute_write(self, query, params=None, error_msg="[DB ERROR]", check_rowcount=False):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params or [])
                conn.commit()
                return cursor.rowcount > 0 if check_rowcount else True
        except Exception as e:
            print(f"{error_msg}: {e}")
            return False

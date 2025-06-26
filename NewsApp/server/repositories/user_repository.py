from utils.db import get_db_connection
from queries import user_queries as q


class UserRepository:
    def save_article(self, user_id, article_id):
        try:
            return self._execute_write(
                q.SAVE_ARTICLE,
                (user_id, article_id, user_id, article_id)
            )
        except Exception as e:
            print(f"[Save Article Error]: {e}")
            return False

    def unsave_article(self, user_id, article_id):
        return self._execute_write(q.UNSAVE_ARTICLE, (user_id, article_id))

    def is_article_saved_by_user(self, user_id, article_id):
        result = self._fetch_one(q.CHECK_ARTICLE_SAVED, (user_id, article_id))
        return result is not None

    def get_saved_articles(self, user_id):
        rows = self._fetch_all(q.GET_SAVED_ARTICLES, (user_id,))
        return [
            {
                "Id": row.Id,
                "Title": row.Title,
                "Content": row.Content,
                "Source": row.Source,
                "Url": row.Url,
                "Category": row.Category,
                "PublishedAt": row.PublishedAt.strftime("%Y-%m-%d %H:%M")
            }
            for row in rows
        ]


    def _fetch_one(self, query, params):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()

    def _fetch_all(self, query, params):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def _execute_write(self, query, params):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0

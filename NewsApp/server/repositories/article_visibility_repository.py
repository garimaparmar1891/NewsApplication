from utils.db import get_db_connection
import queries.article_visibility_queries as q

class ArticleModerationRepository:

    def insert_report(self, user_id, article_id, reason):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(q.INSERT_REPORT, (user_id, article_id, reason))
                conn.commit()
                return True
        except Exception as e:
            print("Error reporting article:", e)
            return False

    def fetch_reported_articles(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.FETCH_REPORTED_ARTICLES)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def update_article_visibility(self, article_id, hide=True):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.UPDATE_ARTICLE_VISIBILITY, (int(hide), article_id))
            conn.commit()

    def update_category_visibility(self, category_id, hide=True):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.UPDATE_CATEGORY_VISIBILITY, (int(hide), category_id))
            conn.commit()

    def insert_blocked_keyword(self, keyword):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.INSERT_BLOCKED_KEYWORD, (keyword,))
            conn.commit()

    def get_blocked_keywords(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.GET_BLOCKED_KEYWORDS)
            return [row[0] for row in cursor.fetchall()]

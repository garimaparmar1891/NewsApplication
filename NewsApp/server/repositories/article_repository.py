from datetime import datetime
from utils.db import get_db_connection
from queries import article_queries as q
from utils.formatting import format_article_row


class ArticleRepository:
    def get_today_headlines(self, date):
        rows = self._execute_query(q.GET_TODAY_HEADLINES, (date,))
        return [format_article_row(row) for row in rows]


    def search_articles_by_keyword_and_range(self, keyword, start_date, end_date):
        like_keyword = f"%{keyword}%"
        rows = self._execute_query(
            q.SEARCH_ARTICLES_BY_KEYWORD_AND_RANGE,
            (like_keyword, like_keyword, start_date, end_date)
        )
        return [format_article_row(row) for row in rows]

    def get_articles_by_range(self, start_date, end_date, category_id=None):
        category_clause = "AND A.CategoryId = ?" if category_id else ""
        query = q.GET_ARTICLES_BY_RANGE_BASE.format(category_clause=category_clause)
        params = [start_date, end_date] + ([category_id] if category_id else [])

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_articles_for_categories_since(self, category_ids, since_datetime):
        if not category_ids:
            return []

        placeholders = ",".join("?" for _ in category_ids)
        query = q.GET_ARTICLES_FOR_CATEGORIES_SINCE.format(placeholders=placeholders)
        params = category_ids + [since_datetime]

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]


    def bulk_insert_articles(self, articles):
        inserted_ids = []
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for article in articles:
                try:
                    published_at = article.get("published_at")
                    if isinstance(published_at, str):
                        published_at = datetime.fromisoformat(published_at.replace("Z", "+00:00"))

                    cursor.execute(q.INSERT_ARTICLE, (
                        article["title"],
                        article.get("content"),
                        article.get("source"),
                        article.get("url"),
                        article["category_id"],
                        published_at,
                        article["server_id"]
                    ))
                    conn.commit()

                    cursor.execute(q.GET_INSERTED_ARTICLE_ID)
                    inserted_ids.append(cursor.fetchone()[0])

                except Exception as e:
                    print(f"[Bulk Insert Error] '{article['title']}': {e}")
                    conn.rollback()

        return inserted_ids


    def record_article_read(self, user_id, article_id):
        try:
            self._execute_query_with_commit(q.INSERT_READ_HISTORY, (user_id, article_id))
            return True
        except Exception as e:
            print(f"[Insert Read History Error]: {e}")
            return False


    def get_all_categories(self):
        rows = self._execute_query(q.GET_CATEGORIES)
        return [{"id": row.Id, "name": row.Name} for row in rows]


    def _execute_query(self, query, params=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            return cursor.fetchall()

    def _execute_query_with_commit(self, query, params=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            conn.commit()
            return cursor

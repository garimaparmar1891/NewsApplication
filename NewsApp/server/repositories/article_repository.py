from utils.db import get_db_connection
from queries import article_queries as q
from utils.formatting import format_article_row
from datetime import datetime

class ArticleRepository:
    def _execute_query(self, query, params=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            return cursor.fetchall()

    def _execute_query_and_commit(self, query, params=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            conn.commit()
            return cursor

    def get_today_headlines(self, date):
        rows = self._execute_query(q.GET_TODAY_HEADLINES, (date,))
        return [format_article_row(row) for row in rows]

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
                    print(f"Bulk Insert Error for '{article['title']}':", e)
                    conn.rollback()
        return inserted_ids

    def get_all_articles(self):
        rows = self._execute_query(q.GET_ALL_ARTICLES)
        return [format_article_row(row) for row in rows]

    def get_articles_by_range(self, start_date, end_date, category_id):
        category_clause = "AND A.CategoryId = ?" if category_id else ""
        query = q.GET_ARTICLES_BY_RANGE_BASE.format(category_clause=category_clause)
        params = [start_date, end_date] + ([category_id] if category_id else [])

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_all_categories(self):
        rows = self._execute_query(q.GET_CATEGORIES)
        return [{"id": row.Id, "name": row.Name} for row in rows]

    def save_article(self, user_id, article_id):
        try:
            self._execute_query_and_commit(q.SAVE_ARTICLE, (user_id, article_id, user_id, article_id))
            return True
        except Exception as e:
            print("Save Article Error:", e)
            return False

    def search_articles_by_keyword_and_range(self, keyword, start_date, end_date):
        like_keyword = f"%{keyword}%"
        rows = self._execute_query(q.SEARCH_ARTICLES_BY_KEYWORD_AND_RANGE, (
            like_keyword, like_keyword, start_date, end_date
        ))
        return [format_article_row(row) for row in rows]


    def get_articles_for_categories_since(self, category_ids, since_datetime):
        print(f"[SQL DEBUG] Fetching articles fetched after {since_datetime} for categories {category_ids}")

        if not category_ids:
            return []

        placeholders = ','.join('?' for _ in category_ids)
        query = f"""
            SELECT A.Id, A.Title, A.Content, A.Source, A.Url, A.CategoryId, A.PublishedAt, A.FetchedAt
            FROM Articles A
            WHERE A.CategoryId IN ({placeholders})
            AND A.FetchedAt > ?
            ORDER BY A.FetchedAt DESC
        """

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, category_ids + [since_datetime])
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]  # ✅ convert to list of dicts

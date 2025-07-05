from utils.db import get_db_connection, fetch_one_query, fetch_all_query, fetch_all_query_with_params, execute_write_query
from queries import article_queries as q
from queries import article_visibility_queries as avq
from queries import category_queries
from utils.formatting import format_article_row
from constants import messages

class ArticleRepository:
    def get_today_headlines(self, date):
        return fetch_all_query_with_params(
            q.GET_TODAY_HEADLINES, 
            self._format_article_row, 
            messages.DB_ERROR_GET_TODAY_HEADLINES, 
            (date,)
        )

    def search_articles_by_keyword_and_range(self, keyword, start_date, end_date):
        like_keyword = f"%{keyword}%"
        return fetch_all_query_with_params(
            q.SEARCH_ARTICLES_BY_KEYWORD_AND_RANGE,
            self._format_article_row,
            messages.DB_ERROR_SEARCH_ARTICLES,
            (like_keyword, like_keyword, start_date, end_date)
        )

    def get_articles_by_range(self, start_date, end_date, category_id=None):
        category_clause = "AND A.CategoryId = ?" if category_id else ""
        query = q.GET_ARTICLES_BY_RANGE_BASE.format(category_clause=category_clause)
        params = [start_date, end_date] + ([category_id] if category_id else [])
        return fetch_all_query_with_params(
            query,
            self._format_article_row,
            messages.DB_ERROR_GET_ARTICLES_BY_RANGE,
            params
        )

    def bulk_insert_articles(self, articles):
        inserted_ids = []
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for article in articles:
                try:
                    cursor.execute(q.INSERT_ARTICLE, self._prepare_article_data(article))
                    conn.commit()
                    cursor.execute(q.GET_INSERTED_ARTICLE_ID)
                    row = cursor.fetchone()
                    if row:
                        inserted_ids.append(row[0])
                    else:
                        print(f"{messages.DB_ERROR_BULK_INSERT_ARTICLE} {messages.DB_ERROR_COULD_NOT_FETCH_ID} '{article['title']}'")
                except Exception as e:
                    print(f"{messages.DB_ERROR_BULK_INSERT_ARTICLE} '{article['title']}': {e}")
                    conn.rollback()
        return inserted_ids

    def record_article_read(self, user_id, article_id):
        try:
            execute_write_query(q.INSERT_READ_HISTORY, (user_id, article_id), messages.DB_ERROR_INSERT_READ_HISTORY)
            return True
        except Exception as e:
            print(f"{messages.DB_ERROR_INSERT_READ_HISTORY}: {e}")
            return False

    def get_all_categories(self):
        return fetch_all_query(
            category_queries.GET_CATEGORIES,
            self._format_category_row,
            messages.DB_ERROR_GET_CATEGORIES
        )

    def get_article_by_id(self, article_id):
        row = fetch_one_query(q.GET_ARTICLE_BY_ID, (article_id,), messages.DB_ERROR_GET_ARTICLE_BY_ID)
        if row:
            return self._format_article_row(row)
        return None

    def get_blocked_keywords(self):
        return fetch_all_query(
            avq.GET_BLOCKED_KEYWORDS,
            lambda row: row[1],
            messages.DB_ERROR_GET_BLOCKED_KEYWORDS
        )

    def get_all_articles(self):
        return fetch_all_query(
            q.GET_ALL_ARTICLES,
            self._format_article_row,
            messages.DB_ERROR_GET_ALL_ARTICLES
        )

    def article_exists_by_title(self, title):
        row = fetch_one_query(q.GET_ARTICLE_BY_TITLE, (title,))
        return bool(row)

    def article_exists_duplicate(self, title, url, published_at):
        """Check if article exists by title, URL, or published date combination"""
        if not title or not url or not published_at:
            return self.article_exists_by_title(title)
        
        row = fetch_one_query(q.CHECK_ARTICLE_DUPLICATE, (title, url, published_at))
        return bool(row)

    def get_read_history(self, user_id):
        return fetch_all_query_with_params(
            q.GET_READ_HISTORY, 
            self._format_read_history_row, 
            messages.DB_ERROR_GET_READ_HISTORY, 
            (user_id,)
        )

    def _format_article_row(self, row):
        return format_article_row({
            "Id": row[0],
            "Title": row[1],
            "Content": row[2],
            "Source": row[3],
            "Url": row[4],
            "Category": row[5],
            "PublishedAt": row[6]
        })

    def _format_category_row(self, row):
        return {"Id": row[0], "Name": row[1]}

    def _format_read_history_row(self, row):
        return {"ArticleId": row[0], "ReadAt": row[1]}

    def _prepare_article_data(self, article):
        return (
            article["title"],
            article.get("content"),
            article.get("source"),
            article.get("url"),
            article["category_id"],
            article["published_at"],
            article["server_id"],
            article["is_hidden"]
        )

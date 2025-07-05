from utils.db import get_db_connection, fetch_one_query, fetch_all_query, execute_write_query, fetch_all_query_with_params
from queries import article_visibility_queries as q
from queries import category_queries as cq
from constants import messages
import pyodbc

class ArticleVisibilityRepository:
    def add_report(self, article_id, user_id, reason):
        try:
            execute_write_query(q.ADD_ARTICLE_REPORT, (article_id, user_id, reason), messages.DB_ERROR_ADD_REPORT)
        except pyodbc.IntegrityError as e:
            if "UQ_User_Article_in_RA" in str(e):
                raise ValueError("You have already reported this article.")
            raise

    def get_all_reported_articles(self):
        return fetch_all_query(
            q.GET_ALL_REPORTED_ARTICLES,
            lambda row: dict(zip([d[0] for d in row.cursor_description], row)),
            messages.DB_ERROR_GET_REPORTED_ARTICLES
        )

    def get_report_count(self, article_id):
        row = fetch_one_query(q.GET_REPORT_COUNT, (article_id,))
        return row[0] if row else 0

    def hide_article(self, article_id):
        execute_write_query(q.HIDE_ARTICLE, (article_id,), messages.DB_ERROR_HIDE_ARTICLE)

    def unhide_article(self, article_id):
        execute_write_query(q.UNHIDE_ARTICLE, (article_id,), messages.DB_ERROR_UNHIDE_ARTICLE)

    def hide_category(self, category_id):
        execute_write_query(q.HIDE_CATEGORY, (category_id,), messages.DB_ERROR_HIDE_CATEGORY)

    def unhide_category(self, category_id):
        execute_write_query(q.UNHIDE_CATEGORY, (category_id,), messages.DB_ERROR_UNHIDE_CATEGORY)

    def add_blocked_keyword(self, keyword):
        execute_write_query(q.ADD_BLOCKED_KEYWORD, (keyword,), messages.DB_ERROR_ADD_BLOCKED_KEYWORD)

    def get_blocked_keywords(self):
        return fetch_all_query(
            q.GET_BLOCKED_KEYWORDS,
            lambda row: dict(zip([d[0] for d in row.cursor_description], row)),
            messages.DB_ERROR_GET_BLOCKED_KEYWORDS
        )

    def is_keyword_blocked(self, content):
        keywords = self.get_blocked_keywords()
        return any(kw["Keyword"].lower() in content.lower() for kw in keywords)

    def article_exists(self, article_id):
        row = fetch_one_query(q.ARTICLE_EXISTS, (article_id,))
        return row is not None

    def clear_article_reports(self, article_id):
        execute_write_query(q.CLEAR_ARTICLE_REPORTS, (article_id,), messages.DB_ERROR_CLEAR_REPORTS)

    def delete_blocked_keyword(self, keyword_id):
        affected_rows = execute_write_query(q.DELETE_BLOCKED_KEYWORD, (keyword_id,), messages.DB_ERROR_DELETE_BLOCKED_KEYWORD)
        return affected_rows

    def get_user_reported_articles(self, user_id):
        return fetch_all_query_with_params(
            q.GET_USER_REPORTED_ARTICLES,
            lambda row: row.ArticleId if hasattr(row, 'ArticleId') else row[0],
            messages.DB_ERROR_GET_USER_REPORTED,
            (user_id,)
        )

    def unhide_articles_after_keyword_removal(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            articles = self._get_all_articles(cursor)
            blocked_keywords = self._get_blocked_keywords(cursor)
            
            for article in articles:
                if self._should_unhide_article(cursor, article, blocked_keywords):
                    cursor.execute(q.UNHIDE_ARTICLE, (article.Id,))
            
            conn.commit()

    def _get_all_articles(self, cursor):
        cursor.execute(q.GET_ALL_ARTICLES_FOR_UNHIDE)
        return cursor.fetchall()

    def _get_blocked_keywords(self, cursor):
        cursor.execute(q.GET_BLOCKED_KEYWORDS)
        return [row.Keyword.lower() for row in cursor.fetchall()]

    def _should_unhide_article(self, cursor, article, blocked_keywords):
        if self._is_blocked_by_keyword(article, blocked_keywords):
            return False
        
        if self._has_reports(cursor, article.Id):
            return False
        
        if self._is_category_hidden(cursor, article.CategoryId):
            return False
        
        return True

    def _is_blocked_by_keyword(self, article, blocked_keywords):
        title = (article.Title or "").lower()
        content = (article.Content or "").lower()
        combined_text = f"{title} {content}"
        return any(kw in combined_text for kw in blocked_keywords)

    def _has_reports(self, cursor, article_id):
        cursor.execute(q.GET_REPORT_COUNT, (article_id,))
        report_count_row = cursor.fetchone()
        return report_count_row[0] > 0 if report_count_row else False

    def _is_category_hidden(self, cursor, category_id):
        cursor.execute(cq.GET_CATEGORY_IS_HIDDEN, (category_id,))
        cat_row = cursor.fetchone()
        return cat_row and cat_row[0] == 1

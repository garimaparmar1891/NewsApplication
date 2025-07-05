from utils.db import get_db_connection, fetch_one_query, fetch_all_query, execute_write_query, fetch_all_query_with_params
from queries import notification_queries as q
from queries import user_keywords as uk
from queries import login_history_queries as lhq
from constants import messages
import logging

logger = logging.getLogger(__name__)


class NotificationRepository:
    def update_user_preferences(self, user_id, preferences):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                for pref in preferences:
                    self._upsert_preference(cursor, user_id, pref)
                conn.commit()
            return True
        except Exception as e:
            logger.error(messages.DB_ERROR_UPDATE_PREFERENCES + ": %s", e)
            return False

    def _upsert_preference(self, cursor, user_id, preference):
        category_id = preference.get("categoryId")
        is_enabled = preference.get("isEnabled", True)
        cursor.execute(
            q.UPSERT_NOTIFICATION_PREF,
            (user_id, category_id, is_enabled, user_id, category_id, is_enabled)
        )

    def get_enabled_category_ids(self, user_id):
        return self._fetch_column(q.GET_ENABLED_CATEGORIES, (user_id,), "CategoryId")

    def get_user_preferences(self, user_id):
        return fetch_all_query_with_params(
            q.GET_USER_PREFERENCES, 
            self._map_preference_row, 
            messages.DB_ERROR_GET_USER_PREFERENCES, 
            (user_id,)
        )

    def _map_preference_row(self, row):
        return {
            "categoryId": row.CategoryId,
            "CategoryName": row.CategoryName,
            "isEnabled": bool(row.IsEnabled)
        }

    def get_user_keywords(self, user_id):
        return fetch_all_query_with_params(
            uk.GET_USER_KEYWORD_MAP, 
            self._map_keyword_row, 
            messages.DB_ERROR_GET_USER_KEYWORDS, 
            (user_id,)
        )

    def _map_keyword_row(self, row):
        return {
            "categoryId": row.CategoryId,
            "keyword": row.Keyword.lower()
        }

    def add_user_keyword(self, user_id, category_id, keyword):
        try:
            if self._keyword_exists(user_id, category_id, keyword):
                return False
            execute_write_query(
                uk.INSERT_USER_KEYWORD, 
                (user_id, category_id, keyword), 
                messages.DB_ERROR_ADD_USER_KEYWORD
            )
            return True
        except Exception as e:
            logger.error(messages.DB_ERROR_ADD_USER_KEYWORD + ": %s", e)
            return False

    def _keyword_exists(self, user_id, category_id, keyword):
        row = fetch_one_query(uk.CHECK_USER_KEYWORD_EXISTS, (user_id, category_id, keyword))
        return row is not None

    def get_unsent_articles(self, user_id, category_id, keyword):
        like_keyword = f"%{keyword.lower()}%"
        return fetch_all_query_with_params(
            q.GET_UNSENT_ARTICLES, 
            lambda row: row, 
            messages.DB_ERROR_GET_UNSENT_ARTICLES, 
            (user_id, category_id, like_keyword, like_keyword)
        )

    def get_articles_by_categories(self, user_id, category_ids):
        if not category_ids:
            return []
        placeholders = ",".join(["?"] * len(category_ids))
        query = q.GET_ARTICLES_BY_CATEGORIES.format(placeholders=placeholders)
        params = [user_id] + category_ids
        return fetch_all_query_with_params(
            query, 
            lambda row: row, 
            messages.DB_ERROR_GET_ARTICLES_BY_CATEGORIES, 
            params
        )

    def mark_articles_as_sent(self, user_id, article_ids):
        if not article_ids:
            return
        for article_id in article_ids:
            self._mark_single_article_sent(user_id, article_id)

    def _mark_single_article_sent(self, user_id, article_id):
        execute_write_query(
            q.MARK_ARTICLE_AS_SENT, 
            (user_id, article_id, user_id, article_id), 
            messages.DB_ERROR_MARK_ARTICLES_SENT
        )

    def get_unread_user_notifications(self, user_id):
        return fetch_all_query_with_params(
            q.GET_UNREAD_NOTIFICATIONS, 
            self._map_notification_row, 
            messages.DB_ERROR_GET_UNREAD_NOTIFICATIONS, 
            (user_id,)
        )

    def _map_notification_row(self, row):
        return {
            "notification_id": row.Id,
            "article_id": row.ArticleId,
            "title": row.Title,
            "source": row.Source,
            "message": row.Message,
            "created_at": row.CreatedAt,
        }

    def mark_notifications_as_read(self, user_id):
        execute_write_query(
            q.MARK_NOTIFICATIONS_AS_READ, 
            (user_id,), 
            messages.DB_ERROR_MARK_NOTIFICATIONS_READ
        )

    def insert_notification(self, user_id, article_id, message):
        execute_write_query(
            q.INSERT_NOTIFICATION, 
            (user_id, article_id, message), 
            messages.DB_ERROR_INSERT_NOTIFICATION
        )

    def get_users_with_enabled_preferences(self):
        return fetch_all_query(
            q.GET_USERS_WITH_PREFS, 
            self._map_user_row, 
            messages.DB_ERROR_GET_USERS_WITH_PREFS
        )

    def _map_user_row(self, row):
        return {
            "user_id": row.Id, 
            "email": row.Email, 
            "username": row.Username
        }

    def get_last_login(self, user_id):
        row = fetch_one_query(lhq.GET_LAST_LOGIN, (user_id,))
        return row[0] if row else None

    def _fetch_column(self, query, params, column_name):
        return [
            getattr(row, column_name) 
            for row in fetch_all_query_with_params(
                query, 
                lambda row: row, 
                f"{messages.DB_ERROR_FETCH_COLUMN} {column_name}", 
                params
            )
        ]

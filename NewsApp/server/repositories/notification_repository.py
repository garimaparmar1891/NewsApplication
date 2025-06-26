from datetime import datetime
from utils.db import get_db_connection
from queries import notification_queries as q


class NotificationRepository:
    def update_user_preferences(self, user_id, preferences):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                for pref in preferences:
                    category_id = pref.get("categoryId")
                    is_enabled = pref.get("isEnabled", True)
                    cursor.execute(
                        q.UPSERT_NOTIFICATION_PREF,
                        (user_id, category_id, is_enabled, user_id, category_id, is_enabled)
                    )
                conn.commit()
            return True
        except Exception as e:
            print("[Preferences Update Error]:", e)
            return False

    def get_enabled_category_ids(self, user_id):
        return self._fetch_column(q.GET_ENABLED_CATEGORIES, (user_id,), "CategoryId")

    def get_user_preferences(self, user_id):
        rows = self._execute_query(q.GET_USER_PREFERENCES, (user_id,))
        return [
            {
                "categoryId": row.CategoryId,
                "CategoryName": row.CategoryName,
                "isEnabled": bool(row.IsEnabled)
            }
            for row in rows
        ]


    def get_user_keywords(self, user_id):
        rows = self._execute_query(q.GET_USER_KEYWORDS, (user_id,))
        return [{"categoryId": row.CategoryId, "keyword": row.Keyword.lower()} for row in rows]

    def add_user_keyword(self, user_id, category_id, keyword):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(q.CHECK_USER_KEYWORD_EXISTS, (user_id, category_id, keyword))
                if cursor.fetchone():
                    return False
                cursor.execute(q.INSERT_USER_KEYWORD, (user_id, category_id, keyword))
                conn.commit()
                return True
        except Exception as e:
            print(f"[Add Keyword Error]: {e}")
            return False


    def get_unsent_articles_by_keywords(self, user_id, keyword_map):
        if not keyword_map:
            return []

        results = []
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for category_id, keywords in keyword_map.items():
                for keyword in keywords:
                    like_kw = f"%{keyword.lower()}%"
                    cursor.execute(q.GET_UNSENT_ARTICLES, (user_id, category_id, like_kw, like_kw))
                    for row in cursor.fetchall():
                        results.append({
                            "Id": row.Id,
                            "Title": row.Title,
                            "Content": row.Content,
                            "PublishedAt": row.PublishedAt.strftime("%Y-%m-%d %H:%M"),
                            "CategoryId": row.CategoryId,
                            "Source": row.Source,
                            "Url": row.Url
                        })
        return results

    def get_articles_by_categories(self, user_id, category_ids):
        if not category_ids:
            return []
        placeholders = ",".join(["?"] * len(category_ids))
        query = q.GET_ARTICLES_BY_CATEGORIES.format(placeholders=placeholders)
        return self._fetch_dict(query, [user_id] + category_ids)

    def mark_articles_as_sent(self, user_id, article_ids):
        if not article_ids:
            return
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for article_id in article_ids:
                cursor.execute(q.MARK_ARTICLE_AS_SENT, (user_id, article_id, user_id, article_id))
            conn.commit()


    def get_unread_user_notifications(self, user_id):
        rows = self._execute_query(q.GET_UNREAD_NOTIFICATIONS, (user_id,))
        return [
            {
                "notification_id": row.Id,
                "article_id": row.ArticleId,
                "title": row.Title,
                "source": row.Source,
                "message": row.Message,
                "created_at": row.CreatedAt
            }
            for row in rows
        ]

    def mark_notifications_as_read(self, user_id):
        self._execute_query_with_commit(q.MARK_NOTIFICATIONS_AS_READ, (user_id,))

    def insert_notification(self, user_id, article_id, message):
        self._execute_query_with_commit(q.INSERT_NOTIFICATION, (user_id, article_id, message))


    def get_users_with_enabled_preferences(self):
        rows = self._execute_query(q.GET_USERS_WITH_PREFS)
        return [{"user_id": row.Id, "email": row.Email, "username": row.Username} for row in rows]

    def get_last_login(self, user_id):
        row = self._execute_query(q.GET_LAST_LOGIN, (user_id,))
        return row[0][0] if row else None


    def _execute_query(self, query, params=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            return cursor.fetchall()

    def _fetch_dict(self, query, params=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def _fetch_column(self, query, params, column_name):
        rows = self._execute_query(query, params)
        return [getattr(row, column_name) for row in rows]

    def _execute_query_with_commit(self, query, params=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            conn.commit()

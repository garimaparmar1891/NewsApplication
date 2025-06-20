from utils.db import get_db_connection
from queries import notification_queries as q
from datetime import datetime

class NotificationRepository:

    def get_last_login(self, user_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.GET_LAST_LOGIN, (user_id,))
            row = cursor.fetchone()
            return row[0] if row else None

    def get_notifications_since_last_login(self, user_id):
        last_login = self.get_last_login(user_id) or datetime(1900, 1, 1)
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.GET_NOTIFICATIONS_SINCE, (user_id, last_login))
            rows = cursor.fetchall()

            notifications = []
            notification_ids = []

            for row in rows:
                notifications.append({
                    "message": row.Message,
                    "createdAt": row.CreatedAt.strftime("%Y-%m-%d %H:%M")
                })
                notification_ids.append(row.Id)

            if notification_ids:
                mark_query = q.MARK_NOTIFICATIONS_READ(len(notification_ids))
                cursor.execute(mark_query, notification_ids)
                conn.commit()

            return notifications

    def update_user_preferences(self, user_id, preferences):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                for pref in preferences:
                    category_id = pref.get("categoryId")
                    is_enabled = pref.get("isEnabled", True)

                    cursor.execute(q.UPSERT_NOTIFICATION_PREF, (
                    user_id, category_id,            
                    is_enabled,                      
                    user_id, category_id, is_enabled
                ))

                conn.commit()
                return True
            except Exception as e:
                print("Update Preferences Error:", e)
                conn.rollback()
                return False

    def get_enabled_category_ids(self, user_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.GET_ENABLED_CATEGORIES, (user_id,))
            return [row.CategoryId for row in cursor.fetchall()]

    def get_user_keywords(self, user_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.GET_USER_KEYWORDS, (user_id,))
            return [{"categoryId": row.CategoryId, "keyword": row.Keyword.lower()} for row in cursor.fetchall()]

    def add_user_keyword(self, user_id, category_id, keyword):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(q.CHECK_USER_KEYWORD_EXISTS, (user_id, category_id, keyword))
                if cursor.fetchone():
                    return False
                cursor.execute(q.INSERT_USER_KEYWORD, (user_id, category_id, keyword))
                conn.commit()
                return True
            except Exception as e:
                print(f"Add UserKeyword Error: {e}")
                conn.rollback()
                return False

    def get_unsent_articles_by_keywords(self, user_id, keyword_map):
        if not keyword_map:
            return []

        with get_db_connection() as conn:
            cursor = conn.cursor()
            results = []

            for category_id in keyword_map.keys():
                query = q.GET_UNSENT_ARTICLES(1)
                cursor.execute(query, (category_id, user_id))
                results.extend([
                    {
                        "Id": row.Id,
                        "Title": row.Title,
                        "Content": row.Content,
                        "PublishedAt": row.PublishedAt.strftime("%Y-%m-%d %H:%M")
                    }
                    for row in cursor.fetchall()
                ])

            return results

    def mark_articles_as_sent(self, user_id, article_ids):
        if not article_ids:
            return
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for article_id in article_ids:
                cursor.execute(q.MARK_ARTICLE_AS_SENT, (user_id, article_id, user_id, article_id))
            conn.commit()

    def get_users_with_enabled_preferences(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.GET_USERS_WITH_PREFS)
            return [
                {"user_id": row.Id, "email": row.Email, "username": row.Username}
                for row in cursor.fetchall()
            ]

    def get_user_preferences(self, user_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.GET_USER_PREFERENCES, (user_id,))
            return [
                {
                    "categoryId": row.CategoryId,
                    "CategoryName": row.CategoryName,
                    "isEnabled": bool(row.IsEnabled)
                }
                for row in cursor.fetchall()
            ]

    def save_sent_notification(self, user_id, article_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.MARK_ARTICLE_AS_SENT, (user_id, article_id, user_id, article_id))
            conn.commit()

    def get_unread_notifications(self, user_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.GET_UNREAD_NOTIFICATIONS, (user_id,))
            rows = cursor.fetchall()
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
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.MARK_NOTIFICATIONS_AS_READ, (user_id,))
            conn.commit()

    def insert_notification(self, user_id, article_id, message):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.INSERT_NOTIFICATION, (user_id, article_id, message))
            conn.commit()


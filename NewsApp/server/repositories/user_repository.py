from utils.db import get_db_connection
from queries import user_queries as q

class UserRepository:
    def get_user_by_email(self, email):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.GET_USER_BY_EMAIL, (email,))
            row = cursor.fetchone()
            if row:
                return {
                    "Id": row.Id,
                    "Username": row.Username,
                    "Email": row.Email,
                    "PasswordHash": row.PasswordHash,
                    "Role": row.Role
                }
            return None

    def get_user_by_id(self, user_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.GET_USER_BY_ID, (user_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row.Id,
                    "username": row.Username,
                    "email": row.Email
                }
            return None

    def create_user(self, username, email, password_hash):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.CREATE_USER, (username, email, password_hash))
            conn.commit()

    def get_saved_articles(self, user_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.GET_SAVED_ARTICLES, (user_id,))
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
                for row in cursor.fetchall()
            ]

    def unsave_article(self, user_id, article_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.UNSAVE_ARTICLE, (user_id, article_id))
            conn.commit()
            return cursor.rowcount > 0

    def is_article_saved_by_user(self, user_id, article_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.CHECK_ARTICLE_SAVED, (user_id, article_id))
            result = cursor.fetchone()
            return result is not None

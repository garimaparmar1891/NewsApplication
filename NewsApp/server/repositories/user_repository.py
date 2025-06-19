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
                    "Email": row.Email,
                    "Username": row.Username,
                    "PasswordHash": row.PasswordHash,
                    "Role": row.Role
                }
            return None

    def create_user(self, username, email, password_hash):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.CREATE_USER, (username, email, password_hash))
            conn.commit()

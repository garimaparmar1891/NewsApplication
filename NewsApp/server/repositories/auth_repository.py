from utils.db import get_db_connection
from queries import user_queries as q


class AuthRepository:

    def get_user_by_email(self, email):
        row = self._fetch_one(q.GET_USER_BY_EMAIL, (email,))
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
        row = self._fetch_one(q.GET_USER_BY_ID, (user_id,))
        if row:
            return {
                "id": row.Id,
                "username": row.Username,
                "email": row.Email
            }
        return None

    def create_user(self, username, email, password_hash):
        self._execute_write(q.CREATE_USER, (username, email, password_hash))


    def _fetch_one(self, query, params):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()

    def _execute_write(self, query, params):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

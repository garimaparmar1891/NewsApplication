from utils.db import execute_write_query, fetch_one_query
from queries import user_queries as q
from constants import messages


class AuthRepository:

    def get_user_by_email(self, email):
        return fetch_one_query(q.GET_USER_BY_EMAIL, (email,))

    def get_user_by_id(self, user_id):
        return fetch_one_query(q.GET_USER_BY_ID, (user_id,))

    def create_user(self, username, email, password_hash):
        execute_write_query(q.CREATE_USER, (username, email, password_hash), messages.DB_ERROR_CREATE_USER)

    def get_admin_email(self):
        result = fetch_one_query(q.GET_ADMIN_EMAIL, error_msg=messages.DB_ERROR_GET_ADMIN_EMAIL)
        return result.Email if result else None

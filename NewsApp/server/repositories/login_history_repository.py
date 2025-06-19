from utils.db import get_db_connection
from queries import login_history_queries as q

class LoginHistoryRepository:
    def record_login(self, user_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.RECORD_LOGIN, (user_id,))
            conn.commit()

    def get_last_login(self, user_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.GET_LAST_LOGIN, (user_id,))
            row = cursor.fetchone()
            return row.LoginTime if row else None

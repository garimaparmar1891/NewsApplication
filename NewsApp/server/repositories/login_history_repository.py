from utils.db import execute_write_query
from queries import login_history_queries as q
from constants import messages

class LoginHistoryRepository:
    def record_login(self, user_id):
        execute_write_query(q.RECORD_LOGIN, (user_id,), messages.DB_ERROR_RECORD_LOGIN)

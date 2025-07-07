import pytest
from unittest.mock import patch
from repositories.login_history_repository import LoginHistoryRepository
from queries import login_history_queries
from constants import messages


class TestLoginHistoryRepository:
    
    @pytest.fixture
    def login_history_repository(self):
        return LoginHistoryRepository()

    @patch('repositories.login_history_repository.execute_write_query')
    def test_record_login_executes_insert_query(self, mock_execute, login_history_repository):
        user_id = 123
        
        login_history_repository.record_login(user_id)
        
        mock_execute.assert_called_once_with(
            login_history_queries.RECORD_LOGIN, 
            (user_id,), 
            messages.DB_ERROR_RECORD_LOGIN
        ) 
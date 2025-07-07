import pytest
from unittest.mock import Mock, patch
from repositories.auth_repository import AuthRepository
from queries import user_queries
from constants import messages


class TestAuthRepository:
    
    @pytest.fixture
    def auth_repository(self):
        return AuthRepository()
    
    @pytest.fixture
    def mock_user_row(self):
        row = Mock()
        row.Id = 1
        row.Username = "testuser"
        row.Email = "test@example.com"
        row.PasswordHash = "hashed_password"
        row.Role = "User"
        return row
    
    @pytest.fixture
    def mock_admin_row(self):
        row = Mock()
        row.Email = "admin@example.com"
        return row

    @patch('repositories.auth_repository.fetch_one_query')
    def test_get_user_by_email_returns_user_data(self, mock_fetch_one, auth_repository, mock_user_row):
        mock_fetch_one.return_value = mock_user_row
        
        result = auth_repository.get_user_by_email("test@example.com")
        
        assert result.Username == "testuser"

    @patch('repositories.auth_repository.fetch_one_query')
    def test_get_user_by_id_returns_user_data(self, mock_fetch_one, auth_repository, mock_user_row):
        mock_fetch_one.return_value = mock_user_row
        
        result = auth_repository.get_user_by_id(1)
        
        assert result.Email == "test@example.com"

    @patch('repositories.auth_repository.execute_write_query')
    def test_create_user_executes_insert_query(self, mock_execute, auth_repository):
        auth_repository.create_user("newuser", "new@example.com", "password_hash")
        
        mock_execute.assert_called_once()

    @patch('repositories.auth_repository.fetch_one_query')
    def test_get_admin_email_returns_admin_email(self, mock_fetch_one, auth_repository, mock_admin_row):
        mock_fetch_one.return_value = mock_admin_row
        
        result = auth_repository.get_admin_email()
        
        assert result == "admin@example.com"

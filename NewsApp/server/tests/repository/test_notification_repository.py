import pytest
from unittest.mock import Mock, patch, MagicMock
from repositories.notification_repository import NotificationRepository
from queries import notification_queries as q
from queries import user_keywords as uk
from queries import login_history_queries as lhq
from constants import messages


class TestNotificationRepository:
    
    @pytest.fixture
    def notification_repository(self):
        return NotificationRepository()
    
    @pytest.fixture
    def mock_preference_row(self):
        row = Mock()
        row.CategoryId = 1
        row.CategoryName = "Technology"
        row.IsEnabled = True
        return row
    
    @pytest.fixture
    def mock_keyword_row(self):
        row = Mock()
        row.CategoryId = 1
        row.Keyword = "AI"
        return row
    
    @pytest.fixture
    def mock_notification_row(self):
        row = Mock()
        row.Id = 1
        row.ArticleId = 100
        row.Title = "Test Article"
        row.Source = "Test Source"
        row.Message = "Test notification"
        row.CreatedAt = "2024-01-01 10:00:00"
        return row
    
    @pytest.fixture
    def mock_user_row(self):
        row = Mock()
        row.Id = 1
        row.Email = "test@example.com"
        row.Username = "testuser"
        return row

    @patch('repositories.notification_repository.get_db_connection')
    def test_update_user_preferences_commits_transaction(self, mock_connection, notification_repository):
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        preferences = [{"categoryId": 1, "isEnabled": True}]
        result = notification_repository.update_user_preferences(1, preferences)
        
        assert result is True
        mock_conn.commit.assert_called_once()

    @patch('repositories.notification_repository.fetch_all_query_with_params')
    def test_get_enabled_category_ids_returns_category_list(self, mock_fetch, notification_repository):
        mock_rows = [Mock(CategoryId=1), Mock(CategoryId=2)]
        mock_fetch.return_value = mock_rows
        
        result = notification_repository.get_enabled_category_ids(1)
        
        assert result == [1, 2]



    @patch('repositories.notification_repository.fetch_one_query')
    @patch('repositories.notification_repository.execute_write_query')
    def test_add_user_keyword_inserts_new_keyword(self, mock_execute, mock_fetch_one, notification_repository):
        mock_fetch_one.return_value = None
        
        result = notification_repository.add_user_keyword(1, 1, "AI")
        
        assert result is True
        mock_execute.assert_called_once()

    @patch('repositories.notification_repository.fetch_one_query')
    def test_add_user_keyword_returns_false_when_exists(self, mock_fetch_one, notification_repository):
        mock_fetch_one.return_value = Mock()
        
        result = notification_repository.add_user_keyword(1, 1, "AI")
        
        assert result is False

    @patch('repositories.notification_repository.fetch_all_query_with_params')
    def test_get_unsent_articles_returns_articles(self, mock_fetch, notification_repository):
        mock_article = Mock()
        mock_fetch.return_value = [mock_article]
        
        result = notification_repository.get_unsent_articles(1, 1, "AI")
        
        assert result == [mock_article]

    @patch('repositories.notification_repository.fetch_all_query_with_params')
    def test_get_articles_by_categories_returns_articles(self, mock_fetch, notification_repository):
        mock_article = Mock()
        mock_fetch.return_value = [mock_article]
        
        result = notification_repository.get_articles_by_categories(1, [1, 2])
        
        assert result == [mock_article]

    @patch('repositories.notification_repository.execute_write_query')
    def test_mark_articles_as_sent_calls_execute_for_each_article(self, mock_execute, notification_repository):
        notification_repository.mark_articles_as_sent(1, [100, 101])
        
        assert mock_execute.call_count == 2

    @patch('repositories.notification_repository.execute_write_query')
    def test_mark_notifications_as_read_executes_update(self, mock_execute, notification_repository):
        notification_repository.mark_notifications_as_read(1)
        
        mock_execute.assert_called_once()

    @patch('repositories.notification_repository.execute_write_query')
    def test_insert_notification_executes_insert(self, mock_execute, notification_repository):
        notification_repository.insert_notification(1, 100, "Test message")
        
        mock_execute.assert_called_once()


    @patch('repositories.notification_repository.fetch_one_query')
    def test_get_last_login_returns_login_time(self, mock_fetch_one, notification_repository):
        mock_fetch_one.return_value = ("2024-01-01 10:00:00",)
        
        result = notification_repository.get_last_login(1)
        
        assert result == "2024-01-01 10:00:00"

    @patch('repositories.notification_repository.fetch_one_query')
    def test_get_last_login_returns_none_when_no_login(self, mock_fetch_one, notification_repository):
        mock_fetch_one.return_value = None
        
        result = notification_repository.get_last_login(1)
        
        assert result is None 
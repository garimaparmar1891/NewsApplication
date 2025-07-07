import pytest
from unittest.mock import Mock, patch
from repositories.user_repository import UserRepository
from utils.custom_exceptions import AppError
from http import HTTPStatus
import pyodbc


class TestUserRepository:
    
    @pytest.fixture
    def user_repository(self):
        return UserRepository()
    
    @pytest.fixture
    def mock_article_row(self):
        # Create a simple list-like object that can be indexed
        row = [0]
        return row
    
    @pytest.fixture
    def mock_saved_article_row(self):
        # Create a custom object that supports both indexing and attributes
        class MockRow:
            def __init__(self):
                self.data = [1, "Test Article", "Test Content", "Test Source", "http://test.com", "Technology", "2024-01-01"]
                self.cursor_description = [('Id',), ('Title',), ('Content',), ('Source',), ('Url',), ('Category',), ('PublishedAt',)]
            
            def __getitem__(self, index):
                return self.data[index]
        
        return MockRow()

    @patch('repositories.user_repository.fetch_one_query')
    @patch('repositories.user_repository.execute_write_query')
    def test_save_article_success(self, mock_execute, mock_fetch_one, user_repository, mock_article_row):
        mock_fetch_one.return_value = mock_article_row
        
        result = user_repository.save_article(1, 1)
        
        assert result is True

    @patch('repositories.user_repository.execute_write_query')
    def test_unsave_article_success(self, mock_execute, user_repository):
        mock_execute.return_value = 1
        
        result = user_repository.unsave_article(1, 1)
        
        assert result == 1

    @patch('repositories.user_repository.fetch_one_query')
    def test_is_article_saved_by_user_returns_true(self, mock_fetch_one, user_repository):
        mock_fetch_one.return_value = Mock()
        
        result = user_repository.is_article_saved_by_user(1, 1)
        
        assert result is True

    @patch('repositories.user_repository.fetch_all_query_with_params')
    def test_get_saved_articles_returns_articles(self, mock_fetch_all, user_repository, mock_saved_article_row):
        mock_fetch_all.return_value = [mock_saved_article_row]
        
        result = user_repository.get_saved_articles(1)
        
        assert len(result) == 1

    @patch('repositories.user_repository.fetch_all_query_with_params')
    def test_get_visible_article_ids_returns_visible_ids(self, mock_fetch_all, user_repository):
        mock_fetch_all.return_value = [1, 2, 3]
        
        result = user_repository.get_visible_article_ids([1, 2, 3, 4])
        
        assert result == {1, 2, 3}

    @patch('repositories.user_repository.fetch_all_query_with_params')
    def test_get_saved_article_ids_returns_article_ids(self, mock_fetch_all, user_repository):
        mock_fetch_all.return_value = [(1,), (2,), (3,)]
        
        result = user_repository.get_saved_article_ids(1)
        
        assert result == [1, 2, 3]

    @patch('repositories.user_repository.fetch_one_query')
    def test_validate_article_exists_raises_error_when_article_not_found(self, mock_fetch_one, user_repository):
        mock_fetch_one.return_value = None
        
        with pytest.raises(AppError) as exc_info:
            user_repository._validate_article_exists(999)
        
        assert exc_info.value.status_code == HTTPStatus.NOT_FOUND

    @patch('repositories.user_repository.execute_write_query')
    def test_insert_saved_article_success(self, mock_execute, user_repository):
        user_repository._insert_saved_article(1, 1)
        
        mock_execute.assert_called_once()

    @patch('repositories.user_repository.execute_write_query')
    def test_insert_saved_article_raises_error_on_foreign_key_violation(self, mock_execute, user_repository):
        mock_execute.side_effect = pyodbc.IntegrityError("FOREIGN KEY constraint")
        
        with pytest.raises(AppError) as exc_info:
            user_repository._insert_saved_article(1, 999)
        
        assert exc_info.value.status_code == HTTPStatus.NOT_FOUND

    def test_map_row_to_dict_returns_dictionary(self, user_repository, mock_saved_article_row):
        result = user_repository._map_row_to_dict(mock_saved_article_row)
        
        assert isinstance(result, dict)
        assert result['Id'] == 1

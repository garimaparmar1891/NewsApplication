import pytest
from unittest.mock import Mock, patch
from repositories.user_keyword_repository import UserKeywordRepository


class TestUserKeywordRepository:
    
    @pytest.fixture
    def user_keyword_repository(self):
        return UserKeywordRepository()
    
    @pytest.fixture
    def mock_keyword_row(self):
        row = Mock()
        row.Id = 1
        row.Keyword = "technology"
        row.Category = "Tech"
        return row
    
    @pytest.fixture
    def mock_keyword_map_row(self):
        row = Mock()
        row.CategoryId = 1
        row.Keyword = "AI"
        return row

    @patch('repositories.user_keyword_repository.fetch_one_query')
    def test_check_user_keyword_exists_returns_result_when_keyword_exists(self, mock_fetch_one, user_keyword_repository):
        mock_fetch_one.return_value = Mock()
        
        result = user_keyword_repository.check_user_keyword_exists(1, 1, "technology")
        
        assert result is not None

    @patch('repositories.user_keyword_repository.execute_write_query')
    def test_insert_user_keyword_calls_execute_write_query(self, mock_execute, user_keyword_repository):
        user_keyword_repository.insert_user_keyword(1, 1, "technology")
        
        mock_execute.assert_called_once()

    @patch('repositories.user_keyword_repository.execute_write_query')
    def test_delete_user_keyword_calls_execute_write_query(self, mock_execute, user_keyword_repository):
        user_keyword_repository.delete_user_keyword(1, 1)
        
        mock_execute.assert_called_once()

    @patch('repositories.user_keyword_repository.fetch_all_query_with_params')
    def test_get_user_keywords_returns_mapped_keywords(self, mock_fetch_all, user_keyword_repository, mock_keyword_row):
        mock_fetch_all.return_value = [mock_keyword_row]
        
        result = user_keyword_repository.get_user_keywords(1)
        
        assert len(result) == 1

    @patch('repositories.user_keyword_repository.fetch_all_query_with_params')
    def test_get_user_keywords_map_returns_category_keyword_mapping(self, mock_fetch_all, user_keyword_repository, mock_keyword_map_row):
        mock_fetch_all.return_value = [mock_keyword_map_row]
        
        result = user_keyword_repository.get_user_keywords_map(1)
        
        assert result[1] == ["ai"]

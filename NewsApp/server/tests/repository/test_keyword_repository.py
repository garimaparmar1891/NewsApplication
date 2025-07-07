import pytest
from unittest.mock import Mock, patch
from repositories.keyword_repository import KeywordRepository


class TestKeywordRepository:
    
    @pytest.fixture
    def keyword_repository(self):
        return KeywordRepository()
    
    @pytest.fixture
    def mock_keyword_row(self):
        row = Mock()
        row.Id = 1
        row.Word = "Technology"
        row.CategoryId = 2
        return row

    @patch('repositories.keyword_repository.fetch_all_query')
    def test_get_all_keywords_returns_mapped_data(self, mock_fetch_all, keyword_repository, mock_keyword_row):
        expected_result = [{'id': 1, 'word': 'Technology', 'category_id': 2}]
        mock_fetch_all.return_value = expected_result
        
        result = keyword_repository.get_all_keywords()
        
        assert result[0]['word'] == "Technology"

    @patch('repositories.keyword_repository.execute_write_query')
    def test_add_keyword_executes_insert_query(self, mock_execute, keyword_repository):
        mock_execute.return_value = 1
        
        result = keyword_repository.add_keyword("AI", 1)
        
        assert result == 1

    @patch('repositories.keyword_repository.execute_write_query')
    def test_delete_keyword_executes_delete_query(self, mock_execute, keyword_repository):
        mock_execute.return_value = 1
        
        result = keyword_repository.delete_keyword("TestKeyword")
        
        assert result == 1

    def test_map_keyword_row_returns_correct_structure(self, keyword_repository, mock_keyword_row):
        result = keyword_repository._map_keyword_row(mock_keyword_row)
        
        assert result['id'] == 1 
import pytest
from unittest.mock import Mock, patch
from repositories.category_repository import CategoryRepository
from queries import category_queries
from constants import messages


class TestCategoryRepository:
    
    @pytest.fixture
    def category_repository(self):
        return CategoryRepository()
    
    @pytest.fixture
    def mock_category_row(self):
        return (1, "Technology")

    @patch('repositories.category_repository.fetch_one_query')
    def test_get_category_by_name_returns_category_data(self, mock_fetch_one, category_repository, mock_category_row):
        mock_fetch_one.return_value = mock_category_row
        
        result = category_repository.get_category_by_name("Technology")
        
        assert result == {"Id": 1, "Name": "Technology"}

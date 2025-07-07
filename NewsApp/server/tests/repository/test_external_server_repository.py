import pytest
from unittest.mock import Mock, patch
from repositories.external_server_repository import ExternalServerRepository
from queries import external_server_queries
from constants import messages


class TestExternalServerRepository:
    
    @pytest.fixture
    def external_server_repository(self):
        return ExternalServerRepository()
    
    @pytest.fixture
    def mock_server_row(self):
        row = Mock()
        row.Id = 1
        row.Name = "NewsAPI"
        row.ApiKey = "test_api_key"
        row.IsActive = 1
        row.LastAccessed = "2024-01-01 10:00:00"
        row.BaseUrl = "https://newsapi.org/v2/"
        return row

    @patch('repositories.external_server_repository.fetch_all_query')
    def test_get_keys_returns_mapped_server_data(self, mock_fetch_all, external_server_repository, mock_server_row):
        mock_fetch_all.return_value = [{"id": 1, "name": "NewsAPI", "api_key": "test_api_key", "is_active": 1, "last_accessed": "2024-01-01 10:00:00", "base_url": "https://newsapi.org/v2/"}]

        result = external_server_repository.get_keys()

        assert result[0]["name"] == "NewsAPI" 
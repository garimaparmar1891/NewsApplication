import pytest
from unittest.mock import patch, MagicMock
from services.external_news.external_api_config import ExternalAPIConfig

class TestExternalAPIConfig:
    @patch('services.external_news.external_api_config.ExternalServerRepository')
    def test_news_api_key_is_set_when_newsapi_present(self, mock_repo):
        mock_repo.return_value.get_keys.return_value = [
            {"name": "newsapi", "api_key": "test_newsapi_key"}
        ]
        config = ExternalAPIConfig()
        assert config.NEWS_API_KEY == "test_newsapi_key"

    @patch('services.external_news.external_api_config.ExternalServerRepository')
    def test_news_api_key_is_none_when_newsapi_absent(self, mock_repo):
        mock_repo.return_value.get_keys.return_value = [
            {"name": "thenewsapi", "api_key": "test_thenewsapi_key"}
        ]
        config = ExternalAPIConfig()
        assert config.NEWS_API_KEY is None

    @patch('services.external_news.external_api_config.ExternalServerRepository')
    def test_thenewsapi_token_is_set_when_thenewsapi_present(self, mock_repo):
        mock_repo.return_value.get_keys.return_value = [
            {"name": "thenewsapi", "api_key": "test_thenewsapi_key"}
        ]
        config = ExternalAPIConfig()
        assert config.THENEWSAPI_TOKEN == "test_thenewsapi_key"

    @patch('services.external_news.external_api_config.ExternalServerRepository')
    def test_thenewsapi_token_is_none_when_thenewsapi_absent(self, mock_repo):
        mock_repo.return_value.get_keys.return_value = [
            {"name": "newsapi", "api_key": "test_newsapi_key"}
        ]
        config = ExternalAPIConfig()
        assert config.THENEWSAPI_TOKEN is None 
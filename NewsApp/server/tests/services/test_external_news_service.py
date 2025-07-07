import pytest
from unittest.mock import MagicMock, patch
from services.external_news.external_news_service import ExternalNewsService

class TestExternalNewsService:
    @patch('services.external_news.external_news_service.AdminRepository')
    @patch('services.external_news.external_news_service.ArticleFetcher')
    @patch('services.external_news.external_news_service.ArticleInserter')
    def test_fetch_and_store_all_no_articles_found(self, mock_article_inserter, mock_article_fetcher, mock_admin_repo):
        service = ExternalNewsService()
        mock_admin_repo.return_value.get_external_servers.return_value = [{'is_active': True, 'name': 'TestSource'}]
        mock_article_fetcher.return_value.fetch.return_value = []
        service._log_summary = MagicMock()
        service.fetch_and_store_all()
        assert not service._log_summary.called

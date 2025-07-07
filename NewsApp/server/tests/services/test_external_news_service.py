import pytest
from unittest.mock import MagicMock, patch
from services.external_news.external_news_service import ExternalNewsService

class TestExternalNewsService:
    @patch('services.external_news.external_news_service.AdminRepository')
    @patch('services.external_news.external_news_service.ArticleFetcher')
    @patch('services.external_news.external_news_service.ArticleInserter')
    @patch('services.external_news.external_news_service.NotificationManager')
    def test_fetch_and_store_all_inserts_articles(self, mock_notification_manager, mock_article_inserter, mock_article_fetcher, mock_admin_repo):
        service = ExternalNewsService()
        mock_admin_repo.return_value.get_external_servers.return_value = [{'is_active': True, 'name': 'TestSource'}]
        mock_article_fetcher.return_value.fetch.return_value = ['article1']
        mock_article_inserter.return_value.insert.return_value = ([1], ['article1'])
        service.notification_manager = MagicMock()
        service._log_summary = MagicMock()
        service.fetch_and_store_all()
        assert service._log_summary.called

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

    def test_log_summary_prints_total_inserted(self, capsys):
        service = ExternalNewsService()
        service._log_summary(5, {})
        captured = capsys.readouterr()
        assert "Total articles inserted: 5" in captured.out

    def test_log_summary_prints_notification_summary(self, capsys):
        service = ExternalNewsService()
        user_notification_count = {'user@example.com': 3}
        service._log_summary(0, user_notification_count)
        captured = capsys.readouterr()
        assert "Notification summary:" in captured.out 
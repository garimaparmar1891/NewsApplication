import pytest
from unittest.mock import MagicMock
from services.external_news.notification_manager import ArticleFormatter, EmailBuilder, ArticleMatcher, NotificationProcessor, NotificationManager

class TestArticleFormatter:
    def test_format_article_row_valid(self):
        row = [1, 'Title', 'Content', 'Source', 'Url', 2, '2023-01-01']
        result = ArticleFormatter.format_article_row(row)
        assert result["Id"] == 1

    def test_format_article_row_invalid(self):
        result = ArticleFormatter.format_article_row(None)
        assert result == {}

class TestEmailBuilder:
    def test_build_digest_email_returns_body(self):
        articles = [{"Title": "T", "Content": "C", "Source": "S", "Url": "U", "CategoryId": 1, "PublishedAt": "P"}]
        body = EmailBuilder.build_digest_email("user", articles)
        assert "Hi user" in body

    def test_build_digest_email_empty_articles(self):
        body = EmailBuilder.build_digest_email("user", [])
        assert "matched articles" in body

class TestArticleMatcher:
    @pytest.fixture
    def matcher(self):
        repo = MagicMock()
        return ArticleMatcher(repo)

    def test_get_matched_articles_for_user_keywords(self, matcher):
        matcher._get_articles_by_keywords = MagicMock(return_value=[{"Id": 1}])
        result = matcher.get_matched_articles_for_user(1)
        assert result == [{"Id": 1}]

    def test_get_matched_articles_for_user_categories(self, matcher):
        matcher._get_articles_by_keywords = MagicMock(return_value=[])
        matcher._get_articles_by_categories = MagicMock(return_value=[{"Id": 2}])
        result = matcher.get_matched_articles_for_user(1)
        assert result == [{"Id": 2}]

class TestNotificationProcessor:
    @pytest.fixture
    def processor(self):
        repo = MagicMock()
        service = MagicMock()
        return NotificationProcessor(repo, service)

    def test_process_user_notifications_no_user(self, processor):
        processor._get_user_data = MagicMock(return_value=None)
        result = processor.process_user_notifications(1)
        assert result == 0

    def test_process_user_notifications_success(self, processor):
        processor._get_user_data = MagicMock(return_value={"id": 1, "username": "u", "email": "e"})
        processor.article_matcher.get_matched_articles_for_user = MagicMock(return_value=[{"Id": 1}])
        processor._send_email_digest = MagicMock(return_value=True)
        processor._mark_articles_sent = MagicMock()
        processor._create_notifications_for_sent_articles = MagicMock()
        result = processor.process_user_notifications(1)
        assert result == 1

class TestNotificationManager:
    @pytest.fixture
    def manager(self):
        repo = MagicMock()
        service = MagicMock()
        return NotificationManager(repo, service)

    def test_check_and_notify_users_no_articles(self, manager):
        user_notification_count = {}
        result = manager.check_and_notify_users([], user_notification_count)
        assert result is None

    def test_check_and_notify_users_with_users(self, manager):
        manager.notification_repo.get_users_with_enabled_preferences.return_value = [{"user_id": 1, "email": "e"}]
        manager.notification_processor.process_user_notifications = MagicMock(return_value=2)
        user_notification_count = {}
        manager.check_and_notify_users([{"Id": 1}], user_notification_count)
        assert user_notification_count["e"] == 2 

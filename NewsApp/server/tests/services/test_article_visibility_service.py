import pytest
from unittest.mock import Mock, patch
from services.article_visibility_service import ArticleVisibilityService
from utils.custom_exceptions import AppError
from http import HTTPStatus
from constants import messages


class TestArticleVisibilityService:
    
    @pytest.fixture
    def mock_article_visibility_repository(self):
        return Mock()
    
    @pytest.fixture
    def mock_article_repository(self):
        return Mock()
    
    @pytest.fixture
    def mock_auth_repository(self):
        return Mock()
    
    @pytest.fixture
    def mock_admin_notifier(self):
        return Mock()
    
    @pytest.fixture
    def article_visibility_service(self, mock_article_visibility_repository, mock_article_repository, mock_auth_repository, mock_admin_notifier, app_context):
        with patch('services.article_visibility_service.ArticleVisibilityRepository', return_value=mock_article_visibility_repository), \
             patch('services.article_visibility_service.ArticleRepository', return_value=mock_article_repository), \
             patch('services.article_visibility_service.AuthRepository', return_value=mock_auth_repository), \
             patch('services.article_visibility_service.AdminNotifier', return_value=mock_admin_notifier):
            service = ArticleVisibilityService()
            return service

    def test_report_article_success(self, article_visibility_service, mock_article_visibility_repository, mock_article_repository, mock_auth_repository, mock_admin_notifier):
        mock_article_repository.get_article_by_id.return_value = {'Title': 'Test Article'}
        mock_auth_repository.get_user_by_id.return_value = (1, 'testuser', 'test@example.com')
        mock_article_visibility_repository.get_report_count.return_value = 1
        
        response, status_code = article_visibility_service.report_article(1, 1, 'Inappropriate content')
        
        assert status_code == 200
        assert response.json['message'] == messages.ARTICLE_REPORTED_SUCCESS

    def test_report_article_already_reported(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.add_report.side_effect = ValueError('Article already reported')
        
        with pytest.raises(AppError) as exc_info:
            article_visibility_service.report_article(1, 1, 'Inappropriate content')
        
        assert exc_info.value.status_code == HTTPStatus.CONFLICT

    def test_report_article_missing_fields(self, article_visibility_service):
        with pytest.raises(AppError) as exc_info:
            article_visibility_service.report_article(None, 1, 'Inappropriate content')
        
        assert exc_info.value.message == messages.REPORT_FIELDS_REQUIRED

    def test_get_all_reported_articles_success(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.get_all_reported_articles.return_value = [{'id': 1, 'title': 'Test'}]
        
        response, status_code = article_visibility_service.get_all_reported_articles()
        
        assert status_code == 200
        assert response.json['data'] == [{'id': 1, 'title': 'Test'}]

    def test_get_all_reported_articles_empty_list(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.get_all_reported_articles.return_value = []
        
        response, status_code = article_visibility_service.get_all_reported_articles()
        
        assert status_code == 200
        assert response.json['data'] == []

    def test_get_all_reported_articles_calls_repository(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.get_all_reported_articles.return_value = []
        article_visibility_service.get_all_reported_articles()
        
        mock_article_visibility_repository.get_all_reported_articles.assert_called_once()

    def test_hide_article_success(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.article_exists.return_value = True
        
        response, status_code = article_visibility_service.hide_article(1)
        
        assert status_code == 200
        assert response.json['message'] == messages.ARTICLE_HIDDEN_SUCCESS

    def test_hide_article_not_found(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.article_exists.return_value = False
        
        with pytest.raises(AppError) as exc_info:
            article_visibility_service.hide_article(1)
        
        assert exc_info.value.message == messages.ARTICLE_NOT_FOUND

    def test_hide_article_calls_repository(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.article_exists.return_value = True
        article_visibility_service.hide_article(1)
        
        mock_article_visibility_repository.hide_article.assert_called_once_with(1)

    def test_unhide_article_success(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.article_exists.return_value = True
        
        response, status_code = article_visibility_service.unhide_article(1)
        
        assert status_code == 200
        assert response.json['message'] == messages.ARTICLE_UNHIDDEN_SUCCESS

    def test_unhide_article_not_found(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.article_exists.return_value = False
        
        with pytest.raises(AppError) as exc_info:
            article_visibility_service.unhide_article(1)
        
        assert exc_info.value.message == messages.ARTICLE_NOT_FOUND

    def test_unhide_article_clears_reports(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.article_exists.return_value = True
        article_visibility_service.unhide_article(1)
        
        mock_article_visibility_repository.clear_article_reports.assert_called_once_with(1)

    def test_toggle_article_visibility_hide(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.article_exists.return_value = True
        
        response, status_code = article_visibility_service.toggle_article_visibility(1, 'hide')
        
        assert status_code == 200
        assert response.json['message'] == messages.ARTICLE_HIDDEN_SUCCESS

    def test_toggle_article_visibility_unhide(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.article_exists.return_value = True
        
        response, status_code = article_visibility_service.toggle_article_visibility(1, 'unhide')
        
        assert status_code == 200
        assert response.json['message'] == messages.ARTICLE_UNHIDDEN_SUCCESS

    def test_toggle_article_visibility_invalid_action(self, article_visibility_service):
        with pytest.raises(AppError) as exc_info:
            article_visibility_service.toggle_article_visibility(1, 'invalid')
        
        assert exc_info.value.message == messages.INVALID_VISIBILITY_ACTION

    def test_hide_category_success(self, article_visibility_service, mock_article_visibility_repository):
        response, status_code = article_visibility_service.hide_category(1)
        
        assert status_code == 200
        assert response.json['message'] == messages.CATEGORY_HIDDEN_SUCCESS

    def test_hide_category_calls_repository(self, article_visibility_service, mock_article_visibility_repository):
        article_visibility_service.hide_category(1)
        
        mock_article_visibility_repository.hide_category.assert_called_once_with(1)

    def test_hide_category_returns_success_response(self, article_visibility_service, mock_article_visibility_repository):
        response, status_code = article_visibility_service.hide_category(1)
        
        assert hasattr(response, 'json')
        assert 'message' in response.json

    def test_unhide_category_success(self, article_visibility_service, mock_article_visibility_repository):
        response, status_code = article_visibility_service.unhide_category(1)
        
        assert status_code == 200
        assert response.json['message'] == messages.CATEGORY_UNHIDDEN_SUCCESS

    def test_unhide_category_calls_repository(self, article_visibility_service, mock_article_visibility_repository):
        article_visibility_service.unhide_category(1)
        
        mock_article_visibility_repository.unhide_category.assert_called_once_with(1)

    def test_unhide_category_returns_success_response(self, article_visibility_service, mock_article_visibility_repository):
        response, status_code = article_visibility_service.unhide_category(1)
        
        assert hasattr(response, 'json')
        assert 'message' in response.json

    def test_toggle_category_visibility_hide(self, article_visibility_service, mock_article_visibility_repository):
        response, status_code = article_visibility_service.toggle_category_visibility(1, 'hide')
        
        assert status_code == 200
        assert response.json['message'] == messages.CATEGORY_HIDDEN_SUCCESS

    def test_toggle_category_visibility_unhide(self, article_visibility_service, mock_article_visibility_repository):
        response, status_code = article_visibility_service.toggle_category_visibility(1, 'unhide')
        
        assert status_code == 200
        assert response.json['message'] == messages.CATEGORY_UNHIDDEN_SUCCESS

    def test_toggle_category_visibility_invalid_action(self, article_visibility_service):
        with pytest.raises(AppError) as exc_info:
            article_visibility_service.toggle_category_visibility(1, 'invalid')
        
        assert exc_info.value.message == messages.INVALID_VISIBILITY_ACTION

    def test_add_blocked_keyword_success(self, article_visibility_service, mock_article_visibility_repository):
        response, status_code = article_visibility_service.add_blocked_keyword('spam')
        
        assert status_code == 200
        assert response.json['message'] == messages.BLOCKED_KEYWORD_ADDED

    def test_add_blocked_keyword_missing_keyword(self, article_visibility_service):
        with pytest.raises(AppError) as exc_info:
            article_visibility_service.add_blocked_keyword(None)
        
        assert exc_info.value.message == messages.KEYWORD_REQUIRED

    def test_add_blocked_keyword_calls_repository(self, article_visibility_service, mock_article_visibility_repository):
        article_visibility_service.add_blocked_keyword('spam')
        
        mock_article_visibility_repository.add_blocked_keyword.assert_called_once_with('spam')

    def test_get_blocked_keywords_success(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.get_blocked_keywords.return_value = [{'id': 1, 'keyword': 'spam'}]
        
        response, status_code = article_visibility_service.get_blocked_keywords()
        
        assert status_code == 200
        assert response.json['data'] == [{'id': 1, 'keyword': 'spam'}]

    def test_get_blocked_keywords_empty_list(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.get_blocked_keywords.return_value = []
        
        response, status_code = article_visibility_service.get_blocked_keywords()
        
        assert status_code == 200
        assert response.json['data'] == []

    def test_get_blocked_keywords_calls_repository(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.get_blocked_keywords.return_value = []
        article_visibility_service.get_blocked_keywords()
        
        mock_article_visibility_repository.get_blocked_keywords.assert_called_once()

    def test_delete_blocked_keyword_success(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.delete_blocked_keyword.return_value = 1
        
        response, status_code = article_visibility_service.delete_blocked_keyword(1)
        
        assert status_code == 200
        assert response.json['message'] == messages.BLOCKED_KEYWORD_DELETED

    def test_delete_blocked_keyword_not_found(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.delete_blocked_keyword.return_value = 0
        
        with pytest.raises(AppError) as exc_info:
            article_visibility_service.delete_blocked_keyword(1)
        
        assert exc_info.value.message == messages.KEYWORD_NOT_FOUND

    def test_delete_blocked_keyword_unhides_articles(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.delete_blocked_keyword.return_value = 1
        article_visibility_service.delete_blocked_keyword(1)
        
        mock_article_visibility_repository.unhide_articles_after_keyword_removal.assert_called_once()

    def test_is_article_blocked_true(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.is_keyword_blocked.return_value = True
        
        response, status_code = article_visibility_service.is_article_blocked('spam content')
        
        assert status_code == 200
        assert response.json['data']['blocked'] is True

    def test_is_article_blocked_false(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.is_keyword_blocked.return_value = False
        
        response, status_code = article_visibility_service.is_article_blocked('normal content')
        
        assert status_code == 200
        assert response.json['data']['blocked'] is False

    def test_is_article_blocked_calls_repository(self, article_visibility_service, mock_article_visibility_repository):
        mock_article_visibility_repository.is_keyword_blocked.return_value = False
        article_visibility_service.is_article_blocked('test content')
        
        mock_article_visibility_repository.is_keyword_blocked.assert_called_once_with('test content')

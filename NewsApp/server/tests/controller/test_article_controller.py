import pytest
from unittest.mock import Mock, patch
from controllers.article_controller import ArticleController
from utils.custom_exceptions import AppError


class TestArticleController:
    
    @pytest.fixture
    def article_controller(self):
        return ArticleController()
    
    @pytest.fixture
    def mock_article_service(self, article_controller):
        with patch.object(article_controller, 'article_service') as mock_service:
            yield mock_service
    
    @pytest.fixture
    def mock_request(self):
        with patch('controllers.article_controller.request') as mock_req:
            yield mock_req
    
    @pytest.fixture
    def mock_get_user_id(self, article_controller):
        with patch.object(article_controller, '_get_user_id') as mock_user_id:
            mock_user_id.return_value = 1
            yield mock_user_id
    
    @pytest.fixture
    def mock_get_request_param(self, article_controller):
        with patch.object(article_controller, '_get_request_param') as mock_param:
            yield mock_param
    
    @pytest.fixture
    def mock_get_validated_date_params(self, article_controller):
        with patch.object(article_controller, '_get_validated_date_params') as mock_date:
            yield mock_date
    
    def test_search_articles_by_keyword_and_range_returns_service_response(
        self, article_controller, mock_article_service, mock_get_user_id, 
        mock_get_request_param, mock_get_validated_date_params
    ):
        mock_get_request_param.return_value = "technology"
        mock_get_validated_date_params.return_value = {
            'start_date': '2024-01-01',
            'end_date': '2024-01-31'
        }
        expected_response = {"data": [{"id": 1, "title": "Tech News"}]}
        mock_article_service.search_articles_by_keyword_and_range.return_value = expected_response
        
        result = article_controller.search_articles_by_keyword_and_range()
        
        assert result == expected_response
    
    def test_get_today_headlines_returns_service_response(
        self, article_controller, mock_article_service, mock_get_user_id
    ):
        expected_response = {"data": [{"id": 1, "title": "Today's Headlines"}]}
        mock_article_service.get_today_headlines.return_value = expected_response
        
        result = article_controller.get_today_headlines()
        
        assert result == expected_response
    
    def test_get_all_categories_returns_service_response(
        self, article_controller, mock_article_service
    ):
        expected_response = {"data": [{"id": 1, "name": "Technology"}]}
        mock_article_service.get_all_categories.return_value = expected_response
        
        result = article_controller.get_all_categories()
        
        assert result == expected_response
    
    def test_get_all_articles_returns_service_response(
        self, article_controller, mock_article_service, mock_get_user_id
    ):
        expected_response = {"data": [{"id": 1, "title": "Article"}]}
        mock_article_service.get_all_articles.return_value = expected_response
        
        result = article_controller.get_all_articles()
        
        assert result == expected_response
    
    def test_record_article_read_returns_service_response(
        self, article_controller, mock_article_service, mock_get_user_id
    ):
        article_id = 1
        expected_response = {"message": "Article read recorded"}
        mock_article_service.record_article_read.return_value = expected_response
        
        result = article_controller.record_article_read(article_id)
        
        assert result == expected_response

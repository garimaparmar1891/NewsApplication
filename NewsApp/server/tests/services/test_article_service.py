import pytest
from unittest.mock import Mock, patch
from services.article_service import ArticleService
from utils.custom_exceptions import AppError
from http import HTTPStatus
from constants import messages
from datetime import datetime, date


class TestArticleService:
    
    @pytest.fixture
    def article_service(self, mock_article_repository, mock_category_repository, mock_recommendation_service, app_context):
        return ArticleService()
    
    @pytest.fixture
    def mock_article_repository(self):
        with patch('services.article_service.ArticleRepository') as mock_repo:
            yield mock_repo.return_value
    
    @pytest.fixture
    def mock_category_repository(self):
        with patch('services.article_service.CategoryRepository') as mock_repo:
            yield mock_repo.return_value
    
    @pytest.fixture
    def mock_recommendation_service(self):
        with patch('services.article_service.RecommendationService') as mock_service:
            yield mock_service.return_value
    
    @pytest.fixture
    def sample_articles(self):
        return [
            {
                "Id": 1,
                "Title": "Test Article 1",
                "Content": "Test content 1",
                "Source": "Test Source",
                "Url": "http://test.com/1",
                "CategoryId": 1,
                "PublishedAt": datetime.now(),
                "server_id": 1,
                "is_hidden": 0
            },
            {
                "Id": 2,
                "Title": "Test Article 2",
                "Content": "Test content 2",
                "Source": "Test Source",
                "Url": "http://test.com/2",
                "CategoryId": 2,
                "PublishedAt": datetime.now(),
                "server_id": 1,
                "is_hidden": 0
            }
        ]
    
    @pytest.fixture
    def sample_categories(self):
        return [
            {"Id": 1, "name": "Technology"},
            {"Id": 2, "name": "Sports"},
            {"Id": 3, "name": "Business"}
        ]

    def test_search_articles_by_keyword_and_range_success(self, article_service, mock_article_repository, sample_articles):
        search_params = {"keyword": "test", "start_date": "2024-01-01", "end_date": "2024-01-31"}
        mock_article_repository.search_articles_by_keyword_and_range.return_value = sample_articles
        
        response, status_code = article_service.search_articles_by_keyword_and_range(search_params)
        
        assert status_code == 200
        assert len(response.json['data']) == 2

    def test_search_articles_by_keyword_and_range_empty_result(self, article_service, mock_article_repository):
        search_params = {"keyword": "nonexistent", "start_date": "2024-01-01", "end_date": "2024-01-31"}
        mock_article_repository.search_articles_by_keyword_and_range.return_value = []
        
        with patch.object(article_service, '_respond_with_articles') as mock_respond:
            mock_respond.return_value = (Mock(json={'message': messages.NO_ARTICLES_FOR_KEYWORD}), 404)
            response, status_code = article_service.search_articles_by_keyword_and_range(search_params)
        
        assert status_code == 404
        assert response.json['message'] == messages.NO_ARTICLES_FOR_KEYWORD

    def test_search_articles_by_keyword_and_range_invalid_date_range(self, article_service):
        search_params = {"keyword": "test", "start_date": "2024-01-31", "end_date": "2024-01-01"}
        
        with pytest.raises(AppError) as exc_info:
            article_service.search_articles_by_keyword_and_range(search_params)
        
        assert exc_info.value.message == messages.INVALID_DATE_RANGE

    def test_get_today_headlines_success(self, article_service, mock_article_repository, sample_articles):
        mock_article_repository.get_today_headlines.return_value = sample_articles
        
        response, status_code = article_service.get_today_headlines()
        
        assert status_code == 200
        assert len(response.json['data']) == 2

    def test_get_today_headlines_empty_result(self, article_service, mock_article_repository):
        mock_article_repository.get_today_headlines.return_value = []
        
        with patch.object(article_service, '_respond_with_articles') as mock_respond:
            mock_respond.return_value = (Mock(json={'message': messages.NO_HEADLINES_AVAILABLE}), 404)
            response, status_code = article_service.get_today_headlines()
        
        assert status_code == 404
        assert response.json['message'] == messages.NO_HEADLINES_AVAILABLE

    def test_get_today_headlines_with_user_id(self, article_service, mock_article_repository, mock_recommendation_service, sample_articles):
        mock_article_repository.get_today_headlines.return_value = sample_articles
        formatted_articles = [
            {"Id": "1", "Title": "Test Article 1", "Content": "Test content 1", "Source": "Test Source", "Url": "http://test.com/1", "Category": "", "CategoryId": "1", "PublishedAt": "2024-01-01 10:00"},
            {"Id": "2", "Title": "Test Article 2", "Content": "Test content 2", "Source": "Test Source", "Url": "http://test.com/2", "Category": "", "CategoryId": "2", "PublishedAt": "2024-01-01 10:00"}
        ]
        mock_recommendation_service.score_and_sort_articles.return_value = formatted_articles
        
        response, status_code = article_service.get_today_headlines(user_id=1)
        
        assert status_code == 200
        mock_recommendation_service.score_and_sort_articles.assert_called_once()

    def test_get_articles_by_range_success(self, article_service, mock_article_repository, mock_category_repository, sample_articles, sample_categories):
        date_range = {"start_date": "2024-01-01", "end_date": "2024-01-31"}
        category_names = ["Technology", "Sports"]
        mock_category_repository.get_category_by_name.side_effect = lambda name: next((cat for cat in sample_categories if cat["name"] == name), None)
        mock_article_repository.get_articles_by_range.return_value = sample_articles
        
        response, status_code = article_service.get_articles_by_range(date_range, category_names)
        
        assert status_code == 200
        assert len(response.json['data']) == 2

    def test_get_articles_by_range_empty_result(self, article_service, mock_article_repository, mock_category_repository):
        date_range = {"start_date": "2024-01-01", "end_date": "2024-01-31"}
        category_names = ["Technology"]
        mock_category_repository.get_category_by_name.return_value = {"Id": 1, "name": "Technology"}
        mock_article_repository.get_articles_by_range.return_value = []
        
        with patch.object(article_service, '_respond_with_articles') as mock_respond:
            mock_respond.return_value = (Mock(json={'message': messages.NO_ARTICLES_IN_RANGE}), 404)
            response, status_code = article_service.get_articles_by_range(date_range, category_names)
        
        assert status_code == 404
        assert response.json['message'] == messages.NO_ARTICLES_IN_RANGE

    def test_get_articles_by_range_single_category_string(self, article_service, mock_article_repository, mock_category_repository, sample_articles):
        date_range = {"start_date": "2024-01-01", "end_date": "2024-01-31"}
        category_names = "Technology"
        mock_category_repository.get_category_by_name.return_value = {"Id": 1, "name": "Technology"}
        mock_article_repository.get_articles_by_range.return_value = sample_articles
        
        response, status_code = article_service.get_articles_by_range(date_range, category_names)
        
        assert status_code == 200
        mock_article_repository.get_articles_by_range.assert_called_once_with("2024-01-01", "2024-01-31", [1])

    def test_get_all_categories_success(self, article_service, mock_article_repository, sample_categories):
        mock_article_repository.get_all_categories.return_value = sample_categories
        
        response, status_code = article_service.get_all_categories()
        
        assert status_code == 200
        assert response.json['data'] == sample_categories

    def test_get_all_categories_calls_repository(self, article_service, mock_article_repository, sample_categories):
        mock_article_repository.get_all_categories.return_value = sample_categories
        article_service.get_all_categories()
        
        mock_article_repository.get_all_categories.assert_called_once()

    def test_get_all_categories_empty_result(self, article_service, mock_article_repository):
        mock_article_repository.get_all_categories.return_value = []
        
        response, status_code = article_service.get_all_categories()
        
        assert status_code == 200
        assert response.json['data'] == []

    def test_record_article_read_success(self, article_service, mock_article_repository):
        mock_article_repository.record_article_read.return_value = True
        
        response, status_code = article_service.record_article_read(1, 1)
        
        assert status_code == 200
        assert response.json['message'] == messages.READ_RECORDED

    def test_record_article_read_failure(self, article_service, mock_article_repository):
        mock_article_repository.record_article_read.return_value = False
        
        with pytest.raises(AppError) as exc_info:
            article_service.record_article_read(1, 1)
        
        assert exc_info.value.message == messages.READ_RECORD_FAILED
        assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

    def test_record_article_read_missing_fields(self, article_service):
        with pytest.raises(AppError) as exc_info:
            article_service.record_article_read(None, None)
        
        assert exc_info.value.message == messages.MISSING_REQUIRED_FIELDS

    def test_get_all_articles_success(self, article_service, mock_article_repository, sample_articles):
        mock_article_repository.get_all_articles.return_value = sample_articles
        
        response, status_code = article_service.get_all_articles()
        
        assert status_code == 200
        assert len(response.json['data']) == 2

    def test_get_all_articles_empty_result(self, article_service, mock_article_repository):
        mock_article_repository.get_all_articles.return_value = []
        
        with patch.object(article_service, '_respond_with_articles') as mock_respond:
            mock_respond.return_value = (Mock(json={'message': messages.NO_ARTICLES_FOUND}), 404)
            response, status_code = article_service.get_all_articles()
        
        assert status_code == 404
        assert response.json['message'] == messages.NO_ARTICLES_FOUND

    def test_get_all_articles_with_user_id(self, article_service, mock_article_repository, mock_recommendation_service, sample_articles):
        mock_article_repository.get_all_articles.return_value = sample_articles
        formatted_articles = [
            {"Id": "1", "Title": "Test Article 1", "Content": "Test content 1", "Source": "Test Source", "Url": "http://test.com/1", "Category": "", "CategoryId": "1", "PublishedAt": "2024-01-01 10:00"},
            {"Id": "2", "Title": "Test Article 2", "Content": "Test content 2", "Source": "Test Source", "Url": "http://test.com/2", "Category": "", "CategoryId": "2", "PublishedAt": "2024-01-01 10:00"}
        ]
        mock_recommendation_service.score_and_sort_articles.return_value = formatted_articles
        
        response, status_code = article_service.get_all_articles(user_id=1)
        
        assert status_code == 200
        mock_recommendation_service.score_and_sort_articles.assert_called_once()

    def test_bulk_insert_articles_success(self, article_service, mock_article_repository):
        articles = [
            {
                "title": "Test Article",
                "content": "Test content",
                "source": "Test Source",
                "url": "http://test.com",
                "category_id": 1,
                "published_at": "2024-01-01T10:00:00Z",
                "server_id": 1
            }
        ]
        mock_article_repository.get_blocked_keywords.return_value = []
        mock_article_repository.bulk_insert_articles.return_value = True
        
        result = article_service.bulk_insert_articles(articles)
        
        assert result is True

    def test_bulk_insert_articles_with_blocked_keywords(self, article_service, mock_article_repository):
        articles = [
            {
                "title": "Blocked Article",
                "content": "This contains blocked keyword",
                "source": "Test Source",
                "url": "http://test.com",
                "category_id": 1,
                "published_at": "2024-01-01T10:00:00Z",
                "server_id": 1
            }
        ]
        mock_article_repository.get_blocked_keywords.return_value = ["blocked"]
        mock_article_repository.bulk_insert_articles.return_value = True
        
        result = article_service.bulk_insert_articles(articles)
        
        assert result is True

    def test_bulk_insert_articles_calls_repository(self, article_service, mock_article_repository):
        articles = [
            {
                "title": "Test Article",
                "content": "Test content",
                "source": "Test Source",
                "url": "http://test.com",
                "category_id": 1,
                "published_at": "2024-01-01T10:00:00Z",
                "server_id": 1
            }
        ]
        mock_article_repository.get_blocked_keywords.return_value = []
        mock_article_repository.bulk_insert_articles.return_value = True
        
        article_service.bulk_insert_articles(articles)
        
        mock_article_repository.get_blocked_keywords.assert_called_once()
        mock_article_repository.bulk_insert_articles.assert_called_once()

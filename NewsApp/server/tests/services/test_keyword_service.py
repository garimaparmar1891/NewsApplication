import pytest
from unittest.mock import Mock, patch
from services.keyword_service import KeywordService
from utils.custom_exceptions import AppError
from http import HTTPStatus
from constants import messages


class TestKeywordService:
    
    @pytest.fixture
    def mock_repository(self):
        with patch('services.keyword_service.KeywordRepository') as mock_repo:
            yield mock_repo.return_value
    
    @pytest.fixture
    def keyword_service(self, mock_repository):
        return KeywordService()
    
    def test_get_all_keywords_success(self, keyword_service, mock_repository, app_context):
        mock_repository.get_all_keywords.return_value = [{"id": 1, "word": "test"}]
        
        response, status_code = keyword_service.get_all_keywords()
        
        assert status_code == 200
    
    def test_get_all_keywords_not_found(self, keyword_service, mock_repository, app_context):
        mock_repository.get_all_keywords.return_value = []
        
        with pytest.raises(AppError) as exc_info:
            keyword_service.get_all_keywords()
        
        assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    
    def test_add_keyword_success(self, keyword_service, mock_repository, app_context):
        mock_repository.add_keyword.return_value = 1
        
        response, status_code = keyword_service.add_keyword("test", 1)
        
        assert status_code == 200
    
    def test_add_keyword_failure(self, keyword_service, mock_repository, app_context):
        mock_repository.add_keyword.return_value = 0
        
        with pytest.raises(AppError) as exc_info:
            keyword_service.add_keyword("test", 1)
        
        assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    
    def test_delete_keyword_success(self, keyword_service, mock_repository, app_context):
        mock_repository.delete_keyword.return_value = 1
        
        response, status_code = keyword_service.delete_keyword("test")
        
        assert status_code == 200
    
    def test_delete_keyword_not_found(self, keyword_service, mock_repository, app_context):
        mock_repository.delete_keyword.return_value = 0
        
        with pytest.raises(AppError) as exc_info:
            keyword_service.delete_keyword("test")
        
        assert exc_info.value.status_code == HTTPStatus.NOT_FOUND 
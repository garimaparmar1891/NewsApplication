import pytest
from services.admin_service import AdminService
from utils.custom_exceptions import AppError
from http import HTTPStatus
from constants import messages


class TestAdminService:
    
    @pytest.fixture
    def admin_service(self, mock_admin_repository, app_context):
        return AdminService()
    
    def test_get_external_servers_success(self, admin_service, mock_admin_repository, sample_external_servers, app_context):
        mock_admin_repository.get_external_servers.return_value = sample_external_servers
        
        response, status_code = admin_service.get_external_servers()
        
        assert status_code == 200
        assert response.json['data'] == sample_external_servers
    
    def test_get_external_servers_calls_repository(self, admin_service, mock_admin_repository, sample_external_servers, app_context):
        mock_admin_repository.get_external_servers.return_value = sample_external_servers
        admin_service.get_external_servers()
        
        mock_admin_repository.get_external_servers.assert_called_once()
    
    def test_update_external_server_success(self, admin_service, mock_admin_repository, app_context):
        mock_admin_repository.update_external_server.return_value = True
        
        response, status_code = admin_service.update_external_server(1, {"name": "Updated"})
        
        assert status_code == 200
        assert response.json['message'] == messages.EXTERNAL_SERVER_UPDATED
    
    def test_update_external_server_failure(self, admin_service, mock_admin_repository, app_context):
        mock_admin_repository.update_external_server.return_value = False
        
        with pytest.raises(AppError) as exc_info:
            admin_service.update_external_server(1, {"name": "Updated"})
        
        assert exc_info.value.message == messages.EXTERNAL_SERVER_UPDATE_FAILED
        assert exc_info.value.status_code == HTTPStatus.BAD_REQUEST
    
    def test_get_categories_success(self, admin_service, mock_admin_repository, sample_categories, app_context):
        mock_admin_repository.get_categories.return_value = sample_categories
        
        response, status_code = admin_service.get_categories()
        
        assert status_code == 200
        assert response.json['data'] == sample_categories
    
    def test_get_categories_calls_repository(self, admin_service, mock_admin_repository, sample_categories, app_context):
        mock_admin_repository.get_categories.return_value = sample_categories
        admin_service.get_categories()
        
        mock_admin_repository.get_categories.assert_called_once()
    
    def test_add_category_success(self, admin_service, mock_admin_repository, app_context):
        mock_admin_repository.add_category.return_value = True
        
        response, status_code = admin_service.add_category("Technology")
        
        assert status_code == 200
        assert response.json['message'] == messages.CATEGORY_ADDED
    
    def test_add_category_failure(self, admin_service, mock_admin_repository, app_context):
        mock_admin_repository.add_category.return_value = False
        
        with pytest.raises(AppError) as exc_info:
            admin_service.add_category("Technology")
        
        assert exc_info.value.message == messages.CATEGORY_ADD_FAILED
        assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
 
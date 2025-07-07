import pytest
from unittest.mock import Mock, patch, MagicMock
from controllers.admin_controller import AdminController
from utils.custom_exceptions import AppError
from flask import request
from http import HTTPStatus
from flask import Flask

app = Flask(__name__)

class TestAdminController:
    
    @pytest.fixture
    def admin_controller(self):
        return AdminController()
    
    @pytest.fixture
    def mock_admin_service(self, admin_controller):
        with patch.object(admin_controller, 'admin_service') as mock_service:
            yield mock_service

    def test_get_external_servers_success(self, admin_controller, mock_admin_service):
        expected_response = {"data": [{"id": 1, "name": "NewsAPI"}]}
        mock_admin_service.get_external_servers.return_value = expected_response
        
        result = admin_controller.get_external_servers()
        
        assert result == expected_response
        mock_admin_service.get_external_servers.assert_called_once()

    def test_get_external_servers_service_exception(self, admin_controller, mock_admin_service):
        mock_admin_service.get_external_servers.side_effect = AppError("Service error", 500)
        
        result = admin_controller.get_external_servers()
        
        assert result == {"error": "Service error", "status_code": 500}

    def test_get_external_servers_general_exception(self, admin_controller, mock_admin_service):
        mock_admin_service.get_external_servers.side_effect = Exception("Unexpected error")
        
        result = admin_controller.get_external_servers()
        
        assert result == {"error": "Unexpected server error", "status_code": 500}

    def test_update_external_server_success(self, admin_controller, mock_admin_service):
        server_id = 1
        update_data = {"name": "UpdatedAPI", "url": "https://api.updated.com"}
        expected_response = {"message": "Server updated successfully"}
        mock_admin_service.update_external_server.return_value = expected_response
        
        with app.test_request_context():
            with patch('flask.request') as mock_request:
                mock_request.get_json.return_value = update_data
                with patch.object(admin_controller, '_validate_json_data', return_value=(update_data, None)):
                    result = admin_controller.update_external_server(server_id)
                    if isinstance(result, tuple):
                        response, status_code = result
                        assert response.get_json() == expected_response
                        assert status_code == 200
                    else:
                        assert result == expected_response
                    mock_admin_service.update_external_server.assert_called_once_with(server_id, update_data)

    def test_update_external_server_no_json_data(self, admin_controller, mock_admin_service):
        server_id = 1
        
        with app.test_request_context():
            with patch('flask.request') as mock_request:
                mock_request.get_json.return_value = None
                with patch.object(admin_controller, '_validate_json_data', return_value=(None, (None, 400))):
                    result = admin_controller.update_external_server(server_id)
                    if isinstance(result, tuple):
                        response, status_code = result
                        assert status_code == 400
                    else:
                        assert result[1] == 400 or result.get('status_code') == 400
                    mock_admin_service.update_external_server.assert_not_called()

    def test_update_external_server_service_exception(self, admin_controller, mock_admin_service):
        server_id = 1
        update_data = {"name": "UpdatedAPI"}
        mock_admin_service.update_external_server.side_effect = AppError("Update failed", 400)
        
        with app.test_request_context():
            with patch('flask.request') as mock_request:
                mock_request.get_json.return_value = update_data
                with patch.object(admin_controller, '_validate_json_data', return_value=(update_data, None)):
                    result = admin_controller.update_external_server(server_id)
                    if isinstance(result, tuple):
                        response, status_code = result
                        assert response.get_json()["error"] == "Update failed"
                        assert status_code == 400
                    else:
                        assert result["error"] == "Update failed"
                        assert result["status_code"] == 400

    def test_get_categories_success(self, admin_controller, mock_admin_service):
        expected_response = {"data": [{"id": 1, "name": "Technology"}, {"id": 2, "name": "Sports"}]}
        mock_admin_service.get_categories.return_value = expected_response
        
        result = admin_controller.get_categories()
        
        assert result == expected_response
        mock_admin_service.get_categories.assert_called_once()

    def test_get_categories_service_exception(self, admin_controller, mock_admin_service):
        mock_admin_service.get_categories.side_effect = AppError("Categories not found", 404)
        
        result = admin_controller.get_categories()
        
        assert result == {"error": "Categories not found", "status_code": 404}

    def test_get_categories_general_exception(self, admin_controller, mock_admin_service):
        mock_admin_service.get_categories.side_effect = Exception("Database error")
        
        result = admin_controller.get_categories()
        
        assert result == {"error": "Unexpected server error", "status_code": 500}

    def test_add_category_success(self, admin_controller, mock_admin_service):
        category_name = "Sports"
        expected_response = {"message": "Category added successfully", "category_id": 3}
        mock_admin_service.add_category.return_value = expected_response
        
        with app.test_request_context():
            with patch('flask.request') as mock_request:
                mock_request.get_json.return_value = {"name": category_name}
                with patch.object(admin_controller, '_validate_json_data', return_value=({"name": category_name}, None)):
                    result = admin_controller.add_category()
                    if isinstance(result, tuple):
                        response, status_code = result
                        assert response.get_json() == expected_response
                        assert status_code == 200
                    else:
                        assert result == expected_response
                    mock_admin_service.add_category.assert_called_once_with(category_name)

    def test_add_category_no_json_data(self, admin_controller, mock_admin_service):
        with app.test_request_context():
            with patch('flask.request') as mock_request:
                mock_request.get_json.return_value = None
                with patch.object(admin_controller, '_validate_json_data', return_value=(None, (None, 400))):
                    result = admin_controller.add_category()
                    if isinstance(result, tuple):
                        response, status_code = result
                        assert status_code == 400
                    else:
                        assert result[1] == 400 or result.get('status_code') == 400
                    mock_admin_service.add_category.assert_not_called()

    def test_add_category_missing_name_field(self, admin_controller, mock_admin_service):
        with app.test_request_context():
            with patch('flask.request') as mock_request:
                mock_request.get_json.return_value = {"description": "Sports category"}
                with patch.object(admin_controller, '_validate_json_data', return_value=(None, (None, 400))):
                    result = admin_controller.add_category()
                    if isinstance(result, tuple):
                        response, status_code = result
                        assert status_code == 400
                    else:
                        assert result[1] == 400 or result.get('status_code') == 400
                    mock_admin_service.add_category.assert_not_called()

    def test_add_category_empty_name_field(self, admin_controller, mock_admin_service):
        with app.test_request_context():
            with patch('flask.request') as mock_request:
                mock_request.get_json.return_value = {"name": ""}
                with patch.object(admin_controller, '_validate_json_data', return_value=(None, (None, 400))):
                    result = admin_controller.add_category()
                    if isinstance(result, tuple):
                        response, status_code = result
                        assert status_code == 400
                    else:
                        assert result[1] == 400 or result.get('status_code') == 400
                    mock_admin_service.add_category.assert_not_called()

    def test_add_category_none_name_field(self, admin_controller, mock_admin_service):
        with app.test_request_context():
            with patch('flask.request') as mock_request:
                mock_request.get_json.return_value = {"name": None}
                with patch.object(admin_controller, '_validate_json_data', return_value=(None, (None, 400))):
                    result = admin_controller.add_category()
                    if isinstance(result, tuple):
                        response, status_code = result
                        assert status_code == 400
                    else:
                        assert result[1] == 400 or result.get('status_code') == 400
                    mock_admin_service.add_category.assert_not_called()

    def test_add_category_service_exception(self, admin_controller, mock_admin_service):
        category_name = "Sports"
        mock_admin_service.add_category.side_effect = AppError("Category already exists", 409)
        
        with app.test_request_context():
            with patch('flask.request') as mock_request:
                mock_request.get_json.return_value = {"name": category_name}
                with patch.object(admin_controller, '_validate_json_data', return_value=({"name": category_name}, None)):
                    result = admin_controller.add_category()
                    if isinstance(result, tuple):
                        response, status_code = result
                        assert response.get_json()["error"] == "Category already exists"
                        assert status_code == 409
                    else:
                        assert result["error"] == "Category already exists"
                        assert result["status_code"] == 409

    def test_add_category_general_exception(self, admin_controller, mock_admin_service):
        category_name = "Sports"
        mock_admin_service.add_category.side_effect = Exception("Database connection failed")
        
        with app.test_request_context():
            with patch('flask.request') as mock_request:
                mock_request.get_json.return_value = {"name": category_name}
                with patch.object(admin_controller, '_validate_json_data', return_value=({"name": category_name}, None)):
                    result = admin_controller.add_category()
                    if isinstance(result, tuple):
                        response, status_code = result
                        assert response.get_json()["error"] == "Unexpected server error"
                        assert status_code == 500
                    else:
                        assert result["error"] == "Unexpected server error"
                        assert result["status_code"] == 500

    def test_update_external_server_general_exception(self, admin_controller, mock_admin_service):
        server_id = 1
        update_data = {"name": "UpdatedAPI"}
        mock_admin_service.update_external_server.side_effect = Exception("Network error")
        
        with app.test_request_context():
            with patch('flask.request') as mock_request:
                mock_request.get_json.return_value = update_data
                with patch.object(admin_controller, '_validate_json_data', return_value=(update_data, None)):
                    result = admin_controller.update_external_server(server_id)
                    if isinstance(result, tuple):
                        response, status_code = result
                        assert response.get_json()["error"] == "Unexpected server error"
                        assert status_code == 500
                    else:
                        assert result["error"] == "Unexpected server error"
                        assert result["status_code"] == 500 
import pytest
from services.base_service import BaseService
from utils.custom_exceptions import AppError
from http import HTTPStatus


class TestBaseService:
    
    @pytest.fixture
    def base_service(self):
        return BaseService()
    
    def test_success_response_with_data_and_message(self, base_service, app_context):
        data = {"key": "value"}
        message = "Success"
        
        response, status_code = base_service.success_response(data=data, message=message)
        
        assert status_code == 200
        assert response.json["data"] == data
        assert response.json["message"] == message
    
    def test_success_response_with_only_data(self, base_service, app_context):
        data = {"key": "value"}
        
        response, status_code = base_service.success_response(data=data)
        
        assert status_code == 200
        assert response.json["data"] == data
        assert "message" not in response.json
    
    def test_create_success_response_with_data(self, base_service, app_context):
        data = {"key": "value"}
        
        response, status_code = base_service._create_success_response(data=data)
        
        assert status_code == 200
        assert response.json["data"] == data
    
    def test_create_success_response_with_message(self, base_service, app_context):
        message = "Operation completed"
        
        response, status_code = base_service._create_success_response(message=message)
        
        assert status_code == 200
        assert response.json["message"] == message
    
    def test_validate_required_fields_all_present(self, base_service):
        field1 = "value1"
        field2 = "value2"
        
        base_service._validate_required_fields(field1, field2)
    
    def test_validate_required_fields_missing_field(self, base_service):
        field1 = "value1"
        field2 = None
        
        with pytest.raises(AppError) as exc_info:
            base_service._validate_required_fields(field1, field2)
        
        assert exc_info.value.message == "Missing required fields"
        assert exc_info.value.status_code == HTTPStatus.BAD_REQUEST
    
    def test_handle_empty_result_with_data(self, base_service):
        result = {"key": "value"}
        
        response = base_service._handle_empty_result(result, "Not found")
        
        assert response == result
    
    def test_handle_empty_result_without_data(self, base_service):
        result = None
        
        with pytest.raises(AppError) as exc_info:
            base_service._handle_empty_result(result, "Not found")
        
        assert exc_info.value.message == "Not found"
        assert exc_info.value.status_code == HTTPStatus.NOT_FOUND 
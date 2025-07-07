import pytest
from unittest.mock import Mock, patch
from controllers.auth_controller import AuthController
from utils.custom_exceptions import AppError
from app import create_app  # Import the app factory

app = create_app()  # Create the real Flask app

class TestAuthController:
    
    @pytest.fixture
    def auth_controller(self):
        return AuthController()
    
    @pytest.fixture
    def mock_auth_service(self, auth_controller):
        with patch.object(auth_controller, 'auth_service') as mock_service:
            yield mock_service
    
    def test_signup_returns_service_response_when_valid_data_provided(self, auth_controller, mock_auth_service):
        signup_data = {"username": "testuser", "email": "test@example.com", "password": "password123"}
        expected_response = {"message": "User registered successfully"}
        mock_auth_service.signup.return_value = expected_response
        
        with app.test_request_context(json=signup_data):
            result = auth_controller.signup()
            assert result == expected_response
    
    def test_login_returns_service_response_when_valid_credentials_provided(self, auth_controller, mock_auth_service):
        login_data = {"email": "test@example.com", "password": "password123"}
        expected_response = {"token": "jwt_token_here"}
        mock_auth_service.login.return_value = expected_response
        
        with app.test_request_context(json=login_data):
            result = auth_controller.login()
            assert result == expected_response 
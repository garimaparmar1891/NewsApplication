import pytest
from unittest.mock import Mock, patch
from services.auth_service import AuthService
from utils.custom_exceptions import AppError
from http import HTTPStatus
from constants import messages


class TestAuthService:
    
    @pytest.fixture
    def auth_service(self, mock_auth_repository, mock_login_history_repository, app_context):
        return AuthService()
    
    @pytest.fixture
    def mock_auth_repository(self):
        with patch('services.auth_service.AuthRepository') as mock_repo:
            yield mock_repo.return_value
    
    @pytest.fixture
    def mock_login_history_repository(self):
        with patch('services.auth_service.LoginHistoryRepository') as mock_repo:
            yield mock_repo.return_value
    
    @pytest.fixture
    def sample_user_data(self):
        return {
            "Id": 1,
            "Username": "testuser",
            "Email": "test@example.com",
            "PasswordHash": "hashed_password",
            "Role": "user"
        }
    
    @pytest.fixture
    def sample_signup_data(self):
        return {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123"
        }
    
    @pytest.fixture
    def sample_login_data(self):
        return {
            "email": "test@example.com",
            "password": "password123"
        }

    def test_signup_success(self, auth_service, mock_auth_repository, sample_signup_data, app_context):
        mock_auth_repository.get_user_by_email.return_value = None
        mock_auth_repository.create_user.return_value = True
        
        response, status_code = auth_service.signup(sample_signup_data)
        
        assert status_code == 200
        assert response.json['message'] == messages.USER_REGISTERED

    def test_signup_user_already_exists(self, auth_service, mock_auth_repository, sample_signup_data, app_context):
        mock_auth_repository.get_user_by_email.return_value = Mock()
        
        with pytest.raises(AppError) as exc_info:
            auth_service.signup(sample_signup_data)
        
        assert exc_info.value.message == messages.USER_ALREADY_EXISTS
        assert exc_info.value.status_code == HTTPStatus.CONFLICT

    def test_login_success(self, auth_service, mock_auth_repository, mock_login_history_repository, sample_login_data, sample_user_data, app_context):
        mock_auth_repository.get_user_by_email.return_value = Mock(
            Id=sample_user_data["Id"],
            Username=sample_user_data["Username"],
            Email=sample_user_data["Email"],
            PasswordHash=sample_user_data["PasswordHash"],
            Role=sample_user_data["Role"]
        )
        
        with patch.object(auth_service.bcrypt, 'check_password_hash', return_value=True):
            with patch.object(auth_service, '_generate_token', return_value='test_token'):
                response, status_code = auth_service.login(sample_login_data)
        
        assert status_code == 200
        assert response.json['data']['access_token'] == 'test_token'
        assert response.json['data']['username'] == sample_user_data["Username"]

    def test_login_invalid_credentials(self, auth_service, mock_auth_repository, sample_login_data, app_context):
        mock_auth_repository.get_user_by_email.return_value = Mock(
            Id=1,
            Username="testuser",
            Email="test@example.com",
            PasswordHash="hashed_password",
            Role="user"
        )
        
        with patch.object(auth_service.bcrypt, 'check_password_hash', return_value=False):
            with pytest.raises(AppError) as exc_info:
                auth_service.login(sample_login_data)
        
        assert exc_info.value.message == "Invalid credentials"
        assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED

    def test_record_login_calls_repository(self, auth_service, mock_login_history_repository, app_context):
        user_id = 1
        
        auth_service.record_login(user_id)
        
        mock_login_history_repository.record_login.assert_called_once_with(user_id)

    def test_record_login_success(self, auth_service, mock_login_history_repository, app_context):
        user_id = 1
        mock_login_history_repository.record_login.return_value = True
        
        auth_service.record_login(user_id)
        
        mock_login_history_repository.record_login.assert_called_once_with(user_id)

    def test_validate_signup_data_missing_fields(self, auth_service, app_context):
        incomplete_data = {"username": "test"}
        
        with pytest.raises(AppError) as exc_info:
            auth_service._validate_signup_data(incomplete_data)
        
        assert exc_info.value.message == "Missing required fields"

    def test_validate_signup_data_invalid_email(self, auth_service, app_context):
        invalid_data = {
            "username": "test",
            "email": "invalid-email",
            "password": "password123"
        }
        
        with pytest.raises(AppError) as exc_info:
            auth_service._validate_signup_data(invalid_data)
        
        assert exc_info.value.message == messages.INVALID_EMAIL_FORMAT

    def test_validate_login_data_missing_fields(self, auth_service, app_context):
        incomplete_data = {"email": "test@example.com"}
        
        with pytest.raises(AppError) as exc_info:
            auth_service._validate_login_data(incomplete_data)
        
        assert exc_info.value.message == "Missing required fields"

    def test_validate_login_data_invalid_email(self, auth_service, app_context):
        invalid_data = {
            "email": "invalid-email",
            "password": "password123"
        }
        
        with pytest.raises(AppError) as exc_info:
            auth_service._validate_login_data(invalid_data)
        
        assert exc_info.value.message == messages.INVALID_EMAIL_FORMAT

    def test_validate_email_format_valid(self, auth_service, app_context):
        valid_email = "test@example.com"
        
        auth_service._validate_email_format(valid_email)

    def test_validate_email_format_invalid(self, auth_service, app_context):
        invalid_email = "invalid-email"
        
        with pytest.raises(AppError) as exc_info:
            auth_service._validate_email_format(invalid_email)
        
        assert exc_info.value.message == messages.INVALID_EMAIL_FORMAT

    def test_check_user_exists_user_found(self, auth_service, mock_auth_repository, app_context):
        mock_auth_repository.get_user_by_email.return_value = Mock()
        
        with pytest.raises(AppError) as exc_info:
            auth_service._check_user_exists("test@example.com")
        
        assert exc_info.value.message == messages.USER_ALREADY_EXISTS

    def test_check_user_exists_user_not_found(self, auth_service, mock_auth_repository, app_context):
        mock_auth_repository.get_user_by_email.return_value = None
        
        auth_service._check_user_exists("test@example.com")

    def test_hash_password_returns_string(self, auth_service, app_context):
        password = "testpassword"
        
        with patch.object(auth_service.bcrypt, 'generate_password_hash') as mock_hash:
            mock_hash.return_value = b'hashed_password'
            result = auth_service._hash_password(password)
        
        assert isinstance(result, str)
        assert result == "hashed_password"

    def test_hash_password_calls_bcrypt(self, auth_service, app_context):
        password = "testpassword"
        
        with patch.object(auth_service.bcrypt, 'generate_password_hash') as mock_hash:
            mock_hash.return_value = b'hashed_password'
            auth_service._hash_password(password)
        
        mock_hash.assert_called_once_with(password)

    def test_get_and_validate_user_success(self, auth_service, mock_auth_repository, sample_user_data, app_context):
        mock_auth_repository.get_user_by_email.return_value = Mock(
            Id=sample_user_data["Id"],
            Username=sample_user_data["Username"],
            Email=sample_user_data["Email"],
            PasswordHash=sample_user_data["PasswordHash"],
            Role=sample_user_data["Role"]
        )
        
        with patch.object(auth_service.bcrypt, 'check_password_hash', return_value=True):
            result = auth_service._get_and_validate_user("test@example.com", "password123")
        
        assert result["Username"] == sample_user_data["Username"]
        assert result["Email"] == sample_user_data["Email"]

    def test_get_and_validate_user_invalid_password(self, auth_service, mock_auth_repository, sample_user_data, app_context):
        mock_auth_repository.get_user_by_email.return_value = Mock(
            Id=sample_user_data["Id"],
            Username=sample_user_data["Username"],
            Email=sample_user_data["Email"],
            PasswordHash=sample_user_data["PasswordHash"],
            Role=sample_user_data["Role"]
        )
        
        with patch.object(auth_service.bcrypt, 'check_password_hash', return_value=False):
            with pytest.raises(AppError) as exc_info:
                auth_service._get_and_validate_user("test@example.com", "wrongpassword")
        
        assert exc_info.value.message == "Invalid credentials"

    def test_format_user_data_with_user(self, auth_service, sample_user_data, app_context):
        user_row = Mock(
            Id=sample_user_data["Id"],
            Username=sample_user_data["Username"],
            Email=sample_user_data["Email"],
            PasswordHash=sample_user_data["PasswordHash"],
            Role=sample_user_data["Role"]
        )
        
        result = auth_service._format_user_data(user_row)
        
        assert result["Id"] == sample_user_data["Id"]
        assert result["Username"] == sample_user_data["Username"]

    def test_format_user_data_none(self, auth_service, app_context):
        result = auth_service._format_user_data(None)
        
        assert result is None

    def test_generate_token_returns_string(self, auth_service, sample_user_data, app_context):
        with patch('services.auth_service.create_access_token') as mock_create_token:
            mock_create_token.return_value = 'test_token'
            result = auth_service._generate_token(sample_user_data)
        
        assert isinstance(result, str)
        assert result == 'test_token'

    def test_generate_token_calls_create_access_token(self, auth_service, sample_user_data, app_context):
        with patch('services.auth_service.create_access_token') as mock_create_token:
            mock_create_token.return_value = 'test_token'
            auth_service._generate_token(sample_user_data)
        
        mock_create_token.assert_called_once()

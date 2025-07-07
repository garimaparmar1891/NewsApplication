import pytest
from unittest.mock import Mock, patch
from controllers.base_controller import BaseController
from http import HTTPStatus
from flask import Flask


class TestBaseController:
    
    @pytest.fixture
    def app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    @pytest.fixture
    def base_controller(self):
        return BaseController()
    
    def test_get_user_id_returns_jwt_identity(self, app, base_controller):
        expected_user_id = 123
        with app.app_context():
            with patch('controllers.base_controller.get_jwt_identity', return_value=expected_user_id):
                result = base_controller._get_user_id()
                assert result == expected_user_id
    
    def test_validate_required_dates_returns_error_when_start_date_missing(self, app, base_controller):
        with app.app_context():
            result = base_controller._validate_required_dates(None, "2024-01-01")
            assert result[1] == HTTPStatus.BAD_REQUEST
    
    def test_get_date_range_params_returns_request_args(self, app, base_controller):
        with app.test_request_context('/?start_date=2024-01-01&end_date=2024-01-31'):
            start_date, end_date = base_controller._get_date_range_params()
            assert start_date == "2024-01-01"
            assert end_date == "2024-01-31"
    
    def test_get_validated_date_params_returns_error_when_dates_missing(self, base_controller):
        with patch.object(base_controller, '_get_date_range_params', return_value=(None, None)):
            with patch.object(base_controller, '_validate_required_dates', return_value=("error", HTTPStatus.BAD_REQUEST)):
                result = base_controller._get_validated_date_params()
                assert result[1] == HTTPStatus.BAD_REQUEST
    
    def test_get_request_param_returns_value_when_param_exists(self, app, base_controller):
        with app.test_request_context('/?test_param=test_value'):
            result = base_controller._get_request_param("test_param")
            assert result == "test_value"

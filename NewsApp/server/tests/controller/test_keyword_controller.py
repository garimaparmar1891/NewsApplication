import pytest
from unittest.mock import Mock, patch
from controllers.keyword_controller import KeywordController
from http import HTTPStatus
from constants import messages
from app import create_app


class TestKeywordController:
    def setup_method(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.controller = KeywordController()

    def teardown_method(self):
        self.app_context.pop()

    def test_get_keywords_success(self):
        mock_service = Mock()
        mock_service.get_all_keywords.return_value = (
            self.app.response_class(
                response='{"data": [{"category_id": 1, "word": "test1"}, {"category_id": 2, "word": "test2"}]}',
                status=200,
                mimetype='application/json'), 200)
        self.controller.keyword_service = mock_service
        result = self.controller.get_keywords()
        assert result[0].get_json() == {"data": [{"category_id": 1, "word": "test1"}, {"category_id": 2, "word": "test2"}]}
        assert result[1] == 200
        mock_service.get_all_keywords.assert_called_once()

    def test_add_keyword_success(self):
        mock_service = Mock()
        mock_service.add_keyword.return_value = (self.app.response_class(
            response='{"message": "Keyword added successfully"}',
            status=200,
            mimetype='application/json'), 200)
        self.controller.keyword_service = mock_service
        with patch.object(self.controller, '_validate_json_data') as mock_validate:
            mock_validate.return_value = ({"word": "test", "category_id": 1}, None)
            result = self.controller.add_keyword()
            assert result[0].get_json() == {"message": "Keyword added successfully"}
            assert result[1] == 200
            mock_service.add_keyword.assert_called_once_with("test", 1)

    def test_delete_keyword_success(self):
        mock_service = Mock()
        mock_service.delete_keyword.return_value = (self.app.response_class(
            response='{"message": "Keyword deleted successfully"}',
            status=200,
            mimetype='application/json'), 200)
        self.controller.keyword_service = mock_service
        result = self.controller.delete_keyword("test")
        assert result[0].get_json() == {"message": "Keyword deleted successfully"}
        assert result[1] == 200
        mock_service.delete_keyword.assert_called_once_with("test")

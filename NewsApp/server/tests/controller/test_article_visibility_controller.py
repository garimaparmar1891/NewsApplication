import pytest
from unittest.mock import patch
from controllers.article_visibility_controller import ArticleVisibilityController
from http import HTTPStatus
from constants import messages
from flask import Flask, jsonify
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from app import create_app

class TestArticleVisibilityController:
    @pytest.fixture(scope="class")
    def app(self):
        app = create_app()
        app.config["TESTING"] = True
        return app

    @pytest.fixture
    def mock_service(self):
        with patch('controllers.article_visibility_controller.ArticleVisibilityService') as mock:
            yield mock.return_value

    @pytest.fixture
    def controller(self, mock_service):
        return ArticleVisibilityController()

    @pytest.fixture
    def mock_request_data(self):
        return {"reason": "inappropriate content"}

    def test_report_article_success(self, app, controller, mock_service, mock_request_data):
        with app.app_context(), \
             patch.object(controller, '_get_user_id', return_value=1), \
             patch.object(controller, '_validate_json_data', return_value=(mock_request_data, None)):
            mock_service.report_article.return_value = (jsonify({"message": messages.ARTICLE_REPORTED_SUCCESS}), 201)
            response, status = controller.report_article(123)
            assert status == 201
            assert response.get_json() == {"message": messages.ARTICLE_REPORTED_SUCCESS}

    def test_get_all_reported_articles_success(self, app, controller, mock_service):
        with app.app_context():
            mock_service.get_all_reported_articles.return_value = (jsonify({"data": []}), 200)
            response, status = controller.get_all_reported_articles()
            assert status == 200
            assert response.get_json() == {"data": []}

    def test_toggle_article_visibility_success(self, app, controller, mock_service):
        with app.app_context():
            # Test hide action
            mock_service.toggle_article_visibility.return_value = (jsonify({"message": messages.ARTICLE_HIDDEN_SUCCESS}), 200)
            response, status = controller.toggle_article_visibility(123, "hide")
            assert status == 200
            assert response.get_json() == {"message": messages.ARTICLE_HIDDEN_SUCCESS}
            # Test unhide action
            mock_service.toggle_article_visibility.return_value = (jsonify({"message": messages.ARTICLE_UNHIDDEN_SUCCESS}), 200)
            response, status = controller.toggle_article_visibility(123, "unhide")
            assert status == 200
            assert response.get_json() == {"message": messages.ARTICLE_UNHIDDEN_SUCCESS}

    def test_toggle_category_visibility_success(self, app, controller, mock_service):
        with app.app_context():
            # Test hide action
            mock_service.toggle_category_visibility.return_value = (jsonify({"message": messages.CATEGORY_HIDDEN_SUCCESS}), 200)
            response, status = controller.toggle_category_visibility(456, "hide")
            assert status == 200
            assert response.get_json() == {"message": messages.CATEGORY_HIDDEN_SUCCESS}
            # Test unhide action
            mock_service.toggle_category_visibility.return_value = (jsonify({"message": messages.CATEGORY_UNHIDDEN_SUCCESS}), 200)
            response, status = controller.toggle_category_visibility(456, "unhide")
            assert status == 200
            assert response.get_json() == {"message": messages.CATEGORY_UNHIDDEN_SUCCESS}

    def test_add_blocked_keyword_success(self, app, controller, mock_service):
        keyword_data = {"keyword": "spam"}
        with app.app_context(), patch.object(controller, '_validate_json_data', return_value=(keyword_data, None)):
            mock_service.add_blocked_keyword.return_value = (jsonify({"message": messages.BLOCKED_KEYWORD_ADDED}), 200)
            response, status = controller.add_blocked_keyword()
            assert status == 200
            assert response.get_json() == {"message": messages.BLOCKED_KEYWORD_ADDED}

    def test_get_blocked_keywords_success(self, app, controller, mock_service):
        with app.app_context():
            mock_service.get_blocked_keywords.return_value = (jsonify({"data": ["spam", "fake"]}), 200)
            response, status = controller.get_blocked_keywords()
            assert status == 200
            assert response.get_json() == {"data": ["spam", "fake"]}

    def test_delete_blocked_keyword_success(self, app, controller, mock_service):
        with app.app_context():
            mock_service.delete_blocked_keyword.return_value = (jsonify({"message": messages.BLOCKED_KEYWORD_DELETED}), 200)
            response, status = controller.delete_blocked_keyword(789)
            assert status == 200
            assert response.get_json() == {"message": messages.BLOCKED_KEYWORD_DELETED}

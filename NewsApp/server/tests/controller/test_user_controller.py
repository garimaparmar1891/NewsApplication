import pytest
from unittest.mock import patch
from controllers.user_controller import UserController
from flask import Flask

class TestUserController:
    @pytest.fixture
    def app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    @pytest.fixture
    def user_controller(self):
        return UserController()

    @pytest.fixture
    def mock_user_service(self, user_controller):
        with patch.object(user_controller, 'user_service') as mock_service:
            yield mock_service

    @pytest.fixture
    def mock_get_user_id(self, user_controller):
        with patch.object(user_controller, '_get_user_id') as mock_method:
            mock_method.return_value = 1
            yield mock_method

    def test_save_article_returns_success_message(self, app, user_controller, mock_user_service, mock_get_user_id):
        article_id = 1
        mock_user_service.save_article.return_value = "saved"
        with app.app_context():
            response, _ = user_controller.save_article(article_id)
            assert response.get_json()["message"] == "saved"

    def test_save_article_calls_service(self, user_controller, mock_user_service, mock_get_user_id):
        article_id = 2
        user_controller.save_article(article_id)
        mock_user_service.save_article.assert_called_once_with(1, article_id)

    def test_get_saved_articles_returns_data(self, app, user_controller, mock_user_service, mock_get_user_id):
        mock_user_service.get_saved_articles.return_value = ["article1"]
        with app.app_context():
            response, _ = user_controller.get_saved_articles()
            assert response.get_json()["data"] == ["article1"]

    def test_get_saved_articles_calls_service(self, user_controller, mock_user_service, mock_get_user_id):
        user_controller.get_saved_articles()
        mock_user_service.get_saved_articles.assert_called_once_with(1)

    def test_unsave_article_returns_success_message(self, app, user_controller, mock_user_service, mock_get_user_id):
        article_id = 3
        mock_user_service.unsave_article.return_value = "unsaved"
        with app.app_context():
            response, _ = user_controller.unsave_article(article_id)
            assert response.get_json()["message"] == "unsaved"

    def test_unsave_article_calls_service(self, user_controller, mock_user_service, mock_get_user_id):
        article_id = 4
        user_controller.unsave_article(article_id)
        mock_user_service.unsave_article.assert_called_once_with(1, article_id) 
import pytest
from unittest.mock import MagicMock, patch
from services.user_service import UserService
from utils.custom_exceptions import AppError
from constants import messages

class TestUserService:
    @patch('services.user_service.UserRepository')
    def test_save_article_success(self, mock_repo):
        mock_repo.return_value.save_article.return_value = True
        service = UserService()
        result = service.save_article(1, 2)
        assert result == messages.ARTICLE_SAVED

    @patch('services.user_service.UserRepository')
    def test_save_article_failure(self, mock_repo):
        mock_repo.return_value.save_article.return_value = False
        service = UserService()
        with pytest.raises(AppError) as exc:
            service.save_article(1, 2)
        assert str(exc.value) == messages.ARTICLE_SAVE_FAILED

    @patch('services.user_service.UserRepository')
    @patch('services.user_service.RecommendationService')
    def test_get_saved_articles_success(self, mock_recommendation, mock_repo):
        mock_repo.return_value.get_saved_articles.return_value = [{"Id": 1}]
        mock_repo.return_value.get_visible_article_ids.return_value = [1]
        mock_recommendation.return_value.score_and_sort_articles.return_value = [{"Id": 1}]
        with patch('services.user_service.UserService._format_article_row', return_value={"Id": 1}):
            service = UserService()
            result = service.get_saved_articles(1)
            assert result == [{"Id": 1}]

    @patch('services.user_service.UserRepository')
    def test_get_saved_articles_no_articles(self, mock_repo):
        mock_repo.return_value.get_saved_articles.return_value = []
        service = UserService()
        with pytest.raises(AppError) as exc:
            service.get_saved_articles(1)
        assert str(exc.value) == messages.NO_SAVED_ARTICLES

    @patch('services.user_service.UserRepository')
    def test_unsave_article_success(self, mock_repo):
        mock_repo.return_value.is_article_saved_by_user.return_value = True
        mock_repo.return_value.unsave_article.return_value = 1
        service = UserService()
        result = service.unsave_article(1, 2)
        assert result == messages.ARTICLE_UNSAVED_SUCCESS

    @patch('services.user_service.UserRepository')
    def test_unsave_article_not_saved(self, mock_repo):
        mock_repo.return_value.is_article_saved_by_user.return_value = False
        service = UserService()
        with pytest.raises(AppError) as exc:
            service.unsave_article(1, 2)
        assert str(exc.value) == messages.ARTICLE_NOT_SAVED

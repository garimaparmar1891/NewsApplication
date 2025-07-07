import pytest
from unittest.mock import Mock, patch
from services.article_reaction_service import ArticleReactionService
from utils.custom_exceptions import AppError
from http import HTTPStatus
from constants import messages


class TestArticleReactionService:
    
    @pytest.fixture
    def article_reaction_service(self, mock_article_reaction_repository, mock_article_repository, app_context):
        return ArticleReactionService()
    
    @pytest.fixture
    def mock_article_reaction_repository(self):
        with patch('services.article_reaction_service.ArticleReactionRepository') as mock_repo:
            yield mock_repo.return_value
    
    @pytest.fixture
    def mock_article_repository(self):
        with patch('services.article_reaction_service.ArticleRepository') as mock_repo:
            yield mock_repo.return_value
    
    @pytest.fixture
    def sample_article(self):
        return {"id": 1, "title": "Test Article", "content": "Test content"}
    
    @pytest.fixture
    def sample_reactions(self):
        return [
            {"article_id": 1, "reaction": "like", "reacted_at": "2024-01-01 10:00:00"},
            {"article_id": 2, "reaction": "dislike", "reacted_at": "2024-01-02 11:00:00"}
        ]

    def test_react_to_article_success(self, article_reaction_service, mock_article_reaction_repository, mock_article_repository, sample_article):
        mock_article_repository.get_article_by_id.return_value = sample_article
        mock_article_reaction_repository.check_user_reaction.return_value = None
        mock_article_reaction_repository.react_to_article.return_value = True
        
        response, status_code = article_reaction_service.react_to_article(1, 1, "like")
        
        assert status_code == 200
        assert response.json['message'] == messages.REACTION_RECORDED

    def test_react_to_article_already_liked(self, article_reaction_service, mock_article_reaction_repository, mock_article_repository, sample_article):
        mock_article_repository.get_article_by_id.return_value = sample_article
        mock_article_reaction_repository.check_user_reaction.return_value = "like"
        
        with pytest.raises(AppError) as exc_info:
            article_reaction_service.react_to_article(1, 1, "like")
        
        assert exc_info.value.message == messages.ALREADY_LIKED
        assert exc_info.value.status_code == HTTPStatus.BAD_REQUEST

    def test_get_user_reactions_success(self, article_reaction_service, mock_article_reaction_repository, sample_reactions):
        mock_article_reaction_repository.get_user_reactions.return_value = sample_reactions
        
        response, status_code = article_reaction_service.get_user_reactions(1)
        
        assert status_code == 200
        assert response.json['data'] == sample_reactions

    def test_get_user_reactions_calls_repository(self, article_reaction_service, mock_article_reaction_repository):
        mock_article_reaction_repository.get_user_reactions.return_value = []
        article_reaction_service.get_user_reactions(1)
        mock_article_reaction_repository.get_user_reactions.assert_called_once_with(1)

    def test_get_user_liked_articles_success(self, article_reaction_service, mock_article_reaction_repository, sample_reactions):
        mock_article_reaction_repository.get_user_reactions.return_value = sample_reactions
        
        response, status_code = article_reaction_service.get_user_liked_articles(1)
        
        assert status_code == 200
        assert len(response.json['data']) == 1
        assert response.json['data'][0]['Reaction'] == 'like'

    def test_get_user_liked_articles_filters_correctly(self, article_reaction_service, mock_article_reaction_repository):
        reactions = [
            {"article_id": 1, "reaction": "like", "reacted_at": "2024-01-01 10:00:00"},
            {"article_id": 2, "reaction": "dislike", "reacted_at": "2024-01-02 11:00:00"}
        ]
        mock_article_reaction_repository.get_user_reactions.return_value = reactions
        
        response, status_code = article_reaction_service.get_user_liked_articles(1)
        
        assert len(response.json['data']) == 1
        assert response.json['data'][0]['ArticleId'] == 1

    def test_get_user_disliked_articles_success(self, article_reaction_service, mock_article_reaction_repository, sample_reactions):
        mock_article_reaction_repository.get_user_reactions.return_value = sample_reactions
        
        response, status_code = article_reaction_service.get_user_disliked_articles(1)
        
        assert status_code == 200
        assert len(response.json['data']) == 1
        assert response.json['data'][0]['Reaction'] == 'dislike'

    def test_get_user_disliked_articles_filters_correctly(self, article_reaction_service, mock_article_reaction_repository):
        reactions = [
            {"article_id": 1, "reaction": "like", "reacted_at": "2024-01-01 10:00:00"},
            {"article_id": 2, "reaction": "dislike", "reacted_at": "2024-01-02 11:00:00"}
        ]
        mock_article_reaction_repository.get_user_reactions.return_value = reactions
        
        response, status_code = article_reaction_service.get_user_disliked_articles(1)
        
        assert len(response.json['data']) == 1
        assert response.json['data'][0]['ArticleId'] == 2 
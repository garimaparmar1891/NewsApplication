import pytest
from unittest.mock import Mock, patch
from controllers.article_reaction_controller import ArticleReactionController


class TestArticleReactionController:
    
    @pytest.fixture
    def article_reaction_controller(self):
        return ArticleReactionController()
    
    @pytest.fixture
    def mock_reaction_service(self, article_reaction_controller):
        with patch.object(article_reaction_controller, 'reaction_service') as mock_service:
            yield mock_service
    
    @pytest.fixture
    def mock_get_user_id(self, article_reaction_controller):
        with patch.object(article_reaction_controller, '_get_user_id') as mock_user_id:
            mock_user_id.return_value = 1
            yield mock_user_id
    
    def test_react_to_article_returns_service_response(
        self, article_reaction_controller, mock_reaction_service, mock_get_user_id
    ):
        article_id = 1
        reaction_type = "like"
        expected_response = {"message": "Reaction recorded"}
        mock_reaction_service.react_to_article.return_value = expected_response
        
        result = article_reaction_controller.react_to_article(article_id, reaction_type)
        
        assert result == expected_response
    
    def test_get_user_reactions_returns_service_response(
        self, article_reaction_controller, mock_reaction_service, mock_get_user_id
    ):
        expected_response = {"data": [{"article_id": 1, "reaction_type": "like"}]}
        mock_reaction_service.get_user_reactions.return_value = expected_response
        
        result = article_reaction_controller.get_user_reactions()
        
        assert result == expected_response

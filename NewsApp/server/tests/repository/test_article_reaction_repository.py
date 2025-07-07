import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from repositories.article_reaction_repository import ArticleReactionRepository


class TestArticleReactionRepository:
    
    @pytest.fixture
    def repository(self):
        return ArticleReactionRepository()
    
    @pytest.fixture
    def mock_reaction_row(self):
        row = Mock()
        row.ArticleId = 1
        row.ReactionType = "like"
        row.ReactedAt = datetime.now()
        return row

    @patch('repositories.article_reaction_repository.execute_write_query')
    def test_react_to_article_calls_execute_write_query(self, mock_execute, repository):
        mock_execute.return_value = 1
        
        result = repository.react_to_article(1, 1, "like")
        
        assert result == 1

    @patch('repositories.article_reaction_repository.fetch_all_query_with_params')
    def test_get_user_reactions_returns_mapped_data(self, mock_fetch_all, repository, mock_reaction_row):
        mock_fetch_all.return_value = [{'article_id': 1, 'reaction': 'like', 'reacted_at': mock_reaction_row.ReactedAt}]
        
        result = repository.get_user_reactions(1)
        
        assert result[0]['article_id'] == 1

    @patch('repositories.article_reaction_repository.fetch_one_query')
    def test_check_user_reaction_returns_reaction_type(self, mock_fetch_one, repository):
        mock_result = Mock()
        mock_result.ReactionType = "like"
        mock_fetch_one.return_value = mock_result
        
        result = repository.check_user_reaction(1, 1)
        
        assert result == "like"

    def test_map_reaction_row_returns_correct_structure(self, repository, mock_reaction_row):
        result = repository._map_reaction_row(mock_reaction_row)
        
        assert result['article_id'] == 1 
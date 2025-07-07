import pytest
from unittest.mock import MagicMock
from services.user_profile import UserProfileLoader

class TestUserProfileLoader:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_repos = {
            'user_keyword_repo': MagicMock(),
            'article_reaction_repo': MagicMock(),
            'user_repo': MagicMock(),
            'article_repo': MagicMock(),
            'article_visibility_repo': MagicMock(),
            'notification_repo': MagicMock()
        }
        self.loader = UserProfileLoader(self.mock_repos)

    def test_fetch_keywords_returns_keywords(self):
        self.mock_repos['user_keyword_repo'].get_user_keywords.return_value = [{'keyword': 'python'}]
        result = self.loader._fetch_keywords(1)
        assert result == {'python'}

    def test_fetch_keywords_empty(self):
        self.mock_repos['user_keyword_repo'].get_user_keywords.return_value = []
        result = self.loader._fetch_keywords(1)
        assert result == set()

    def test_fetch_keywords_multiple(self):
        self.mock_repos['user_keyword_repo'].get_user_keywords.return_value = [{'keyword': 'python'}, {'keyword': 'ai'}]
        result = self.loader._fetch_keywords(1)
        assert result == {'python', 'ai'}

    def test_fetch_liked_articles_returns_liked(self):
        self.mock_repos['article_reaction_repo'].get_user_reactions.return_value = [{'article_id': 1, 'reaction': 'like'}]
        result = self.loader._fetch_liked_articles(1)
        assert result == {1}

    def test_fetch_liked_articles_empty(self):
        self.mock_repos['article_reaction_repo'].get_user_reactions.return_value = []
        result = self.loader._fetch_liked_articles(1)
        assert result == set()

    def test_fetch_liked_articles_ignores_dislike(self):
        self.mock_repos['article_reaction_repo'].get_user_reactions.return_value = [{'article_id': 2, 'reaction': 'dislike'}]
        result = self.loader._fetch_liked_articles(1)
        assert result == set()

    def test_fetch_disliked_articles_returns_disliked(self):
        self.mock_repos['article_reaction_repo'].get_user_reactions.return_value = [{'article_id': 3, 'reaction': 'dislike'}]
        result = self.loader._fetch_disliked_articles(1)
        assert result == {3}

    def test_fetch_disliked_articles_empty(self):
        self.mock_repos['article_reaction_repo'].get_user_reactions.return_value = []
        result = self.loader._fetch_disliked_articles(1)
        assert result == set()

    def test_fetch_disliked_articles_ignores_like(self):
        self.mock_repos['article_reaction_repo'].get_user_reactions.return_value = [{'article_id': 4, 'reaction': 'like'}]
        result = self.loader._fetch_disliked_articles(1)
        assert result == set()

    def test_fetch_saved_articles_returns_saved(self):
        self.mock_repos['user_repo'].get_saved_article_ids.return_value = [5]
        result = self.loader._fetch_saved_articles(1)
        assert result == {5}

    def test_fetch_saved_articles_empty(self):
        self.mock_repos['user_repo'].get_saved_article_ids.return_value = []
        result = self.loader._fetch_saved_articles(1)
        assert result == set()

    def test_fetch_saved_articles_multiple(self):
        self.mock_repos['user_repo'].get_saved_article_ids.return_value = [6, 7]
        result = self.loader._fetch_saved_articles(1)
        assert result == {6, 7}

    def test_fetch_read_history_returns_history(self):
        self.mock_repos['article_repo'].get_read_history.return_value = [{'ArticleId': 8}]
        result = self.loader._fetch_read_history(1)
        assert result == {8}

    def test_fetch_read_history_empty(self):
        self.mock_repos['article_repo'].get_read_history.return_value = []
        result = self.loader._fetch_read_history(1)
        assert result == set()

    def test_fetch_read_history_multiple(self):
        self.mock_repos['article_repo'].get_read_history.return_value = [{'ArticleId': 9}, {'ArticleId': 10}]
        result = self.loader._fetch_read_history(1)
        assert result == {9, 10}

    def test_fetch_reported_articles_returns_reported(self):
        self.mock_repos['article_visibility_repo'].get_user_reported_articles.return_value = [11]
        result = self.loader._fetch_reported_articles(1)
        assert result == {11}

    def test_fetch_reported_articles_empty(self):
        self.mock_repos['article_visibility_repo'].get_user_reported_articles.return_value = []
        result = self.loader._fetch_reported_articles(1)
        assert result == set()

    def test_fetch_reported_articles_multiple(self):
        self.mock_repos['article_visibility_repo'].get_user_reported_articles.return_value = [12, 13]
        result = self.loader._fetch_reported_articles(1)
        assert result == {12, 13}

    def test_fetch_enabled_categories_returns_enabled(self):
        self.mock_repos['notification_repo'].get_enabled_category_ids.return_value = [14]
        result = self.loader._fetch_enabled_categories(1)
        assert result == {14}

    def test_fetch_enabled_categories_empty(self):
        self.mock_repos['notification_repo'].get_enabled_category_ids.return_value = []
        result = self.loader._fetch_enabled_categories(1)
        assert result == set()

    def test_fetch_enabled_categories_none_repo(self):
        self.loader.notification_repo = None
        result = self.loader._fetch_enabled_categories(1)
        assert result == set() 
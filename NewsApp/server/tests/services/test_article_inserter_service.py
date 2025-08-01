import pytest
from unittest.mock import MagicMock
from services.external_news.article_inserter import ArticleInserter

class TestArticleInserter:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_repo = MagicMock()
        self.mock_service = MagicMock()
        self.inserter = ArticleInserter(self.mock_repo, self.mock_service)

    def test_insert_returns_empty_when_no_new_articles(self):
        articles = [{"title": "A"}]
        self.mock_repo.article_exists_by_title.return_value = True
        inserted_ids, new_articles = self.inserter.insert(articles)
        assert inserted_ids == []

    def test_filter_new_articles_returns_empty_when_all_exist(self):
        articles = [{"title": "A"}]
        self.mock_repo.article_exists_by_title.return_value = True
        result = self.inserter._filter_new_articles(articles)
        assert result == []

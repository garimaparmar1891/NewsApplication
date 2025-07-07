import pytest
from unittest.mock import MagicMock
from services.external_news.category_resolver import CategoryResolver

class TestCategoryResolver:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.article_repo = MagicMock()
        self.keyword_repo = MagicMock()
        self.article_repo.get_all_categories.return_value = [
            {"Name": "Sports", "Id": 2},
            {"Name": "Tech", "Id": 3}
        ]
        self.keyword_repo.get_all_keywords.return_value = [
            {"word": "football", "category_id": 2},
            {"word": "ai", "category_id": 3}
        ]
        self.resolver = CategoryResolver(self.article_repo, self.keyword_repo)

    def test_resolve_returns_category_id_from_map(self):
        article = {"category": "Sports"}
        assert self.resolver.resolve(article) == 2

    def test_resolve_finds_category_by_keyword(self):
        article = {"title": "AI revolution", "content": ""}
        assert self.resolver.resolve(article) == 3

    def test_build_category_map_returns_correct_map(self):
        result = self.resolver._build_category_map()
        assert result == {"sports": 2, "tech": 3}

    def test_get_combined_text_returns_lowercase(self):
        article = {"title": "Hello", "content": "World"}
        assert self.resolver._get_combined_text(article) == "hello world"

    def test_find_category_by_keywords_returns_category_id(self):
        combined_text = "football match tonight"
        assert self.resolver._find_category_by_keywords(combined_text) == 2

    def test_find_category_by_keywords_returns_default(self):
        combined_text = "no match"
        assert self.resolver._find_category_by_keywords(combined_text) == 1 
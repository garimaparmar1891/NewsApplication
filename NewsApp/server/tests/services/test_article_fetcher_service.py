import pytest
from unittest.mock import MagicMock
from services.external_news.article_fetcher import ArticleFetcher, SourceType

class TestArticleFetcher:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.handler_registry = {"newsapi": MagicMock(), "generic": MagicMock()}
        self.blocked_keywords = [{"Keyword": "block"}]
        self.category_resolver = MagicMock()
        self.fetcher = ArticleFetcher(self.handler_registry, self.blocked_keywords, self.category_resolver)

    def test_get_source_name_lowercase(self):
        source = {"name": "NewsAPI"}
        assert self.fetcher._get_source_name(source) == "newsapi"

    def test_get_source_name_generic(self):
        source = {"name": "GENERIC"}
        assert self.fetcher._get_source_name(source) == "generic"

    def test_get_handler_found(self):
        assert self.fetcher._get_handler("newsapi") == self.handler_registry["newsapi"]

    def test_get_handler_not_found(self):
        assert self.fetcher._get_handler("unknown") is None

    def test_validate_source_config_true(self):
        source = {"base_url": "url", "api_key": "key"}
        assert self.fetcher._validate_source_config(source)

    def test_validate_source_config_false(self):
        source = {"base_url": "url"}
        assert not self.fetcher._validate_source_config(source)

    def test_determine_source_type_newsapi(self):
        assert self.fetcher._determine_source_type("newsapi") == SourceType.NEWSAPI

    def test_determine_source_type_generic(self):
        assert self.fetcher._determine_source_type("other") == SourceType.GENERIC

    def test_extract_source_config(self):
        source = {"base_url": "url", "api_key": "key"}
        assert self.fetcher._extract_source_config(source) == {"base_url": "url", "api_key": "key"}

    def test_get_categories(self):
        self.category_resolver.article_repo.get_all_categories.return_value = ["cat1"]
        assert self.fetcher._get_categories() == ["cat1"]

    def test_get_visibility_status_hidden(self):
        assert self.fetcher._get_visibility_status("block something") == self.fetcher.HIDDEN_VALUE

    def test_get_visibility_status_visible(self):
        assert self.fetcher._get_visibility_status("safe content") == self.fetcher.VISIBLE_VALUE

    def test_is_blocked_true(self):
        assert self.fetcher._is_blocked("block this")

    def test_is_blocked_false(self):
        assert not self.fetcher._is_blocked("allow this") 
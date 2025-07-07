import pytest
from services.external_news.handler_registry import HandlerRegistry

class TestHandlerRegistry:
    def test_create_handler_registry_contains_newsapi(self):
        registry = HandlerRegistry()
        assert "newsapi" in registry.handlers

    def test_create_handler_registry_contains_thenewsapi(self):
        registry = HandlerRegistry()
        assert "thenewsapi" in registry.handlers

    def test_get_handler_returns_newsapi_handler(self):
        registry = HandlerRegistry()
        handler = registry.get_handler("newsapi")
        assert handler.__class__.__name__ == "NewsAPIHandler"

    def test_get_handler_returns_thenewsapi_handler(self):
        registry = HandlerRegistry()
        handler = registry.get_handler("thenewsapi")
        assert handler.__class__.__name__ == "TheNewsAPIHandler" 
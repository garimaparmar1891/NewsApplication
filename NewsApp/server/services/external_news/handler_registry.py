from utils.handlers.newsapi_handler import NewsAPIHandler
from utils.handlers.thenewsapi_handler import TheNewsAPIHandler

class HandlerRegistry:
    def __init__(self):
        self.handlers = self._create_handler_registry()

    def _create_handler_registry(self):
        return {
            "newsapi": NewsAPIHandler(),
            "thenewsapi": TheNewsAPIHandler()
        }

    def get_handler(self, name):
        if not name:
            raise ValueError("Handler name cannot be empty")
        handler = self.handlers.get(name.lower())
        if handler is None:
            raise KeyError(f"Handler '{name}' not found")
        return handler

from constants.messages import THENEWSAPI_ERROR_FETCHING
from utils.base_news_handler import BaseNewsHandler

class TheNewsAPIHandler(BaseNewsHandler):
    def __init__(self, locale="us"):
        default_params = {"locale": locale}
        super().__init__(default_params)
        self.locale = locale

    def _build_request_params(self, api_key, **kwargs):
        return {
            "api_token": api_key,
            **self.default_params
        }

    def _extract_articles(self, response):
        response_data = response.json()
        raw_articles = response_data.get("data", [])
        return [self._convert_to_standard_format(article) for article in raw_articles]

    def _convert_to_standard_format(self, raw_article):
        return {
            "title": raw_article.get("title"),
            "content": raw_article.get("description"),
            "source": raw_article.get("source"),
            "url": raw_article.get("url"),
            "category": raw_article.get("category", "general"),
            "published_at": raw_article.get("published_at")
        }

    def _log_error(self, message):
        print(THENEWSAPI_ERROR_FETCHING.format(error=message))

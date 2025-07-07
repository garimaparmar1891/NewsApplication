from constants.messages import (
    NEWSAPI_REQUESTING_ARTICLES, 
    NEWSAPI_ERROR_FETCHING
)
from utils.base_news_handler import BaseNewsHandler

class NewsAPIHandler(BaseNewsHandler):
    def __init__(self, country="us", page_size=100):
        default_params = {
            "pageSize": page_size,
            "country": country
        }
        super().__init__(default_params)
        self.default_country = country
        self.page_size = page_size

    def fetch_articles(self, base_url, api_key, category):
        return super().fetch_articles(base_url, api_key, category=category)

    def _build_request_params(self, api_key, **kwargs):
        category = kwargs.get('category', 'general')
        params = {
            "category": category,
            "apiKey": api_key,
            **self.default_params
        }
        return params

    def _extract_articles(self, response):
        response_data = response.json()
        return response_data.get("articles", [])

    def _log_error(self, message):
        print(NEWSAPI_ERROR_FETCHING.format(error=message))

import requests

class TheNewsAPIHandler:
    def __init__(self, locale="us"):
        self.locale = locale

    def fetch_articles(self, base_url, api_key):
        url = base_url
        params = self._build_params(api_key)
        self._log_request(url, params)

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return self._extract_articles(response.json())
        except requests.RequestException as error:
            self._log_error(error)
            return []

    def _build_params(self, api_key):
        return {
            "locale": self.locale,
            "api_token": api_key
        }

    def _log_request(self, url, params):
        print("Request to TheNewsAPI")
        print(f"URL: {url}")
        print(f"Parameters: {params}")

    def _extract_articles(self, response_data):
        articles = response_data.get("data", [])
        return [self._map_article(article) for article in articles]

    def _map_article(self, article):
        return {
            "title": article.get("title"),
            "content": article.get("description"),
            "source": article.get("source"),
            "url": article.get("url"),
            "category": article.get("category", "general"),
            "published_at": article.get("published_at")
        }

    def _log_error(self, error):
        print(f"Error fetching from TheNewsAPI: {error}")

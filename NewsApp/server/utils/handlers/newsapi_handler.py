import requests

class NewsAPIHandler:
    def __init__(self, country="us", page_size=100):
        self.default_country = country
        self.page_size = page_size

    def fetch_articles(self, base_url, api_key, category):
        url = self._build_url(base_url, api_key, category)
        self._log_request(category, url)

        try:
            response = requests.get(url)
            self._ensure_success(response)
            return self._parse_response(response)
        except requests.RequestException as error:
            self._log_error(error)
            return []

    def _build_url(self, base_url, api_key, category):
        return (
            f"{base_url}?category={category}"
            f"&apiKey={api_key}&pageSize={self.page_size}&country={self.default_country}"
        )

    def _log_request(self, category, url):
        print(f"Requesting NewsAPI articles for category: {category}")
        print(f"URL: {url}")

    def _ensure_success(self, response):
        if response.status_code != 200:
            raise Exception(f"NewsAPI Error {response.status_code}: {response.text}")

    def _parse_response(self, response):
        data = response.json()
        return data.get("articles", [])

    def _log_error(self, error):
        print(f"Error fetching from NewsAPI: {error}")

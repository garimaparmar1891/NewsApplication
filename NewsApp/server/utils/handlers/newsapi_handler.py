import requests


class NewsAPIHandler:
    def __init__(self, country="us", page_size=100):
        self.default_country = country
        self.page_size = page_size

    def fetch_articles(self, base_url, api_key, category):
        url = self._build_url(base_url, api_key, category)
        self._log_fetch_attempt(category, url)

        response = requests.get(url)
        self._validate_response(response)

        return self._extract_articles(response)

    # ---------- Private Helpers ----------
    def _build_url(self, base_url, api_key, category):
        return (
            f"{base_url}?category={category}"
            f"&apiKey={api_key}&pageSize={self.page_size}&country={self.default_country}"
        )

    def _log_fetch_attempt(self, category, url):
        print(f"🌐 Fetching NewsAPI articles for category: '{category}'")
        print(f"➡️ Request URL: {url}")

    def _validate_response(self, response):
        if response.status_code != 200:
            raise Exception(f"❌ NewsAPI Error ({response.status_code}): {response.text}")

    def _extract_articles(self, response):
        data = response.json()
        return data.get("articles", [])

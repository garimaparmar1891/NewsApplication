import requests


class TheNewsAPIHandler:
    def __init__(self, locale="us"):
        self.locale = locale

    def fetch_articles(self, base_url, api_key):
        url = base_url
        params = self._build_query_params(api_key)
        self._log_request(url, params)

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return self._parse_articles(response.json())
        except requests.RequestException as e:
            self._handle_error(e)
            return []

    # ---------- Private Helpers ----------
    def _build_query_params(self, api_key):
        return {
            "locale": self.locale,
            "api_token": api_key
        }

    def _log_request(self, url, params):
        print("🌐 Fetching articles from TheNewsAPI")
        print(f"➡️ URL: {url}")
        print(f"🧾 Params: {params}")

    def _parse_articles(self, data):
        return [
            {
                "title": item.get("title"),
                "content": item.get("description"),
                "source": item.get("source"),
                "url": item.get("url"),
                "category": item.get("category", "general"),
                "published_at": item.get("published_at")
            }
            for item in data.get("data", [])
        ]

    def _handle_error(self, error):
        print(f"❌ TheNewsAPI fetch error: {error}")

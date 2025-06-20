from repositories.article_repository import ArticleRepository
from repositories.admin_repository import AdminRepository
from repositories.keyword_repository import KeywordRepository
from services.email_notification_service import EmailNotificationService
from utils.handlers.newsapi_handler import NewsAPIHandler
from utils.handlers.thenewsapi_handler import TheNewsAPIHandler


class ExternalNewsService:
    def __init__(self):
        self.article_repo = ArticleRepository()
        self.admin_repo = AdminRepository()
        self.keyword_repo = KeywordRepository()
        self.email_service = EmailNotificationService()

        self.handler_registry = {
            "newsapi": NewsAPIHandler(),
            "thenewsapi": TheNewsAPIHandler()
        }

        self.category_map = {
            category["name"].lower(): category["id"]
            for category in self.article_repo.get_all_categories()
        }
        self.keywords = self.keyword_repo.get_all_keywords()

    def fetch_and_store_all(self):
        print("📱 API fetch job triggered.")
        sources = self.admin_repo.get_external_servers()
        for source in sources:
            if not source.get("is_active"):
                print(f"Skipping inactive source: {source.get('name')}")
                continue

            inserted_ids = self._handle_source(source)

            if inserted_ids:
                self.email_service.send_notifications()
                print(f"Inserted {len(inserted_ids)} articles from {source['name']}. Sending notifications...")
                return 

            print(f"No articles inserted from {source['name']}, trying next...")

        print("All active sources failed. No news fetched.")


    # ---------- Private Helpers ----------
    def _handle_source(self, source):
        name = source["name"].lower()
        handler = self.handler_registry.get(name)

        if not handler:
            print(f"No handler registered for: {name}")
            return []

        try:
            if name == "newsapi":
                return self._handle_newsapi_source(source, handler)
            else:
                return self._handle_generic_source(source, handler)
        except Exception as e:
            print(f"Error fetching from {name}: {e}")
            return []

    def _handle_newsapi_source(self, source, handler):
        base_url, api_key, server_id = source["base_url"], source["api_key"], source["id"]
        categories = self.article_repo.get_all_categories()
        all_inserted_ids = []

        for category in categories:
            try:
                raw_articles = handler.fetch_articles(base_url, api_key, category["name"])
                articles = self._build_articles(raw_articles, source, category["id"])
                inserted_ids = self.article_repo.bulk_insert_articles(articles)
                all_inserted_ids.extend(inserted_ids)
                print(f"Inserted {len(inserted_ids)} articles for category: {category['name']}")
            except Exception as e:
                print(f"Failed to fetch {category['name']} from NewsAPI: {e}")

        return all_inserted_ids

    def _handle_generic_source(self, source, handler):
        base_url, api_key, server_id = source["base_url"], source["api_key"], source["id"]
        raw_articles = handler.fetch_articles(base_url, api_key)

        articles = []
        for article in raw_articles:
            category_id = self._resolve_category(article)
            articles.append({
                "title": article.get("title", ""),
                "content": article.get("content", ""),
                "source": source["name"].lower(),
                "url": article.get("url"),
                "category_id": category_id,
                "published_at": article.get("published_at"),
                "server_id": server_id
            })

        print(f"Inserting {len(articles)} articles from {source['name']}")
        return self.article_repo.bulk_insert_articles(articles)

    def _build_articles(self, raw_articles, source, category_id):
        server_id = source["id"]
        name = source["name"].lower()
        return [
            {
                "title": a.get("title"),
                "content": a.get("content") or a.get("description"),
                "source": name,
                "url": a.get("url"),
                "category_id": category_id,
                "published_at": a.get("publishedAt"),
                "server_id": server_id
            }
            for a in raw_articles
        ]

    def _resolve_category(self, article):
        api_category = article.get("category", "").lower()
        category_id = self.category_map.get(api_category)

        if category_id:
            return category_id

        combined_text = f"{article.get('title', '')} {article.get('content', '')}".lower()
        for keyword in self.keywords:
            if keyword["word"].lower() in combined_text:
                return keyword["category_id"]

        return 1


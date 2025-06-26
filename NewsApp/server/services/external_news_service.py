from repositories.article_repository import ArticleRepository
from repositories.admin_repository import AdminRepository
from repositories.keyword_repository import KeywordRepository
from services.notification_service import NotificationService
from utils.handlers.newsapi_handler import NewsAPIHandler
from utils.handlers.thenewsapi_handler import TheNewsAPIHandler


class ExternalNewsService:
    def __init__(self):
        self.article_repo = ArticleRepository()
        self.admin_repo = AdminRepository()
        self.keyword_repo = KeywordRepository()
        self.notification_service = NotificationService()

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
        sources = self.admin_repo.get_external_servers()
        total_inserted = 0
        user_notification_count = {}

        for source in sources:
            if not source.get("is_active"):
                continue

            inserted_ids = self._handle_source(source)
            total_inserted += len(inserted_ids)

            if inserted_ids:
                users = self.notification_service.repo.get_users_with_enabled_preferences()
                for user in users:
                    user_id = user.get("user_id")
                    if not user_id:
                        continue

                    result = self.notification_service.send_email_notifications(user_id)
                    if result.get("sent_count"):
                        user_notification_count[user["email"]] = result["sent_count"]

        self._log_summary(total_inserted, user_notification_count)


    def _handle_source(self, source):
        name = source["name"].lower()
        handler = self.handler_registry.get(name)

        if not handler:
            return []

        try:
            if name == "newsapi":
                return self._handle_newsapi_source(source, handler)
            return self._handle_generic_source(source, handler)
        except Exception:
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
            except Exception:
                continue

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
    

    def _log_summary(self, total_inserted, user_notification_count):
        if total_inserted:
            print(f"Total articles inserted: {total_inserted}")
        else:
            print("No articles were inserted from any source.")

        if user_notification_count:
            print("Notification summary:")
            for email, count in user_notification_count.items():
                print(f" - {email}: {count} articles notified")

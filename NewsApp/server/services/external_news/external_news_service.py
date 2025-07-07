from repositories.article_repository import ArticleRepository
from repositories.admin_repository import AdminRepository
from repositories.keyword_repository import KeywordRepository
from services.notification_service import NotificationService
from repositories.article_visibility_repository import ArticleVisibilityRepository
from repositories.notification_repository import NotificationRepository
from services.article_service import ArticleService
from services.base_service import BaseService
from constants.messages import FETCHING_FROM_SOURCE, INSERTED_ARTICLES_FROM_SOURCE

from .category_resolver import CategoryResolver
from .article_fetcher import ArticleFetcher
from .article_inserter import ArticleInserter
from .notification_manager import NotificationManager
from .handler_registry import HandlerRegistry

class ExternalNewsService(BaseService):
    def __init__(self):
        self.article_repo = ArticleRepository()
        self.article_service = ArticleService()
        self.admin_repo = AdminRepository()
        self.keyword_repo = KeywordRepository()
        self.notification_service = NotificationService()
        self.notification_repo = NotificationRepository()
        self.article_visibility_repo = ArticleVisibilityRepository()
        self.blocked_keywords = self.article_visibility_repo.get_blocked_keywords()
        self.handler_registry = HandlerRegistry()
        self.category_resolver = CategoryResolver(self.article_repo, self.keyword_repo)
        self.article_fetcher = ArticleFetcher(self.handler_registry.handlers, self.blocked_keywords, self.category_resolver)
        self.article_inserter = ArticleInserter(self.article_repo, self.article_service)
        self.notification_manager = NotificationManager(self.notification_repo, self.notification_service)

    def fetch_and_store_all(self):
        sources = self.admin_repo.get_active_external_servers()
        total_inserted = 0
        user_notification_count = {}
        articles_found = False  
        active_sources_tried = 0

        seen_articles = set()

        for source in sources:
            if not source.get("is_active"):
                continue
                
            active_sources_tried += 1
            print(f"Running API: {source.get('name')}")
            articles = self.article_fetcher.fetch(source)

            unique_articles = []
            for article in articles or []:
                key = (article.get("title"), article.get("url"), article.get("published_at"))
                if key not in seen_articles:
                    unique_articles.append(article)
                    seen_articles.add(key)

            if unique_articles:
                articles_found = True
                inserted_ids, new_articles = self.article_inserter.insert(unique_articles)
                total_inserted += len(inserted_ids)
                if inserted_ids and new_articles:
                    self.notification_manager.check_and_notify_users(new_articles, user_notification_count)
                break
            else:
                continue

        if articles_found:
            print(f"Total articles inserted: {total_inserted}")
            self._log_summary(total_inserted, user_notification_count)

    def _log_summary(self, total_inserted, user_notification_count):
        pass

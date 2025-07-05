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
        sources = self.admin_repo.get_external_servers()
        total_inserted = 0
        user_notification_count = {}
        articles_found = False
        active_sources_tried = 0

        for source in sources:
            if not source.get("is_active"):
                continue
                
            active_sources_tried += 1
            print(FETCHING_FROM_SOURCE.format(name=source.get('name')))
            articles = self.article_fetcher.fetch(source)
            
            if articles:
                articles_found = True
                inserted_ids, new_articles = self.article_inserter.insert(articles)
                total_inserted += len(inserted_ids)
                
                if inserted_ids:
                    print(INSERTED_ARTICLES_FROM_SOURCE.format(count=len(inserted_ids), name=source.get('name')))
                
                if inserted_ids and new_articles:
                    self.notification_manager.check_and_notify_users(new_articles, user_notification_count)
            else:
                continue

        if articles_found:
            self._log_summary(total_inserted, user_notification_count)

    def _log_summary(self, total_inserted, user_notification_count):
        if total_inserted:
            print(f"Total articles inserted: {total_inserted}")
        if user_notification_count:
            print("Notification summary:")
            for email, count in user_notification_count.items():
                print(f" - {email}: {count} articles notified")

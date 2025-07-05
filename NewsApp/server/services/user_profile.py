from dataclasses import dataclass, field
from typing import Set, Any
from .base_service import BaseService

@dataclass
class UserProfile:
    user_id: int
    keywords: Set[str] = field(default_factory=set)
    liked_articles: Set[Any] = field(default_factory=set)
    disliked_articles: Set[Any] = field(default_factory=set)
    saved_articles: Set[Any] = field(default_factory=set)
    read_history: Set[Any] = field(default_factory=set)
    reported_articles: Set[Any] = field(default_factory=set)
    enabled_categories: Set[int] = field(default_factory=set)

class UserProfileLoader(BaseService):
    def __init__(self, repositories):
        super().__init__()
        self._setup_repositories(repositories)

    def load(self, user_id: int) -> UserProfile:
        return UserProfile(
            user_id=user_id,
            keywords=self._fetch_keywords(user_id),
            liked_articles=self._fetch_liked_articles(user_id),
            disliked_articles=self._fetch_disliked_articles(user_id),
            saved_articles=self._fetch_saved_articles(user_id),
            read_history=self._fetch_read_history(user_id),
            reported_articles=self._fetch_reported_articles(user_id),
            enabled_categories=self._fetch_enabled_categories(user_id)
        )

    def _setup_repositories(self, repositories):
        self.user_keyword_repo = repositories.get('user_keyword_repo')
        self.article_reaction_repo = repositories.get('article_reaction_repo')
        self.user_repo = repositories.get('user_repo')
        self.article_repo = repositories.get('article_repo')
        self.article_visibility_repo = repositories.get('article_visibility_repo')
        self.notification_repo = repositories.get('notification_repo')

    def _fetch_keywords(self, user_id: int) -> Set[str]:
        keywords_data = self.user_keyword_repo.get_user_keywords(user_id)
        return set(k['keyword'] for k in keywords_data)

    def _fetch_liked_articles(self, user_id: int) -> Set[Any]:
        reactions_data = self.article_reaction_repo.get_user_reactions(user_id)
        return set(
            a['article_id'] for a in reactions_data
            if a['reaction'].lower() == 'like'
        )

    def _fetch_disliked_articles(self, user_id: int) -> Set[Any]:
        reactions_data = self.article_reaction_repo.get_user_reactions(user_id)
        return set(
            a['article_id'] for a in reactions_data
            if a['reaction'].lower() == 'dislike'
        )

    def _fetch_saved_articles(self, user_id: int) -> Set[Any]:
        saved_ids = self.user_repo.get_saved_article_ids(user_id)
        return set(saved_ids)

    def _fetch_read_history(self, user_id: int) -> Set[Any]:
        history_data = self.article_repo.get_read_history(user_id)
        return set(a['ArticleId'] for a in history_data)

    def _fetch_reported_articles(self, user_id: int) -> Set[Any]:
        reported_ids = self.article_visibility_repo.get_user_reported_articles(user_id)
        return set(reported_ids)

    def _fetch_enabled_categories(self, user_id: int) -> Set[int]:
        if self.notification_repo:
            enabled_category_ids = self.notification_repo.get_enabled_category_ids(user_id)
            return set(enabled_category_ids)
        return set()

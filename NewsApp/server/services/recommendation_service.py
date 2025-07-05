from repositories.user_keyword_repository import UserKeywordRepository
from repositories.article_reaction_repository import ArticleReactionRepository
from repositories.user_repository import UserRepository
from repositories.article_repository import ArticleRepository
from repositories.article_visibility_repository import ArticleVisibilityRepository
from repositories.notification_repository import NotificationRepository
from .user_profile import UserProfileLoader
from .scoring import ArticleScorer
from .base_service import BaseService
from typing import List, Tuple

class RecommendationService(BaseService):
    def __init__(self):
        super().__init__()
        self._setup_repositories()
        self._setup_profile_loader()
        self._setup_scoring_strategies()

    def score_and_sort_articles(self, user_id: int, articles: List[dict]) -> List[dict]:
        self._validate_required_fields(user_id, articles, error_message="User ID and articles are required")
        user_profile = self._load_user_profile(user_id)
        scored_articles = self._score_articles(articles, user_profile)
        return self._extract_sorted_articles(scored_articles)

    def _setup_repositories(self):
        self.user_keyword_repo = UserKeywordRepository()
        self.article_reaction_repo = ArticleReactionRepository()
        self.user_repo = UserRepository()
        self.article_repo = ArticleRepository()
        self.article_visibility_repo = ArticleVisibilityRepository()
        self.notification_repo = NotificationRepository()

    def _setup_profile_loader(self):
        repositories = {
            'user_keyword_repo': self.user_keyword_repo,
            'article_reaction_repo': self.article_reaction_repo,
            'user_repo': self.user_repo,
            'article_repo': self.article_repo,
            'article_visibility_repo': self.article_visibility_repo,
            'notification_repo': self.notification_repo
        }
        self.profile_loader = UserProfileLoader(repositories)

    def _setup_scoring_strategies(self):
        self.scoring_strategies = ArticleScorer.default_strategies()

    def _load_user_profile(self, user_id: int):
        return self.profile_loader.load(user_id)

    def _score_articles(self, articles: List[dict], user_profile) -> List[Tuple[int, dict]]:
        return [
            (ArticleScorer.score(article, user_profile, self.scoring_strategies), article)
            for article in articles
        ]

    def _extract_sorted_articles(self, scored_articles: List[Tuple[int, dict]]) -> List[dict]:
        scored_articles.sort(reverse=True, key=lambda x: x[0])
        return [article for score, article in scored_articles]

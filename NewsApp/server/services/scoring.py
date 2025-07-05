from typing import List, Callable
from .user_profile import UserProfile

ScoringStrategy = Callable[[dict, UserProfile], int]

class ArticleScorer:
    PREFERENCE_SCORE = 6
    KEYWORD_SCORE = 5
    LIKE_SCORE = 4
    SAVE_SCORE = 3
    READ_SCORE = 2
    DISLIKE_SCORE = -4
    REPORT_SCORE = -6
    

    @staticmethod
    def score(article: dict, user_profile: UserProfile, strategies: List[ScoringStrategy]) -> int:
        return sum(strategy(article, user_profile) for strategy in strategies)

    @staticmethod
    def default_strategies() -> List[ScoringStrategy]:
        return [
            ArticleScorer._keyword_scoring,
            ArticleScorer._like_scoring,
            ArticleScorer._dislike_scoring,
            ArticleScorer._save_scoring,
            ArticleScorer._read_scoring,
            ArticleScorer._report_scoring,
            ArticleScorer._preference_scoring
        ]

    @staticmethod
    def _keyword_scoring(article: dict, user_profile: UserProfile) -> int:
        title = (article.get('Title') or '').lower()
        content = (article.get('Content') or '').lower()
        return ArticleScorer.KEYWORD_SCORE if any(kw.lower() in title or kw.lower() in content for kw in user_profile.keywords) else 0

    @staticmethod
    def _like_scoring(article: dict, user_profile: UserProfile) -> int:
        return ArticleScorer.LIKE_SCORE if article.get('Id') in user_profile.liked_articles else 0

    @staticmethod
    def _dislike_scoring(article: dict, user_profile: UserProfile) -> int:
        return ArticleScorer.DISLIKE_SCORE if article.get('Id') in user_profile.disliked_articles else 0

    @staticmethod
    def _save_scoring(article: dict, user_profile: UserProfile) -> int:
        return ArticleScorer.SAVE_SCORE if article.get('Id') in user_profile.saved_articles else 0

    @staticmethod
    def _read_scoring(article: dict, user_profile: UserProfile) -> int:
        return ArticleScorer.READ_SCORE if article.get('Id') in user_profile.read_history else 0

    @staticmethod
    def _report_scoring(article: dict, user_profile: UserProfile) -> int:
        return ArticleScorer.REPORT_SCORE if article.get('Id') in user_profile.reported_articles else 0

    @staticmethod
    def _preference_scoring(article: dict, user_profile: UserProfile) -> int:
        category_id = article.get('CategoryId')
        return ArticleScorer.PREFERENCE_SCORE if category_id and category_id in user_profile.enabled_categories else 0

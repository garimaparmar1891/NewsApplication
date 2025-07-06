from repositories.article_repository import ArticleRepository
from repositories.category_repository import CategoryRepository
from datetime import datetime
from http import HTTPStatus
from constants import messages
from utils.formatting import format_article_row
from services.recommendation_service import RecommendationService
from utils.custom_exceptions import AppError
from services.base_service import BaseService

class ArticleService(BaseService):
    def __init__(self):
        super().__init__()
        self.repo = ArticleRepository()
        self.category_repo = CategoryRepository()
        self.recommendation_service = RecommendationService()

    def search_articles_by_keyword_and_range(self, search_params, user_id=None):
        self._validate_date_range(search_params['start_date'], search_params['end_date'])
        articles = self.repo.search_articles_by_keyword_and_range(
            search_params['keyword'], 
            search_params['start_date'], 
            search_params['end_date']
        )
        formatted = self._format_articles(articles)
        if user_id and formatted:
            formatted = self.recommendation_service.score_and_sort_articles(user_id, formatted)
        return self._respond_with_articles(formatted, messages.NO_ARTICLES_FOR_KEYWORD)

    def get_today_headlines(self, user_id=None):
        today = datetime.now().date()
        articles = self.repo.get_today_headlines(today)
        formatted = self._format_articles(articles)
        if user_id and formatted:
            formatted = self.recommendation_service.score_and_sort_articles(user_id, formatted)
        return self._respond_with_articles(formatted, messages.NO_HEADLINES_AVAILABLE)

    def get_articles_by_range(self, date_range, category_names, user_id=None):
        self._validate_date_range(date_range['start_date'], date_range['end_date'])
        
        # Handle both single category (string) and multiple categories (list)
        if isinstance(category_names, str):
            category_names = [category_names]
        elif category_names is None:
            category_names = []
        
        # Get category IDs for all category names
        category_ids = []
        for category_name in category_names:
            category_id = self._get_category_id(category_name)
            if category_id:
                category_ids.append(category_id)
        
        articles = self.repo.get_articles_by_range(
            date_range['start_date'], 
            date_range['end_date'], 
            category_ids
        )
        formatted = self._format_articles(articles)
        if user_id and formatted:
            formatted = self.recommendation_service.score_and_sort_articles(user_id, formatted)
        return self._respond_with_articles(formatted, messages.NO_ARTICLES_IN_RANGE)

    def get_all_categories(self):
        categories = self.repo.get_all_categories()
        return self._create_success_response(data=categories)

    def record_article_read(self, user_id, article_id):
        self._validate_required_fields(user_id, article_id, error_message=messages.MISSING_REQUIRED_FIELDS)
        success = self.repo.record_article_read(user_id, article_id)
        return self._handle_read_result(success)

    def get_all_articles(self, user_id=None):
        articles = self.repo.get_all_articles()
        formatted = self._format_articles(articles)
        if user_id and formatted:
            formatted = self.recommendation_service.score_and_sort_articles(user_id, formatted)
        return self._respond_with_articles(formatted, messages.NO_ARTICLES_FOUND)

    def bulk_insert_articles(self, articles):
        blocked_keywords = self.repo.get_blocked_keywords()
        prepared_articles = self._prepare_articles_for_insert(articles, blocked_keywords)
        return self.repo.bulk_insert_articles(prepared_articles)

    def _respond_with_articles(self, articles, error_msg):
        return self._handle_empty_result(articles, error_msg, HTTPStatus.NOT_FOUND)

    def _format_articles(self, articles):
        return [format_article_row(a) for a in articles] if articles else []

    def _handle_read_result(self, success):
        if success:
            return self._create_success_response(message=messages.READ_RECORDED)
        raise AppError(messages.READ_RECORD_FAILED, HTTPStatus.INTERNAL_SERVER_ERROR)

    def _prepare_articles_for_insert(self, articles, blocked_keywords):
        prepared_articles = []
        for article in articles:
            published_at = self._parse_published_at(article.get("published_at"))
            is_hidden = self._should_hide_article(article, blocked_keywords)
            prepared_articles.append({
                "title": article["title"],
                "content": article.get("content"),
                "source": article.get("source"),
                "url": article.get("url"),
                "category_id": article["category_id"],
                "published_at": published_at,
                "server_id": article["server_id"],
                "is_hidden": is_hidden
            })
        return prepared_articles

    def _should_hide_article(self, article, blocked_keywords):
        title = (article.get("title") or "").lower()
        content = (article.get("content") or "").lower()
        combined_text = f"{title} {content}"
        return 1 if any(keyword.lower() in combined_text for keyword in blocked_keywords) else article.get("is_hidden", 0)

    def _parse_published_at(self, published_at):
        if isinstance(published_at, str):
            return datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        return published_at

    def _validate_date_range(self, start_date, end_date):
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            if start > end:
                raise AppError(messages.INVALID_DATE_RANGE, HTTPStatus.BAD_REQUEST)
        except ValueError:
            raise AppError(messages.INVALID_DATE_FORMAT, HTTPStatus.BAD_REQUEST)

    def _get_category_id(self, category_name):
        if not category_name:
            return None
        category = self.category_repo.get_category_by_name(category_name)
        return category["Id"] if category else None

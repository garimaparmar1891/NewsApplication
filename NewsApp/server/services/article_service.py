from repositories.article_repository import ArticleRepository
from repositories.category_repository import CategoryRepository
from datetime import datetime


class ArticleService:
    def __init__(self):
        self.repo = ArticleRepository()
        self.category_repo = CategoryRepository()

    def get_today_headlines(self):
        today = datetime.now().date()
        return self.repo.get_today_headlines(today)

    def get_articles_by_range(self, start_date, end_date, category_name):
        category_id = self._resolve_category_id(category_name)
        return self.repo.get_articles_by_range(start_date, end_date, category_id)

    def get_all_categories(self):
        return self.repo.get_all_categories()

    def save_article(self, user_id, article_id):
        return self.repo.save_article(user_id, article_id)

    def search_articles_by_keyword_and_range(self, keyword, start_date, end_date):
        return self.repo.search_articles_by_keyword_and_range(keyword, start_date, end_date)

    # ---------- Private Helpers ----------
    def _resolve_category_id(self, category_name):
        if not category_name:
            return None

        category = self.category_repo.get_category_by_name(category_name)
        return category["Id"] if category else None

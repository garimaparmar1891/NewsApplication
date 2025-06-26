
from repositories.article_visibility_repository import ArticleModerationRepository

class ArticleModerationService:
    def __init__(self):
        self.repo = ArticleModerationRepository()

    def report_article(self, user_id, article_id, reason):
        return self.repo.insert_report(user_id, article_id, reason)

    def get_reported_articles(self):
        return self.repo.fetch_reported_articles()

    def set_article_visibility(self, article_id, hide=True):
        self.repo.update_article_visibility(article_id, hide)

    def set_category_visibility(self, category_id, hide=True):
        self.repo.update_category_visibility(category_id, hide)

    def add_blocked_keyword(self, keyword):
        self.repo.insert_blocked_keyword(keyword)

    def get_blocked_keywords(self):
        return self.repo.get_blocked_keywords()

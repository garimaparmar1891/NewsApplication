class ArticleInserter:
    def __init__(self, article_repo, article_service):
        self.article_repo = article_repo
        self.article_service = article_service

    def insert(self, articles):
        new_articles = self._filter_new_articles(articles)
        if new_articles:
            inserted_ids = self.article_service.bulk_insert_articles(new_articles)
            return inserted_ids, new_articles
        return [], []

    def _filter_new_articles(self, articles):
        return [article for article in articles if not self.article_repo.article_exists_by_title(article["title"])]

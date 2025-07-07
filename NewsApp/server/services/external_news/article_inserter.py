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
        from scheduler.news_fetcher import format_published_at
        return [
            article for article in articles
            if not self.article_repo.article_exists_duplicate(
                article["title"],
                article.get("url"),
                format_published_at(article.get("published_at"))
            )
        ]

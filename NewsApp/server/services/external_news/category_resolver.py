class CategoryResolver:
    def __init__(self, article_repo, keyword_repo):
        self.article_repo = article_repo
        self.keyword_repo = keyword_repo
        self.category_map = self._build_category_map()
        self.keywords = self.keyword_repo.get_all_keywords()

    def resolve(self, article):
        api_category = article.get("category", "").lower()
        category_id = self.category_map.get(api_category)
        if category_id:
            return category_id
        combined_text = self._get_combined_text(article)
        return self._find_category_by_keywords(combined_text)

    def _build_category_map(self):
        categories = self.article_repo.get_all_categories()
        return {category["Name"].lower(): category["Id"] for category in categories}

    def _get_combined_text(self, article):
        title = article.get('title', '')
        content = article.get('content', '')
        return f"{title} {content}".lower()

    def _find_category_by_keywords(self, combined_text):
        for keyword in self.keywords:
            if keyword["word"].lower() in combined_text:
                return keyword["category_id"]
        return 1
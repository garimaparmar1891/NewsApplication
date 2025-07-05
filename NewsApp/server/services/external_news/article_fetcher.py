from constants.messages import ERROR_FETCHING_FROM_SOURCE
from enum import Enum

class SourceType(Enum):
    NEWSAPI = "newsapi"
    GENERIC = "generic"

class ArticleFetcher:
    REQUIRED_CONFIG_FIELDS = ["base_url", "api_key"]
    HIDDEN_VALUE = 1
    VISIBLE_VALUE = 0
    
    def __init__(self, handler_registry, blocked_keywords, category_resolver):
        self.handler_registry = handler_registry
        self.blocked_keywords = blocked_keywords
        self.category_resolver = category_resolver

    def fetch(self, source):
        name = self._get_source_name(source)
        
        handler = self._get_handler(name)
        if not handler:
            return []
        
        if not self._validate_source_config(source):
            return []
        
        return self._fetch_with_error_handling(source, handler, name)

    def _get_source_name(self, source):
        return source["name"].lower()

    def _get_handler(self, name):
        return self.handler_registry.get(name)

    def _validate_source_config(self, source):
        return all(source.get(field) for field in self.REQUIRED_CONFIG_FIELDS)

    def _fetch_with_error_handling(self, source, handler, name):
        try:
            return self._fetch_articles(source, handler, name)
        except Exception as e:
            self._log_error(name, str(e))
            return []

    def _fetch_articles(self, source, handler, name):
        source_type = self._determine_source_type(name)
        
        if source_type == SourceType.NEWSAPI:
            return self._fetch_newsapi_articles(source, handler)
        else:
            return self._fetch_generic_articles(source, handler)

    def _determine_source_type(self, name):
        return SourceType.NEWSAPI if name == SourceType.NEWSAPI.value else SourceType.GENERIC

    def _fetch_newsapi_articles(self, source, handler):
        config = self._extract_source_config(source)
        categories = self._get_categories()
        
        all_articles = []
        for category in categories:
            articles = self._fetch_articles_for_category(config, handler, category, source)
            all_articles.extend(articles)
        
        return all_articles

    def _fetch_generic_articles(self, source, handler):
        config = self._extract_source_config(source)
        raw_articles = handler.fetch_articles(config["base_url"], config["api_key"])
        
        if not raw_articles:
            return []
        
        return self._process_raw_articles(raw_articles, source)

    def _extract_source_config(self, source):
        return {
            "base_url": source["base_url"],
            "api_key": source["api_key"]
        }

    def _get_categories(self):
        return self.category_resolver.article_repo.get_all_categories()

    def _fetch_articles_for_category(self, config, handler, category, source):
        try:
            raw_articles = handler.fetch_articles(
                config["base_url"], 
                config["api_key"], 
                category["Name"]
            )
            
            if raw_articles:
                return self._build_newsapi_articles(raw_articles, source, category)
            
        except Exception as e:
            self._log_error(category.get('Name', 'unknown'), str(e))
        
        return []

    def _process_raw_articles(self, raw_articles, source):
        articles = []
        for article in raw_articles:
            processed_article = self._process_single_article(article, source)
            if processed_article:
                articles.append(processed_article)
        return articles

    def _process_single_article(self, article, source):
        try:
            category_id = self.category_resolver.resolve(article)
            return self._build_article_dict(article, source, category_id)
        except Exception as e:
            self._log_error(source["name"], str(e))
            return None

    def _build_newsapi_articles(self, raw_articles, source, category):
        return [
            self._build_article_dict(
                article, source, category["Id"], 
                name=source["name"].lower(), 
                server_id=source["id"]
            )
            for article in raw_articles
            if self._build_article_dict(
                article, source, category["Id"], 
                name=source["name"].lower(), 
                server_id=source["id"]
            )
        ]

    def _build_article_dict(self, article, source, category_id, name=None, server_id=None):
        try:
            article_data = self._extract_article_data(article, source, name, server_id)
            
            if not article_data["title"]:
                return None
                
            return self._create_article_dict(article_data, category_id)
            
        except Exception as e:
            self._log_error(source["name"], str(e))
            return None

    def _extract_article_data(self, article, source, name, server_id):
        return {
            "name": name or source["name"].lower(),
            "server_id": server_id or source["id"],
            "title": article.get("title", ""),
            "content": article.get("content") or article.get("description", ""),
            "url": article.get("url"),
            "published_at": article.get("publishedAt") or article.get("published_at")
        }

    def _create_article_dict(self, article_data, category_id):
        combined_content = f"{article_data['title']} {article_data['content']}"
        
        return {
            "title": article_data["title"],
            "content": article_data["content"],
            "source": article_data["name"],
            "url": article_data["url"],
            "category_id": category_id,
            "published_at": article_data["published_at"],
            "server_id": article_data["server_id"],
            "is_hidden": self._get_visibility_status(combined_content)
        }

    def _get_visibility_status(self, content):
        return self.HIDDEN_VALUE if self._is_blocked(content) else self.VISIBLE_VALUE

    def _is_blocked(self, content):
        content_lower = content.lower()
        return any(keyword['Keyword'].lower() in content_lower for keyword in self.blocked_keywords)

    def _log_error(self, name, error):
        print(ERROR_FETCHING_FROM_SOURCE.format(name=name, error=error))

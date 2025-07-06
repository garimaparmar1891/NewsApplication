from features.services.articles.articles_by_range_service import ArticlesByRangeService
from utils.response_handler import handle_data_response
from constants import messages as msg
from menu.paginated_menu import PaginatedMenu

class ArticlesByRangeHandler:

    @staticmethod
    def get_articles_by_range(start, end, categories=None):
        try:
            articles = ArticlesByRangeHandler._fetch_articles(start, end, categories)
            if not articles:
                return
            
            ArticlesByRangeHandler._display_articles(articles)
        except Exception as e:
            print(f"Error occurred while fetching articles by range: {str(e)}")

    @staticmethod
    def get_all_articles():
        try:
            print("Fetching all articles...")
            response = ArticlesByRangeService.get_all_articles()
            result = handle_data_response(response, msg.ARTICLES_FETCH_FAILED)
           
            return result
        except Exception as e:
            print(f"Error occurred while fetching all articles: {str(e)}")
            return False, None

    @staticmethod
    def _fetch_articles(start, end, categories=None):
        try:
            if not categories or (len(categories) == 1 and categories[0].lower() == 'all'):
                success, articles = ArticlesByRangeHandler._fetch_articles_without_category(start, end)
            elif len(categories) > 1:
                success, articles = ArticlesByRangeHandler._fetch_articles_multiple_categories(start, end, categories)
            else:
                success, articles = ArticlesByRangeHandler._fetch_articles_single_category(start, end, categories[0])
            
            if not success:
                print(f"Failed to fetch articles: {articles}")
                return None
                
            if not articles:
                print("No articles found for the specified date range and category.")
                return None
            
            return articles
        except Exception as e:
            print(f"Error occurred while fetching articles: {str(e)}")
            return None

    @staticmethod
    def _display_articles(articles):
        try:
            context_label = "Articles by Date Range"
            PaginatedMenu(articles, context_label=context_label).show()
        except Exception as e:
            print(f"Error occurred while displaying articles: {str(e)}")

    @staticmethod
    def _fetch_articles_without_category(start, end):
        try:
            response = ArticlesByRangeService.get_articles_by_range(start, end)
            result = handle_data_response(response, msg.ARTICLES_FETCH_FAILED)
            return result
        except Exception as e:
            print(f"Error occurred while fetching articles without category: {str(e)}")
            return False, None

    @staticmethod
    def _fetch_articles_single_category(start, end, category):
        try:
            response = ArticlesByRangeService.get_articles_by_range(start, end, category)
            result = handle_data_response(response, msg.ARTICLES_FETCH_FAILED)
            return result
        except Exception as e:
            print(f"Error occurred while fetching articles for category {category}: {str(e)}")
            return False, None

    @staticmethod
    def _fetch_articles_multiple_categories(start, end, categories):
        try:
            all_articles = []
            seen_article_ids = set()
            
            for category in categories:
                success, data = ArticlesByRangeHandler._fetch_articles_single_category(start, end, category)
                if success and data:
                    ArticlesByRangeHandler._process_articles(data, all_articles, seen_article_ids)
                else:
                    print(f"Failed to process articles for category: {category}")
            
            return True, all_articles
        except Exception as e:
            print(f"Error occurred while fetching articles for multiple categories: {str(e)}")
            return False, []

    @staticmethod
    def _process_articles(articles, all_articles, seen_article_ids):
        try:
            for article in articles:
                if ArticlesByRangeHandler._is_valid_article(article):
                    article_id = article['Id']
                    if article_id not in seen_article_ids:
                        seen_article_ids.add(article_id)
                        all_articles.append(article)
                else:
                    all_articles.append(article)
        except Exception as e:
            print(f"Error occurred while processing articles: {str(e)}")

    @staticmethod
    def _is_valid_article(article):
        try:
            return isinstance(article, dict) and 'Id' in article
        except Exception as e:
            print(f"Error occurred while validating article: {str(e)}")
            return False

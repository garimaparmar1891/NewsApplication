from services.article_service import ArticleService
from utils.exception_handler import handle_exceptions
from flask import request
from controllers.base_controller import BaseController


class ArticleController(BaseController):
    
    def __init__(self):
        super().__init__()
        self.article_service = ArticleService()

    @handle_exceptions()
    def search_articles_by_keyword_and_range(self):
        user_id = self._get_user_id()
        keyword = self._get_request_param("q", required=True)
        if isinstance(keyword, tuple):
            return keyword
            
        date_params = self._get_validated_date_params()
        if isinstance(date_params, tuple):
            return date_params
        
        search_params = {
            'keyword': keyword,
            'start_date': date_params['start_date'],
            'end_date': date_params['end_date']
        }
        
        return self.article_service.search_articles_by_keyword_and_range(
            search_params, 
            user_id
        )

    @handle_exceptions()
    def get_today_headlines(self):
        user_id = self._get_user_id()
        return self.article_service.get_today_headlines(user_id)

    @handle_exceptions()
    def get_articles_by_range(self):
        user_id = self._get_user_id()
        date_params = self._get_validated_date_params()
        if isinstance(date_params, tuple):
            return date_params
            
        categories_param = request.args.get("categories")
        category_param = request.args.get("category")
        category_names = []
        
        if categories_param:
            category_names = [cat.strip() for cat in categories_param.split(",") if cat.strip()]
        elif category_param:
            category_names = [category_param.strip()] if category_param.strip() else []
        
        return self.article_service.get_articles_by_range(
            date_params, 
            category_names, 
            user_id
        )

    @handle_exceptions()
    def get_all_categories(self):
        return self.article_service.get_all_categories()

    @handle_exceptions()
    def get_all_articles(self):
        user_id = self._get_user_id()
        return self.article_service.get_all_articles(user_id)

    @handle_exceptions()
    def record_article_read(self, article_id):
        user_id = self._get_user_id()
        return self.article_service.record_article_read(user_id, article_id)

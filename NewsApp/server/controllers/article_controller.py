from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from services.article_service import ArticleService
from utils.response_utils import success_response, error_response
from http import HTTPStatus


class ArticleController:
    def __init__(self):
        self.article_service = ArticleService()

    def get_today_headlines(self):
        return self._respond_with_articles(
            self.article_service.get_today_headlines(),
            "No headlines available"
        )

    def get_articles_by_range(self):
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        category = request.args.get("category")

        if not (start_date and end_date):
            return self._missing_params_response("start_date and end_date")

        articles = self.article_service.get_articles_by_range(start_date, end_date, category)
        return self._respond_with_articles(articles, "No articles found in the given range") 

    def search_articles_by_keyword_and_range(self):
        keyword = request.args.get("q")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if not all([keyword, start_date, end_date]):
            return self._missing_params_response("q, start_date, end_date")

        try:
            articles = self.article_service.search_articles_by_keyword_and_range(keyword, start_date, end_date)
            return self._respond_with_articles(articles, "No articles found for the keyword")
        except Exception as e:
            return error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR) 

    def get_all_categories(self):
        categories = self.article_service.get_all_categories()
        return success_response(data=categories)


    def record_article_read(self, article_id):
        user_id = self._get_user_id_or_unauthorized()
        if not user_id:
            return error_response("Unauthorized", HTTPStatus.UNAUTHORIZED)

        if self.article_service.record_article_read(user_id, article_id):
            return jsonify({"success": True}), HTTPStatus.OK

        return jsonify({"success": False, "message": "Failed to store read history"}), HTTPStatus.INTERNAL_SERVER_ERROR


    def _get_user_id_or_unauthorized(self):
        return get_jwt_identity()

    def _respond_with_articles(self, articles, error_msg):
        return (
            success_response(data=articles)
            if articles
            else error_response(error_msg, HTTPStatus.NOT_FOUND)
        )

    def _missing_params_response(self, params):
        return error_response(
            f"Missing required parameters: {params}", HTTPStatus.BAD_REQUEST
        )

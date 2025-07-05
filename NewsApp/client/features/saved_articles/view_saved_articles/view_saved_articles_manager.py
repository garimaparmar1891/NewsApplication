from .view_saved_articles_service import SavedArticlesService
from utils.paginated_menu import PaginatedMenu

class SavedArticlesManager:
    @staticmethod
    def view_saved_articles_paginated():
        articles, error = SavedArticlesService.fetch_saved_articles()
        if error:
            print(error)
            return
        if not articles:
            print("No saved articles found.")
            return
        PaginatedMenu(articles, context_label="Saved Articles").show()

    @staticmethod
    def delete_saved_article(article_id):
        success, message = SavedArticlesService.delete_saved_article(article_id)
        print(message) 
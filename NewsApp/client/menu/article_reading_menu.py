from menu.menu_constants import (
    ARTICLE_READING_OPTIONS,
    ARTICLE_READING_SELECT_PROMPT,
    ARTICLE_READING_INVALID_CHOICE
)
from features.handlers.articles.article_reading_handler import ArticleReadingHandler

class ArticleReadingMenu:

    @staticmethod
    def display_menu():
        print("\nOptions:")
        for option in ARTICLE_READING_OPTIONS:
            print(option)

    @staticmethod
    def get_user_choice():
        return input(ARTICLE_READING_SELECT_PROMPT).strip()

    @staticmethod
    def handle_menu_choice(choice, article_id):
        if choice == "1":
            ArticleReadingHandler.handle_like_article(article_id)
            return True
        elif choice == "2":
            ArticleReadingHandler.handle_dislike_article(article_id)
            return True
        elif choice == "3":
            ArticleReadingHandler.handle_save_article(article_id)
            return True
        elif choice == "4":
            return False  # Go back to article list
        elif choice == "5":
            ArticleReadingHandler.handle_report_article(article_id)
            return True
        elif choice == "6":
            ArticleReadingHandler.handle_logout()
            return False
        else:
            print(ARTICLE_READING_INVALID_CHOICE)
            return True

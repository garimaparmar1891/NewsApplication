from .save_unsave_service import ArticleSaveService

class ArticleSaveManager:
    """Handles user interaction for saving and unsaving articles."""

    @staticmethod
    def save_article():
        print("\n--- Save Article ---")
        article_id = ArticleSaveManager.prompt_article_id("save")
        success, msg = ArticleSaveService.save_article(article_id)
        ArticleSaveManager.print_result(success, "save", msg)

    @staticmethod
    def unsave_article():
        print("\n--- Unsave Article ---")
        article_id = ArticleSaveManager.prompt_article_id("unsave")
        success, msg = ArticleSaveService.unsave_article(article_id)
        ArticleSaveManager.print_result(success, "unsave", msg)

    @staticmethod
    def prompt_article_id(action):
        return input(f"Enter Article ID to {action}: ").strip()

    @staticmethod
    def print_result(success, action, message=None):
        if success:
            print(f"Article {action}d successfully.")
        else:
            print(f"Failed to {action} article: {message or 'Unknown error'}") 
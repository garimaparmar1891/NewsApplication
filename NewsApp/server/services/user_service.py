from repositories.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def get_saved_articles(self, user_id):
        if not user_id:
            return self._error("Invalid user ID")

        articles = self.repo.get_saved_articles(user_id)
        if not articles:
            return self._error("No saved articles found")

        return self._success(data=articles)

    def unsave_article(self, user_id, article_id):
        if not self.repo.is_article_saved_by_user(user_id, article_id):
            return self._error("This article is not in your saved articles list")

        if self.repo.unsave_article(user_id, article_id):
            return self._success(message="Article unsaved successfully")

        return self._error("Failed to unsave article")

    # ---------- Private Helpers ----------
    def _success(self, data=None, message="Success"):
        response = {"success": True, "message": message}
        if data is not None:
            response["data"] = data
        return response

    def _error(self, message):
        return {"success": False, "message": message}

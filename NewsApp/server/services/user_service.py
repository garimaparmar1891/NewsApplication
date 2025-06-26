from repositories.user_repository import UserRepository
from constants.messages import (
    INVALID_USER_ID,
    NO_SAVED_ARTICLES,
    ARTICLE_NOT_SAVED,
    ARTICLE_UNSAVED_SUCCESS,
    ARTICLE_UNSAVE_FAILED
)


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def save_article(self, user_id, article_id):
        return self.repo.save_article(user_id, article_id)
    
    def get_saved_articles(self, user_id):
        if not user_id:
            return self._error(INVALID_USER_ID)

        articles = self.repo.get_saved_articles(user_id)
        if not articles:
            return self._error(NO_SAVED_ARTICLES)

        return self._success(data=articles)

    def unsave_article(self, user_id, article_id):
        if not self.repo.is_article_saved_by_user(user_id, article_id):
            return self._error(ARTICLE_NOT_SAVED)

        if self.repo.unsave_article(user_id, article_id):
            return self._success(message=ARTICLE_UNSAVED_SUCCESS)

        return self._error(ARTICLE_UNSAVE_FAILED)


    def _success(self, data=None, message="Success"):
        response = {"success": True, "message": message}
        if data is not None:
            response["data"] = data
        return response

    def _error(self, message):
        return {"success": False, "message": message}

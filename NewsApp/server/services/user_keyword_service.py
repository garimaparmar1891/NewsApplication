from repositories.user_keyword_repository import UserKeywordRepository
from constants.messages import (
    KEYWORD_ADDED,
    KEYWORD_ADD_FAILED,
    KEYWORD_DELETED,
    KEYWORD_NOT_FOUND,
    MISSING_KEYWORD_FIELDS
)


class UserKeywordService:
    def __init__(self):
        self.repo = UserKeywordRepository()

    def add_user_keyword(self, user_id, category_id, keyword):
        if not self._is_valid_input(category_id, keyword):
            return {"success": False, "message": MISSING_KEYWORD_FIELDS}

        cleaned_keyword = keyword.strip().lower()
        if self.repo.add_user_keyword(user_id, category_id, cleaned_keyword):
            return {"success": True, "message": KEYWORD_ADDED}

        return {"success": False, "message": KEYWORD_ADD_FAILED}

    def get_user_keywords(self, user_id):
        return self.repo.get_user_keywords(user_id)

    def delete_user_keyword(self, user_id, keyword_id):
        if self.repo.delete_user_keyword(user_id, keyword_id):
            return {"success": True, "message": KEYWORD_DELETED}

        return {"success": False, "message": KEYWORD_NOT_FOUND}


    def _is_valid_input(self, category_id, keyword):
        return bool(category_id and keyword and keyword.strip())

from repositories.user_keyword_repository import UserKeywordRepository


class UserKeywordService:
    def __init__(self):
        self.repo = UserKeywordRepository()

    def add_user_keyword(self, user_id, category_id, keyword):
        if not self._is_valid_input(category_id, keyword):
            return {"success": False, "message": "Invalid category ID or keyword"}

        success = self.repo.add_user_keyword(user_id, category_id, keyword.strip().lower())
        if success:
            return {"success": True, "message": "Keyword added"}
        return {"success": False, "message": "Keyword already exists or failed to add"}

    def get_user_keywords(self, user_id):
        return self.repo.get_user_keywords(user_id)

    def delete_user_keyword(self, user_id, keyword_id):
        success = self.repo.delete_user_keyword(user_id, keyword_id)
        if success:
            return {"success": True, "message": "Keyword deleted"}
        return {"success": False, "message": "Keyword not found or failed to delete"}

    # ---------- Private Helpers ----------
    def _is_valid_input(self, category_id, keyword):
        return bool(category_id and keyword and keyword.strip())

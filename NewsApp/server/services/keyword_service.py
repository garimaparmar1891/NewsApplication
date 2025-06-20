from repositories.keyword_repository import KeywordRepository


class KeywordService:
    def __init__(self):
        self.repo = KeywordRepository()

    def get_all_keywords(self):
        return self.repo.get_all_keywords()

    def add_keyword(self, word, category_id):
        if not self._is_valid_input(word, category_id):
            return {"error": "Keyword and category_id are required", "status": 400}

        cleaned_word = self._clean_word(word)
        return self.repo.add_keyword(cleaned_word, category_id)

    def delete_keyword(self, keyword_id):
        return self.repo.delete_keyword(keyword_id)

    # ---------- Private Helpers ----------

    def _is_valid_input(self, word, category_id):
        return bool(word and category_id)

    def _clean_word(self, word):
        return word.strip().lower()


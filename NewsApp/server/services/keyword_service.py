from repositories.keyword_repository import KeywordRepository
from constants import messages
from http import HTTPStatus


class KeywordService:
    def __init__(self):
        self.repo = KeywordRepository()

    def get_all_keywords(self):
        return self.repo.get_all_keywords()

    def add_keyword(self, word, category_id):
        if not self._is_valid_input(word, category_id):
            return {
                "error": messages.MISSING_KEYWORD_FIELDS,
                "status": HTTPStatus.BAD_REQUEST
            }

        cleaned_word = self._clean_word(word)
        return self.repo.add_keyword(cleaned_word, category_id)

    def delete_keyword(self, keyword_id):
        return self.repo.delete_keyword(keyword_id)


    def _is_valid_input(self, word, category_id):
        return bool(word and category_id)

    def _clean_word(self, word):
        return word.strip().lower()

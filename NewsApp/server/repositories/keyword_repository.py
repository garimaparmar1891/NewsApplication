from utils.db import fetch_all_query, execute_write_query
from queries import admin_queries as q
from constants import messages


class KeywordRepository:

    def get_all_keywords(self):
        return fetch_all_query(
            query=q.GET_ALL_KEYWORDS,
            row_mapper=self._map_keyword_row,
            error_msg=messages.DB_ERROR_GET_KEYWORDS
        )

    def add_keyword(self, word, category_id):
        return execute_write_query(
            query=q.INSERT_KEYWORD,
            params=(word, category_id),
            error_msg=messages.DB_ERROR_ADD_KEYWORD
        )

    def delete_keyword(self, word):
        return execute_write_query(
            query=q.DELETE_KEYWORD,
            params=(word,),
            error_msg=messages.DB_ERROR_DELETE_KEYWORD
        )

    def _map_keyword_row(self, row):
        return {
            "id": row.Id,
            "word": row.Word,
            "category_id": row.CategoryId
        }

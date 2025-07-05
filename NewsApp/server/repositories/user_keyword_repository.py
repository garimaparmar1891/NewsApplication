from utils.db import fetch_one_query, fetch_all_query_with_params, execute_write_query
from queries import user_keywords as q
from constants import messages

class UserKeywordRepository:
    def check_user_keyword_exists(self, user_id, category_id, keyword):
        return fetch_one_query(q.CHECK_USER_KEYWORD_EXISTS, (user_id, category_id, keyword))

    def insert_user_keyword(self, user_id, category_id, keyword):
        return execute_write_query(q.INSERT_USER_KEYWORD, (user_id, category_id, keyword), messages.DB_ERROR_ADD_USER_KEYWORD)

    def get_user_keywords(self, user_id):
        def map_keyword_row(row):
            return {
                "id": row.Id if hasattr(row, 'Id') else row[0],
                "keyword": row.Keyword if hasattr(row, 'Keyword') else row[1],
                "category": row.Category if hasattr(row, 'Category') else row[2]
            }
        return fetch_all_query_with_params(q.GET_USER_KEYWORDS, map_keyword_row, messages.DB_ERROR_GET_USER_KEYWORDS, (user_id,))

    def delete_user_keyword(self, user_id, keyword_id):
        return execute_write_query(q.DELETE_USER_KEYWORD, (keyword_id, user_id), messages.DB_ERROR_DELETE_USER_KEYWORD)

    def get_user_keywords_map(self, user_id):
        rows = fetch_all_query_with_params(q.GET_USER_KEYWORD_MAP, lambda row: row, messages.DB_ERROR_GET_USER_KEYWORD_MAP, (user_id,))
        keyword_map = {}
        for row in rows:
            keyword_map.setdefault(row.CategoryId, []).append(row.Keyword.lower())
        return keyword_map


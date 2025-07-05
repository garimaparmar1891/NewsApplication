from utils.db import fetch_one_query
from queries import category_queries as q
from constants import messages

class CategoryRepository:
    def get_category_by_name(self, name):
        try:
            row = fetch_one_query(q.GET_CATEGORY_BY_NAME, (name,))
            if row:
                return {"Id": row[0], "Name": row[1]}
            return None
        except Exception:
            raise Exception(messages.DB_ERROR_GET_CATEGORY_BY_NAME)

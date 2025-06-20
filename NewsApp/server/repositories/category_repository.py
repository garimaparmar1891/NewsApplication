from utils.db import get_db_connection
from queries import category_queries as q

class CategoryRepository:
    def get_category_by_name(self, name):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.GET_CATEGORY_BY_NAME, (name,))
            row = cursor.fetchone()
            if row:
                return {"Id": row.Id, "Name": row.Name}
            return None

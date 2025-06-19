from utils.db import get_db_connection

class CategoryRepository:
    def get_category_by_name(self, name):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Id, Name FROM Categories WHERE Name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return {"Id": row[0], "Name": row[1]}
            return None

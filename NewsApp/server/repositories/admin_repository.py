from utils.db import get_db_connection
from queries import admin_queries
from datetime import datetime


class AdminRepository:
    def get_external_servers(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(admin_queries.GET_EXTERNAL_SERVERS)
            return [
                {
                    "id": row.Id,
                    "name": row.Name,
                    "api_key": row.ApiKey,
                    "base_url": row.BaseUrl,
                    "is_active": row.IsActive,
                    "last_accessed": row.LastAccessed
                }
                for row in cursor.fetchall()
            ]

    def add_external_server(self, name, base_url, api_key):
        return self._execute_write_query(
            admin_queries.INSERT_EXTERNAL_SERVER,
            (name, api_key, base_url),
            "[DB ERROR] add_external_server"
        )

    def delete_external_server(self, server_id):
        return self._execute_delete_query(
            admin_queries.DELETE_EXTERNAL_SERVER,
            (server_id,),
            "[DB ERROR] delete_external_server"
        )

    def get_categories(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(admin_queries.GET_CATEGORIES)
            return [{"id": row.Id, "name": row.Name} for row in cursor.fetchall()]

    def add_category(self, name):
        return self._execute_write_query(
            admin_queries.INSERT_CATEGORY,
            (name,),
            "[DB ERROR] add_category"
        )

    def delete_category(self, category_id):
        return self._execute_delete_query(
            admin_queries.DELETE_CATEGORY,
            (category_id,),
            "[DB ERROR] delete_category"
        )

    def update_external_server(self, server_id, data):
        update_fields = []
        params = []

        if "Name" in data:
            update_fields.append("Name = ?")
            params.append(data["Name"])

        if "Api_key" in data:
            update_fields.append("ApiKey = ?")
            params.append(data["Api_key"])

        if "Base_Url" in data:
            update_fields.append("BaseUrl = ?")
            params.append(data["Base_Url"])

        if "Is_Active" in data:
            update_fields.append("IsActive = ?")
            params.append(int(data["Is_Active"]))

        update_fields.append("LastAccessed = ?")
        params.append(datetime.now())

        if not update_fields:
            return False

        params.append(server_id)
        sql = admin_queries.UPDATE_EXTERNAL_SERVER_BASE.format(fields=", ".join(update_fields))

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                conn.commit()
                return True
        except Exception as e:
            print(f"[DB ERROR] update_external_server: {e}")
            return False

    def _execute_write_query(self, query, params, error_msg):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return True
        except Exception as e:
            print(f"{error_msg}: {e}")
            return False

    def _execute_delete_query(self, query, params, error_msg):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"{error_msg}: {e}")
            return False

from utils.db import get_db_connection
from queries import admin_queries


class AdminRepository:

    def get_external_servers(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(admin_queries.GET_EXTERNAL_SERVERS)
            return [
                {
                    "Id": row.Id,
                    "Name": row.Name,
                    "Api_key": row.ApiKey,
                    "Base_Url": row.BaseUrl,
                    "Is_Active": row.IsActive,
                    "last_Accessed": row.LastAccessed
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

    # ---------- Private Helpers ----------
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


    def update_external_server(self, server_id, data):
        conn = get_db_connection()
        cursor = conn.cursor()

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

        if not update_fields:
            return False  # nothing to update

        params.append(server_id)

        sql = f"""
            UPDATE ExternalServers
            SET {', '.join(update_fields)}
            WHERE Id = ?
        """
        try:
            cursor.execute(sql, params)
            conn.commit()
            return True
        except Exception as e:
            print(f"DB Error while updating server: {e}")
            return False
        finally:
            conn.close()

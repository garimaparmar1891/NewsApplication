from datetime import datetime
from utils.db import get_db_connection
from queries import admin_queries


class AdminRepository:
    def get_external_servers(self):
        return self._fetch_all(
            query=admin_queries.GET_EXTERNAL_SERVERS,
            row_mapper=self._map_external_server_row
        )

    def update_external_server(self, server_id, data):
        update_fields, params = self._prepare_update_fields(data)

        if not update_fields:
            return False

        update_fields.append("LastAccessed = ?")
        params.append(datetime.now())
        params.append(server_id)

        query = admin_queries.UPDATE_EXTERNAL_SERVER.format(fields=", ".join(update_fields))
        return self._execute_write(query, params, "[DB ERROR] update_external_server")


    def get_categories(self):
        return self._fetch_all(
            query=admin_queries.GET_CATEGORIES,
            row_mapper=self._map_category_row
        )

    def get_category_by_id(self, category_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(admin_queries.GET_CATEGORY_BY_ID, (category_id,))
            return cursor.fetchone()

    def add_category(self, name):
        return self._execute_write(
            admin_queries.INSERT_CATEGORY,
            (name,),
            "[DB ERROR] add_category"
        )

    def hide_category_by_id(self, category_id):
        return self._execute_write(
            admin_queries.HIDE_CATEGORY_BY_ID,
            (category_id,),
            "[DB ERROR] hide_category_by_id"
        )


    def _prepare_update_fields(self, data):
        update_fields = []
        params = []

        field_mapping = {
            "Name": "Name",
            "Api_key": "ApiKey",
            "Base_Url": "BaseUrl",
            "Is_Active": "IsActive"
        }

        for key, db_field in field_mapping.items():
            if key in data:
                update_fields.append(f"{db_field} = ?")
                value = int(data[key]) if key == "Is_Active" else data[key]
                params.append(value)

        return update_fields, params

    def _map_external_server_row(self, row):
        return {
            "id": row.Id,
            "name": row.Name,
            "api_key": row.ApiKey,
            "base_url": row.BaseUrl,
            "is_active": row.IsActive,
            "last_accessed": row.LastAccessed
        }

    def _map_category_row(self, row):
        return {
            "id": row.Id,
            "name": row.Name
        }

    def _execute_write(self, query, params, error_msg):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return True
        except Exception as e:
            print(f"{error_msg}: {e}")
            return False

    def _fetch_all(self, query, row_mapper):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                return [row_mapper(row) for row in rows]
        except Exception as e:
            print(f"[DB ERROR] fetch_all: {e}")
            return []

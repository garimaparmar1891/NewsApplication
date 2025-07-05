from datetime import datetime
from utils.db import execute_write_query, fetch_all_query
from queries import admin_queries, category_queries
from constants import messages

class AdminRepository:
    def get_external_servers(self):
        return fetch_all_query(
            query=admin_queries.GET_EXTERNAL_SERVERS,
            row_mapper=self._map_external_server,
            error_msg=messages.DB_ERROR_GET_EXTERNAL_SERVERS
        )

    def update_external_server(self, server_id, data):
        update_fields, params = self._build_update_params(data)
        if not update_fields:
            return False
        
        update_fields.append("LastAccessed = ?")
        params.extend([datetime.now(), server_id])
        query = admin_queries.UPDATE_EXTERNAL_SERVER.format(fields=", ".join(update_fields))
        return execute_write_query(query, params, messages.DB_ERROR_UPDATE_EXTERNAL_SERVER)

    def get_categories(self):
        return fetch_all_query(
            query=category_queries.GET_CATEGORIES,
            row_mapper=self._map_category,
            error_msg=messages.DB_ERROR_GET_CATEGORIES
        )

    def add_category(self, name):
        return execute_write_query(
            admin_queries.INSERT_CATEGORY,
            (name,),
            messages.DB_ERROR_ADD_CATEGORY,
            integrity_error_msg="UNIQUE KEY constraint",
            integrity_exception=None
        )

    def get_keywords(self):
        return fetch_all_query(
            query=admin_queries.GET_ALL_KEYWORDS,
            row_mapper=self._map_keyword,
            error_msg=messages.DB_ERROR_GET_KEYWORDS
        )

    def add_keyword(self, word, category_id):
        return execute_write_query(
            admin_queries.INSERT_KEYWORD,
            (word, category_id),
            messages.DB_ERROR_ADD_KEYWORD,
            integrity_error_msg="UNIQUE KEY constraint",
            integrity_exception=None
        )

    def delete_keyword(self, word):
        return execute_write_query(
            admin_queries.DELETE_KEYWORD,
            (word,),
            messages.DB_ERROR_DELETE_KEYWORD
        )


    def _build_update_params(self, data):
        field_mapping = {
            "Name": "Name",
            "Api_key": "ApiKey", 
            "Base_Url": "BaseUrl",
            "Is_Active": "IsActive"
        }
        
        update_fields = []
        params = []
        
        for key, db_field in field_mapping.items():
            if key in data:
                update_fields.append(f"{db_field} = ?")
                value = int(data[key]) if key == "Is_Active" else data[key]
                params.append(value)
        
        return update_fields, params

    def _map_external_server(self, row):
        return {
            "id": row.Id,
            "name": row.Name,
            "api_key": row.ApiKey,
            "base_url": row.BaseUrl,
            "is_active": row.IsActive,
            "last_accessed": row.LastAccessed
        }

    def _map_category(self, row):
        return {
            "id": row.Id,
            "name": row.Name
        }

    def _map_keyword(self, row):
        return {
            "id": row.Id,
            "word": row.Word,
            "category_id": row.CategoryId
        }

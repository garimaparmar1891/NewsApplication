from utils.db import get_db_connection
from queries import external_server_queries as q

class ExternalServerRepository:
    def get_keys(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.GET_ALL_KEYS)
            rows = cursor.fetchall()

            keys = {}
            for row in rows:
                keys[row.Name] = {
                    "name": row.Name,
                    "api_key": row.ApiKey,
                    "is_active": row.IsActive,
                    "last_accessed": row.LastAccessed,
                    "base_url": row.BaseUrl
                }
            return keys

    def get_active_sources(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(q.GET_ACTIVE_SOURCES)
            rows = cursor.fetchall()
            return [
                {
                    "name": row.Name,
                    "api_key": row.ApiKey,
                    "is_active": row.IsActive,
                    "base_url": row.BaseUrl
                } for row in rows
            ]

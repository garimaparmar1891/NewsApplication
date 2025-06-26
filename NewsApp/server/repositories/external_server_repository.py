from utils.db import get_db_connection
from queries import external_server_queries as q


class ExternalServerRepository:

    def get_keys(self):
        rows = self._fetch_all(q.GET_ALL_KEYS)
        return {
            row.Name: {
                "name": row.Name,
                "api_key": row.ApiKey,
                "is_active": row.IsActive,
                "last_accessed": row.LastAccessed,
                "base_url": row.BaseUrl
            }
            for row in rows
        }


    def _fetch_all(self, query, params=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            return cursor.fetchall()

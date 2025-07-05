from utils.db import fetch_all_query
from queries import external_server_queries as q
from constants import messages


class ExternalServerRepository:

    def get_keys(self):
        rows = fetch_all_query(q.GET_ALL_KEYS, self._map_server_row, messages.DB_ERROR_GET_EXTERNAL_SERVER_KEYS)
        return rows

    def _map_server_row(self, row):
        return {
            "id": row.Id,
            "name": row.Name,
            "api_key": row.ApiKey,
            "is_active": row.IsActive,
            "last_accessed": row.LastAccessed,
            "base_url": row.BaseUrl
        }

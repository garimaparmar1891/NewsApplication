from utils.db import get_db_connection  # Assuming you have this
import logging

def load_api_keys():
    keys = {}
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Name, ApiKey FROM ExternalServers")
            for row in cursor.fetchall():
                keys[row.Name.lower()] = row.ApiKey
    except Exception as e:
        logging.error(f"Error loading API keys from DB: {e}")
    return keys

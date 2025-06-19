
import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        connection_string = (
            f"DRIVER={os.getenv('DB_DRIVER')};"
            f"SERVER={os.getenv('DB_SERVER')};"
            f"DATABASE={os.getenv('DB_NAME')};"
            f"Trusted_Connection={os.getenv('DB_TRUSTED_CONNECTION', 'yes')};"
        )
        return pyodbc.connect(connection_string)
    except pyodbc.Error as e:
        print(f"❌ Database connection failed: {e}")
        raise

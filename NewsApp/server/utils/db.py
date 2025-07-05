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
        print(f"Database connection failed: {e}")
        raise

def execute_write_query(query, params, error_msg, integrity_error_msg=None, integrity_exception=None):
    import pyodbc  # Ensure pyodbc is available in this scope
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            affected_rows = cursor.rowcount
            conn.commit()
            return affected_rows
    except pyodbc.IntegrityError as e:
        if integrity_error_msg and integrity_error_msg in str(e):
            if integrity_exception:
                raise integrity_exception
            raise Exception(integrity_error_msg)
        raise
    except Exception as e:
        raise Exception(f"{error_msg}: {str(e)}")

def fetch_all_query(query, row_mapper, error_msg):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return [row_mapper(row) for row in rows]
    except Exception as e:
        raise Exception(f"{error_msg}: {str(e)}")

def fetch_all_query_with_params(query, row_mapper, error_msg, params=None):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            return [row_mapper(row) for row in rows]
    except Exception as e:
        raise Exception(f"{error_msg}: {str(e)}")

def fetch_one_query(query, params=None, error_msg=None):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            row = cursor.fetchone()
            return row
    except Exception as e:
        if error_msg:
            raise Exception(f"{error_msg}: {str(e)}")
        raise

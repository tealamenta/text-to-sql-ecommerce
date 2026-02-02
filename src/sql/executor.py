import sqlite3
import pandas as pd
from src.config.settings import CONFIG


def get_connection():
    """Get SQLite connection."""
    return sqlite3.connect(CONFIG.db_path)


def execute_sql(sql: str, conn=None) -> tuple:
    """Execute SQL and return (success, result, error)."""
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True
    
    try:
        result = pd.read_sql(sql, conn)
        return True, result, None
    except Exception as e:
        return False, None, str(e)
    finally:
        if close_conn:
            conn.close()


def get_schema(conn=None) -> str:
    """Get database schema."""
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True
    
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    
    schema_parts = []
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in cursor.fetchall()]
        schema_parts.append(f"{table}({', '.join(columns)})")
    
    if close_conn:
        conn.close()
    
    return "\n".join(schema_parts)

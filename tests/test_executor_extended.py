import pytest
import sqlite3
import pandas as pd
from unittest.mock import patch, MagicMock
from src.sql.executor import execute_sql, get_schema


def test_get_schema_with_connection():
    """Test get_schema with provided connection."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    conn.execute("CREATE TABLE orders (id INTEGER, user_id INTEGER)")
    conn.commit()
    
    schema = get_schema(conn)
    
    assert "users" in schema
    assert "orders" in schema
    assert "id" in schema
    conn.close()


def test_execute_sql_with_join():
    """Test SQL with JOIN."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE a (id INTEGER, val TEXT)")
    conn.execute("CREATE TABLE b (id INTEGER, a_id INTEGER)")
    conn.execute("INSERT INTO a VALUES (1, 'test')")
    conn.execute("INSERT INTO b VALUES (1, 1)")
    conn.commit()
    
    success, result, error = execute_sql(
        "SELECT a.val FROM a JOIN b ON a.id = b.a_id", 
        conn
    )
    
    assert success is True
    assert result.iloc[0]['val'] == 'test'
    conn.close()


def test_execute_sql_aggregate():
    """Test SQL with aggregation."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE sales (amount REAL)")
    conn.execute("INSERT INTO sales VALUES (100), (200), (300)")
    conn.commit()
    
    success, result, error = execute_sql(
        "SELECT SUM(amount) as total, AVG(amount) as avg FROM sales",
        conn
    )
    
    assert success is True
    assert result.iloc[0]['total'] == 600
    assert result.iloc[0]['avg'] == 200
    conn.close()


def test_execute_sql_group_by():
    """Test SQL with GROUP BY."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE items (category TEXT, price REAL)")
    conn.execute("INSERT INTO items VALUES ('A', 10), ('A', 20), ('B', 30)")
    conn.commit()
    
    success, result, error = execute_sql(
        "SELECT category, SUM(price) as total FROM items GROUP BY category",
        conn
    )
    
    assert success is True
    assert len(result) == 2
    conn.close()

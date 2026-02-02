import pytest
import pandas as pd
import sqlite3
from pathlib import Path
from src.sql.executor import execute_sql, get_schema, get_connection


@pytest.fixture
def db_connection():
    """Create test database connection."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE test (id INTEGER, name TEXT)")
    conn.execute("INSERT INTO test VALUES (1, 'Alice'), (2, 'Bob')")
    conn.commit()
    yield conn
    conn.close()


def test_execute_sql_success(db_connection):
    """Test successful SQL execution."""
    success, result, error = execute_sql("SELECT * FROM test", db_connection)
    assert success is True
    assert error is None
    assert len(result) == 2


def test_execute_sql_failure(db_connection):
    """Test failed SQL execution."""
    success, result, error = execute_sql("SELECT * FROM nonexistent", db_connection)
    assert success is False
    assert result is None
    assert error is not None


def test_execute_sql_count(db_connection):
    """Test COUNT query."""
    success, result, error = execute_sql("SELECT COUNT(*) as total FROM test", db_connection)
    assert success is True
    assert result.iloc[0]['total'] == 2


def test_execute_sql_where(db_connection):
    """Test WHERE clause."""
    success, result, error = execute_sql("SELECT * FROM test WHERE name = 'Alice'", db_connection)
    assert success is True
    assert len(result) == 1
    assert result.iloc[0]['name'] == 'Alice'

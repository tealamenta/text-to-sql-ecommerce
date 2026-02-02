import pytest
from unittest.mock import patch, MagicMock
from src.sql.generator import extract_sql, generate_sql, call_llm, SCHEMA


def test_extract_sql_comments():
    """Test extracting SQL with comments."""
    response = """-- This query counts orders
SELECT COUNT(*) FROM orders;
-- End of query"""
    sql = extract_sql(response)
    assert "SELECT COUNT(*)" in sql
    assert "--" not in sql


def test_extract_sql_multiple_statements():
    """Test extracting first statement only."""
    response = "SELECT * FROM a; SELECT * FROM b;"
    sql = extract_sql(response)
    assert sql == "SELECT * FROM a;"


def test_schema_contains_all_tables():
    """Test schema contains all required tables."""
    tables = ['customers', 'orders', 'order_items', 'products', 'payments', 'reviews']
    for table in tables:
        assert table in SCHEMA


@patch('src.sql.generator.requests.post')
def test_call_llm_success(mock_post):
    """Test successful LLM call."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "SELECT * FROM orders;"}
    mock_post.return_value = mock_response
    
    result = call_llm("test prompt")
    
    assert result == "SELECT * FROM orders;"
    mock_post.assert_called_once()


@patch('src.sql.generator.requests.post')
def test_call_llm_timeout(mock_post):
    """Test LLM call timeout."""
    mock_post.side_effect = Exception("Timeout")
    
    result = call_llm("test prompt")
    
    assert "ERROR" in result


@patch('src.sql.generator.call_llm')
def test_generate_sql(mock_llm):
    """Test generate_sql function."""
    mock_llm.return_value = "SELECT COUNT(*) FROM orders;"
    
    result = generate_sql("How many orders?")
    
    assert "SELECT COUNT(*)" in result
    mock_llm.assert_called_once()

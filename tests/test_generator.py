import pytest
from src.sql.generator import (
    SCHEMA,
    FEW_SHOT_EXAMPLES,
    PROMPT_TEMPLATE,
    extract_sql
)


def test_schema_exists():
    """Test schema is defined."""
    assert SCHEMA is not None
    assert "customers" in SCHEMA
    assert "orders" in SCHEMA
    assert "products" in SCHEMA


def test_few_shot_examples_exist():
    """Test few-shot examples are defined."""
    assert FEW_SHOT_EXAMPLES is not None
    assert "SELECT" in FEW_SHOT_EXAMPLES
    assert "COUNT" in FEW_SHOT_EXAMPLES


def test_prompt_template():
    """Test prompt template has placeholders."""
    assert "{schema}" in PROMPT_TEMPLATE
    assert "{examples}" in PROMPT_TEMPLATE
    assert "{question}" in PROMPT_TEMPLATE


def test_extract_sql_simple():
    """Test extracting simple SQL."""
    response = "SELECT * FROM orders;"
    sql = extract_sql(response)
    assert sql == "SELECT * FROM orders;"


def test_extract_sql_markdown():
    """Test extracting SQL from markdown."""
    response = "```sql\nSELECT * FROM orders;\n```"
    sql = extract_sql(response)
    assert "SELECT * FROM orders" in sql


def test_extract_sql_with_explanation():
    """Test extracting SQL with explanation."""
    response = "Here is the query:\n```sql\nSELECT COUNT(*) FROM orders;\n```\nThis counts all orders."
    sql = extract_sql(response)
    assert "SELECT COUNT(*) FROM orders" in sql


def test_extract_sql_multiline():
    """Test extracting multiline SQL."""
    response = """SELECT 
        customer_id,
        COUNT(*) as total
    FROM orders
    GROUP BY customer_id;"""
    sql = extract_sql(response)
    assert "SELECT" in sql
    assert "GROUP BY" in sql

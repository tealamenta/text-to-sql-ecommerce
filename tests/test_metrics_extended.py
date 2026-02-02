import pytest
import pandas as pd
from src.evaluation.metrics import compare_results, normalize_sql, exact_match


def test_compare_results_numeric_tolerance():
    """Test numeric comparison with tolerance."""
    df1 = pd.DataFrame({'value': [100.0]})
    df2 = pd.DataFrame({'value': [100.5]})
    assert compare_results(df1, df2) is True


def test_compare_results_string_numbers():
    """Test comparing string representations of numbers."""
    df1 = pd.DataFrame({'count': ['10']})
    df2 = pd.DataFrame({'count': ['10']})
    assert compare_results(df1, df2) is True


def test_compare_results_unsorted():
    """Test comparing unsorted results."""
    df1 = pd.DataFrame({'val': [3, 1, 2]})
    df2 = pd.DataFrame({'val': [1, 2, 3]})
    assert compare_results(df1, df2) is True


def test_normalize_sql_complex():
    """Test normalizing complex SQL."""
    sql = """
    SELECT   c.customer_id,
             COUNT(*)   as   total
    FROM     customers c
    JOIN     orders o ON c.id = o.customer_id
    GROUP BY c.customer_id;
    """
    normalized = normalize_sql(sql)
    assert "select" in normalized
    assert "  " not in normalized  # No double spaces


def test_exact_match_case_insensitive():
    """Test exact match is case insensitive."""
    sql1 = "SELECT * FROM Orders"
    sql2 = "select * from orders"
    assert exact_match(sql1, sql2) is True


def test_exact_match_whitespace():
    """Test exact match ignores extra whitespace."""
    sql1 = "SELECT  *  FROM  table"
    sql2 = "SELECT * FROM table"
    assert exact_match(sql1, sql2) is True

import pytest
import pandas as pd
from src.evaluation.metrics import (
    compare_results,
    execution_accuracy,
    normalize_sql,
    exact_match
)


def test_compare_results_equal():
    """Test comparing equal results."""
    df1 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    df2 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    assert compare_results(df1, df2) is True


def test_compare_results_different():
    """Test comparing different results."""
    df1 = pd.DataFrame({'a': [1, 2]})
    df2 = pd.DataFrame({'a': [3, 4]})
    assert compare_results(df1, df2) is False


def test_compare_results_different_shape():
    """Test comparing different shapes."""
    df1 = pd.DataFrame({'a': [1, 2, 3]})
    df2 = pd.DataFrame({'a': [1, 2]})
    assert compare_results(df1, df2) is False


def test_compare_results_none():
    """Test comparing with None."""
    df1 = pd.DataFrame({'a': [1]})
    assert compare_results(df1, None) is False
    assert compare_results(None, df1) is False


def test_compare_results_empty():
    """Test comparing empty dataframes."""
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    assert compare_results(df1, df2) is True


def test_normalize_sql():
    """Test SQL normalization."""
    sql = "  SELECT * FROM  table;  "
    normalized = normalize_sql(sql)
    assert normalized == "select * from table"


def test_normalize_sql_uppercase():
    """Test SQL normalization with uppercase."""
    sql = "SELECT COUNT(*) FROM Orders WHERE Status = 'active'"
    normalized = normalize_sql(sql)
    assert "select" in normalized
    assert "from" in normalized


def test_exact_match_true():
    """Test exact match with identical queries."""
    sql1 = "SELECT * FROM table;"
    sql2 = "  select * from table  "
    assert exact_match(sql1, sql2) is True


def test_exact_match_false():
    """Test exact match with different queries."""
    sql1 = "SELECT * FROM table1"
    sql2 = "SELECT * FROM table2"
    assert exact_match(sql1, sql2) is False


def test_execution_accuracy():
    """Test execution accuracy metric."""
    df1 = pd.DataFrame({'count': [10]})
    df2 = pd.DataFrame({'count': [10]})
    assert execution_accuracy(df1, df2) is True

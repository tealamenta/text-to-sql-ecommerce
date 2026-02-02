import pandas as pd


def compare_results(result1: pd.DataFrame, result2: pd.DataFrame) -> bool:
    """Compare two SQL query results."""
    try:
        if result1 is None or result2 is None:
            return False
        if result1.empty and result2.empty:
            return True
        if result1.shape[0] != result2.shape[0]:
            return False
        
        # Compare last column values
        v1 = sorted([str(x) for x in result1.iloc[:, -1].tolist()])
        v2 = sorted([str(x) for x in result2.iloc[:, -1].tolist()])
        
        if v1 == v2:
            return True
        
        # Numeric comparison with tolerance
        try:
            n1 = sorted([float(x) for x in result1.iloc[:, -1].tolist()])
            n2 = sorted([float(x) for x in result2.iloc[:, -1].tolist()])
            return all(abs(a - b) < 1 for a, b in zip(n1, n2))
        except (ValueError, TypeError):
            return False
    except Exception:
        return False


def execution_accuracy(generated_result: pd.DataFrame, expected_result: pd.DataFrame) -> bool:
    """Calculate execution accuracy."""
    return compare_results(generated_result, expected_result)


def normalize_sql(sql: str) -> str:
    """Normalize SQL for comparison."""
    sql = sql.lower().strip()
    sql = " ".join(sql.split())
    sql = sql.rstrip(";")
    return sql


def exact_match(sql1: str, sql2: str) -> bool:
    """Check if two SQL queries are identical."""
    return normalize_sql(sql1) == normalize_sql(sql2)

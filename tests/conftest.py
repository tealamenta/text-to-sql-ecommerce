import pytest
import sqlite3
import pandas as pd
from pathlib import Path


@pytest.fixture
def sample_db():
    """Create a sample e-commerce database for testing."""
    conn = sqlite3.connect(":memory:")
    
    # Create tables
    conn.execute("""
        CREATE TABLE customers (
            customer_id TEXT PRIMARY KEY,
            customer_city TEXT,
            customer_state TEXT
        )
    """)
    
    conn.execute("""
        CREATE TABLE orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT,
            order_status TEXT,
            order_purchase_timestamp TEXT
        )
    """)
    
    conn.execute("""
        CREATE TABLE products (
            product_id TEXT PRIMARY KEY,
            product_category TEXT
        )
    """)
    
    conn.execute("""
        CREATE TABLE order_items (
            order_id TEXT,
            product_id TEXT,
            price REAL
        )
    """)
    
    # Insert sample data
    conn.execute("INSERT INTO customers VALUES ('c1', 'Paris', 'FR')")
    conn.execute("INSERT INTO customers VALUES ('c2', 'Lyon', 'FR')")
    conn.execute("INSERT INTO orders VALUES ('o1', 'c1', 'delivered', '2024-01-01')")
    conn.execute("INSERT INTO orders VALUES ('o2', 'c2', 'shipped', '2024-01-02')")
    conn.execute("INSERT INTO products VALUES ('p1', 'electronics')")
    conn.execute("INSERT INTO order_items VALUES ('o1', 'p1', 100.0)")
    
    conn.commit()
    yield conn
    conn.close()


@pytest.fixture
def test_questions():
    """Sample test questions."""
    return [
        {
            "question": "How many orders?",
            "sql": "SELECT COUNT(*) FROM orders",
            "difficulty": "simple"
        },
        {
            "question": "How many customers?",
            "sql": "SELECT COUNT(*) FROM customers",
            "difficulty": "simple"
        }
    ]

import requests
from src.config.settings import CONFIG

SCHEMA = """Tables:
- customers(customer_id, customer_city, customer_state)
- orders(order_id, customer_id, order_status, order_purchase_timestamp, order_delivered_timestamp)
- order_items(order_id, order_item_id, product_id, price, freight_value)
- products(product_id, product_category, product_weight_g)
- payments(order_id, payment_sequential, payment_type, payment_installments, payment_value)
- reviews(review_id, order_id, review_score, review_comment_title, review_comment_message)"""

FEW_SHOT_EXAMPLES = """
Example 1 - Simple COUNT:
Q: How many orders are there?
SQL: SELECT COUNT(*) as total FROM orders;

Example 2 - COUNT with WHERE:
Q: How many delivered orders?
SQL: SELECT COUNT(*) as total FROM orders WHERE order_status = 'delivered';

Example 3 - COUNT DISTINCT (count unique values):
Q: How many orders per payment method?
SQL: SELECT payment_type, COUNT(DISTINCT order_id) as num_orders FROM payments GROUP BY payment_type ORDER BY num_orders DESC;

Example 4 - Revenue = price only (NOT freight):
Q: Total revenue by product category?
SQL: SELECT p.product_category, SUM(oi.price) as revenue FROM order_items oi JOIN products p ON oi.product_id = p.product_id GROUP BY p.product_category ORDER BY revenue DESC;

Example 5 - Average basket = AVG of price only:
Q: Average basket by city?
SQL: SELECT c.customer_city, ROUND(AVG(oi.price), 2) as avg_basket FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_items oi ON o.order_id = oi.order_id GROUP BY c.customer_city ORDER BY avg_basket DESC;

Example 6 - Date difference (use julianday):
Q: Average delivery time by state?
SQL: SELECT c.customer_state, ROUND(AVG(julianday(o.order_delivered_timestamp) - julianday(o.order_purchase_timestamp)), 2) as avg_days FROM customers c JOIN orders o ON c.customer_id = o.customer_id WHERE o.order_delivered_timestamp IS NOT NULL GROUP BY c.customer_state ORDER BY avg_days;

Example 7 - Products with low rating (HAVING):
Q: Products with average rating below 3?
SQL: SELECT p.product_id, p.product_category, ROUND(AVG(r.review_score), 2) as avg_score FROM products p JOIN order_items oi ON p.product_id = oi.product_id JOIN reviews r ON oi.order_id = r.order_id GROUP BY p.product_id, p.product_category HAVING AVG(r.review_score) < 3 ORDER BY avg_score;
"""

PROMPT_TEMPLATE = """You are a SQLite expert. Generate SQL for an e-commerce database.

{schema}

RULES:
- Use aliases: c=customers, o=orders, oi=order_items, p=products, r=reviews
- Revenue/basket = price only (NOT freight_value)
- COUNT(DISTINCT x) for unique values
- julianday() for date math
- End with semicolon

{examples}

Q: {question}
SQL:"""


def call_llm(prompt: str) -> str:
    try:
        response = requests.post(
            CONFIG.ollama_url,
            json={
                "model": CONFIG.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": CONFIG.temperature,
                    "num_predict": CONFIG.max_tokens
                }
            },
            timeout=120
        )
        return response.json().get("response", "").strip()
    except Exception as e:
        return f"ERROR: {e}"


def extract_sql(response: str) -> str:
    sql = response.strip()
    if "```sql" in sql:
        sql = sql.split("```sql")[1].split("```")[0].strip()
    elif "```" in sql:
        sql = sql.split("```")[1].split("```")[0].strip()
    lines = [l for l in sql.split("\n") if l.strip() and not l.strip().startswith("--")]
    sql = " ".join(lines)
    if ";" in sql:
        sql = sql.split(";")[0] + ";"
    return sql


def generate_sql(question: str) -> str:
    prompt = PROMPT_TEMPLATE.format(
        schema=SCHEMA,
        examples=FEW_SHOT_EXAMPLES,
        question=question
    )
    response = call_llm(prompt)
    return extract_sql(response)

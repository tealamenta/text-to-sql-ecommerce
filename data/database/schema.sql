CREATE TABLE customers (
  customer_id TEXT,
  customer_city TEXT,
  customer_state TEXT
);

CREATE TABLE products (
  product_id TEXT,
  product_category TEXT,
  product_weight_g REAL,
  product_length_cm REAL,
  product_height_cm REAL,
  product_width_cm REAL
);

CREATE TABLE orders (
  order_id TEXT,
  customer_id TEXT,
  order_status TEXT,
  order_purchase_timestamp TEXT,
  order_delivered_timestamp TEXT
);

CREATE TABLE order_items (
  order_id TEXT,
  order_item_id INTEGER,
  product_id TEXT,
  price REAL,
  freight_value REAL
);

CREATE TABLE payments (
  order_id TEXT,
  payment_sequential INTEGER,
  payment_type TEXT,
  payment_installments INTEGER,
  payment_value REAL
);

CREATE TABLE reviews (
  review_id TEXT,
  order_id TEXT,
  review_score INTEGER,
  review_comment_title TEXT,
  review_comment_message TEXT
);
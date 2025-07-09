import sqlite3

DB_NAME = "tracker.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            title TEXT,
            current_price REAL,
            desired_price REAL,
            email_sent INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def save_product(url, title, current_price, desired_price):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO products (url, title, current_price, desired_price, email_sent)
        VALUES (?, ?, ?, ?, 0)
    ''', (url, title, current_price, desired_price))
    conn.commit()
    conn.close()

def get_all_products():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE email_sent = 0")
    rows = cursor.fetchall()
    conn.close()
    return rows

def mark_email_sent(product_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET email_sent = 1 WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
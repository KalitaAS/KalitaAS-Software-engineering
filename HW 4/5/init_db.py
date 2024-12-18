import sqlite3
import os

conn = sqlite3.connect('cosmetics_shop.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS manufacturers (
    manufacturer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT,
    contact_email TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category_id INTEGER,
    manufacturer_id INTEGER,
    price DECIMAL(10,2),
    stock_quantity INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories (category_id),
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers (manufacturer_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    sale_date DATE,
    quantity INTEGER,
    total_price DECIMAL(10,2),
    FOREIGN KEY (product_id) REFERENCES products (product_id)
)
''')

conn.commit()
conn.close()

print('База данных успешно создана!')

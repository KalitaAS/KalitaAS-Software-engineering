import sqlite3
import json
from datetime import datetime


def execute_query(cursor, query, params=None):
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    columns = [description[0] for description in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results


def save_to_json(data, filename):
    with open(f'results_{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)



conn = sqlite3.connect('cosmetics_shop.db')
cursor = conn.cursor()

print('Топ-5 самых дорогих продуктов')
query = '''
SELECT p.name, p.price, c.name as category, m.name as manufacturer
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
WHERE p.stock_quantity > 0
ORDER BY p.price DESC
LIMIT 5
'''
results = execute_query(cursor, query)
save_to_json(results, 'top5_expensive_products')

print('Общая сумма продаж по производителям')
query = '''
SELECT m.name as manufacturer, 
        COUNT(s.sale_id) as total_sales,
        SUM(s.total_price) as total_revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
GROUP BY m.manufacturer_id
'''
results = execute_query(cursor, query)
save_to_json(results, 'sales_by_manufacturer')

print('Статистика по категориям')
query = '''
SELECT c.name as category,
        COUNT(p.product_id) as products_count,
        AVG(p.price) as avg_price,
        SUM(p.stock_quantity) as total_stock
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_id
'''
results = execute_query(cursor, query)
save_to_json(results, 'category_statistics')

print('Анализ продаж по датам')
query = '''
SELECT s.sale_date,
        COUNT(s.sale_id) as num_sales,
        SUM(s.quantity) as total_items_sold,
        SUM(s.total_price) as daily_revenue
FROM sales s
GROUP BY s.sale_date
ORDER BY s.sale_date
'''
results = execute_query(cursor, query)
save_to_json(results, 'daily_sales_analysis')

print('Товары с низким запасом')
query = '''
SELECT p.name, p.stock_quantity, c.name as category
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE p.stock_quantity < 50
ORDER BY p.stock_quantity
'''
results = execute_query(cursor, query)
save_to_json(results, 'low_stock_products')

print('Обновление цен на 10% для определенной категории')
cursor.execute('''
UPDATE products
SET price = price * 1.1
WHERE category_id = 1
''')
conn.commit()

print('Проверка обновленных цен')
query = '''
SELECT name, price
FROM products
WHERE category_id = 1
'''
results = execute_query(cursor, query)
save_to_json(results, 'updated_prices')
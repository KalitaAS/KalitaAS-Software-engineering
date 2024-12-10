import sqlite3
from csv import DictReader
import os

conn = sqlite3.connect('cosmetics_shop.db')
cursor = conn.cursor()


def load_data_from_csv(cursor, table_name, csv_file):
    with open(csv_file, 'r', encoding='utf-8') as file:
        for row in DictReader(file):
            columns = ', '.join(row.keys())
            placeholders = ', '.join(['?' for _ in row])
            query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
            cursor.execute(query, list(row.values()))

data_files = {
    'categories': 'data/categories.csv',
    'manufacturers': 'data/manufacturers.csv',
    'products': 'data/products.csv',
    'sales': 'data/sales.csv'
}

for table, file_path in data_files.items():
    load_data_from_csv(cursor, table, file_path)
    print(f'Данные успешно загружены в таблицу {table}')

conn.commit()
conn.close()